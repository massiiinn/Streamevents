from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from events.models import Event
from .models import ChatMessage
from .forms import ChatMessageForm


# =================== ENVIAR MISSATGE ===================
# Només usuaris autenticats (@login_required) i via POST (@require_POST)
@login_required
@require_POST
def chat_send_message(request, event_pk):
    # Obtenir l'esdeveniment o retornar 404
    event = get_object_or_404(Event, pk=event_pk)

    # Verificar que l'esdeveniment està en directe
    if event.status != 'live':
        return JsonResponse({
            'success': False,
            'error': 'L\'esdeveniment no està en directe'
        })

    # Validar el formulari amb les paraules ofensives i altres validacions
    form = ChatMessageForm(request.POST)

    if form.is_valid():
        # Crear el missatge sense desar-lo encara (commit=False)
        message = form.save(commit=False)
        # Assignar l'usuari i l'esdeveniment
        message.user = request.user
        message.event = event
        message.save()

        # Retornar JSON amb les dades del missatge creat
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'user': message.user.username,
                'display_name': message.get_user_display_name(),
                'message': message.message,
                'created_at': message.get_time_since(),
                'can_delete': message.can_delete(request.user),
                'is_highlighted': message.is_highlighted
            }
        })

    # Si el formulari no és vàlid, retornar els errors
    return JsonResponse({
        'success': False,
        'errors': form.errors
    })


# =================== CARREGAR MISSATGES ===================
# Obté els missatges d'un esdeveniment (utilitzat pel polling cada 3s)
def chat_load_messages(request, event_pk):
    try:
        event = get_object_or_404(Event, pk=event_pk)
        
        # Obtenir TOTS els missatges de l'esdeveniment
        all_messages = ChatMessage.objects.filter(event=event)
        
        # Filtrar manualment els no eliminats (per compatibilitat amb Djongo)
        # Djongo té problemes amb is_deleted=False al query, així que ho fem en Python
        non_deleted = []
        for message in all_messages.order_by('created_at'):
            if not message.is_deleted:  # Filtre manual
                non_deleted.append(message)
                if len(non_deleted) >= 50:  # Límit de 50 missatges
                    break
        
        # Construir la llista de diccionaris amb les dades dels missatges
        messages_data = []
        for m in non_deleted:
            messages_data.append({
                'id': m.id,
                'user': m.user.username,
                'display_name': m.get_user_display_name(),
                'message': m.message,
                'created_at': m.get_time_since(),
                'can_delete': m.can_delete(request.user),
                'is_highlighted': m.is_highlighted,
            })
        
        return JsonResponse({
            'messages': messages_data
        })
        
    except Exception as e:
        # Si hi ha error, retornar llista buida però marcar com a èxit
        # Evita que el polling es trenqui
        return JsonResponse({
            'messages': []
        })


# =================== ELIMINAR MISSATGE ===================
# Marca un missatge com eliminat (soft delete) si l'usuari té permisos
@login_required
@require_POST
def chat_delete_message(request, message_pk):
    message = get_object_or_404(ChatMessage, pk=message_pk)

    # Verificar permisos: autor, creador esdeveniment, o staff
    if not message.can_delete(request.user):
        return JsonResponse({
            'success': False,
            'error': 'No tens permisos per eliminar aquest missatge'
        })

    # Soft delete: marca com eliminat sense esborrar de la BD
    message.is_deleted = True
    message.save()

    return JsonResponse({'success': True})


# =================== DESTACAR MISSATGE (OPCIONAL) ===================
# Toggle del camp is_highlighted, només pel creador de l'esdeveniment
@login_required
@require_POST
def chat_highlight_message(request, message_pk):
    message = get_object_or_404(ChatMessage, pk=message_pk)

    # Només el creador de l'esdeveniment pot destacar missatges
    if message.event.creator != request.user:
        return JsonResponse({
            'success': False,
            'error': 'Només el creador de l\'esdeveniment pot destacar missatges'
        })

    # Toggle: si està destacat, treure-ho; si no, destacar-lo
    message.is_highlighted = not message.is_highlighted
    message.save()

    return JsonResponse({
        'success': True,
        'is_highlighted': message.is_highlighted
    })