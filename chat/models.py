from django.db import models
from django.conf import settings
from django.utils.timesince import timesince
from events.models import Event

# =================== MODEL DE MISSATGE DE XAT ===================
# Representa cada missatge enviat durant un esdeveniment en directe
class ChatMessage(models.Model):
    # =================== CAMPS DEL MODEL ===================
    
    # Esdeveniment al qual pertany aquest missatge
    # Si s'elimina l'esdeveniment, s'eliminen tots els seus missatges (CASCADE)
    # related_name='messages' permet fer event.messages.all()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    # Usuari que ha enviat el missatge
    # Usem settings.AUTH_USER_MODEL per permetre models d'usuari personalitzats
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    # Contingut del missatge (màxim 500 caràcters)
    message = models.TextField(max_length=500)
    
    # Data i hora de creació (s'assigna automàticament)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Soft delete: marca el missatge com eliminat sense esborrar-lo de la BD
    # Permet mantenir un historial i recuperar missatges si cal
    is_deleted = models.BooleanField(default=False)
    
    # Indica si el creador de l'esdeveniment ha destacat aquest missatge
    is_highlighted = models.BooleanField(default=False)

    # =================== REPRESENTACIÓ EN TEXT ===================
    # Com es mostra el missatge al shell de Django o a l'admin
    # Format: "nomUsuari: primeres 50 lletres del missatge"
    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"

    # =================== PERMISOS D'ELIMINACIÓ ===================
    # Comprova si un usuari té permís per eliminar aquest missatge
    # Pot eliminar: el propi autor, el creador de l'esdeveniment, o staff
    def can_delete(self, user):
        # Si l'usuari no està autenticat, no pot eliminar res
        if not user.is_authenticated:
            return False
        # Staff (administradors) poden eliminar qualsevol missatge
        if user.is_staff:
            return True
        # L'autor del missatge pot eliminar el seu propi missatge
        if self.user == user:
            return True
        # El creador de l'esdeveniment pot moderar el xat
        if self.event.creator == user:
            return True
        # En qualsevol altre cas, no té permís
        return False

    # =================== NOM A MOSTRAR DE L'USUARI ===================
    # Retorna el display_name si existeix, sinó el username
    # Permet als usuaris tenir un nom personalitzat al xat
    def get_user_display_name(self):
        if hasattr(self.user, 'display_name') and self.user.display_name:
            return self.user.display_name
        return self.user.username

    # =================== TEMPS TRANSCORREGUT ===================
    # Calcula quant temps ha passat des de la creació del missatge
    # Retorna strings com "2 minuts", "1 hora", "3 dies"
    def get_time_since(self):
        return timesince(self.created_at)

    # =================== META CONFIGURACIÓ ===================
    class Meta:
        # Ordenar missatges del més antic al més recent
        ordering = ['created_at']
        # Noms humans per l'admin de Django
        verbose_name = 'Missatge de Xat'
        verbose_name_plural = 'Missatges de Xat'