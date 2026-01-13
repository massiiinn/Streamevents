from django import forms
from .models import ChatMessage

# =================== FORMULARI DE MISSATGE DE XAT ===================
# Formulari basat en el model ChatMessage per enviar missatges
class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']  # Només volem que l'usuari pugui editar el missatge
        widgets = {
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',  # Classe Bootstrap per estil
                    'rows': 2,  # Alçada del textarea (2 files)
                    'placeholder': 'Escriu un missatge...',  # Text d'ajuda
                    'maxlength': 500  # Límit màxim de caràcters al navegador
                }
            )
        }

    # =================== VALIDACIÓ PERSONALITZADA DEL MISSATGE ===================
    # Aquest mètode es crida automàticament quan Django valida el formulari
    def clean_message(self):
        # Obtenir el missatge i eliminar espais al principi i final
        message = self.cleaned_data.get('message', '').strip()

        # =================== VALIDACIÓ 1: MISSATGE BUIT ===================
        # Després de fer strip(), comprova que quedi alguna cosa
        if not message:
            raise forms.ValidationError('El missatge no pot estar buit.')

        # =================== VALIDACIÓ 2: LONGITUD MÀXIMA ===================
        # Verificar que no superi els 500 caràcters
        if len(message) > 500:
            raise forms.ValidationError('El missatge no pot superar els 500 caràcters.')

        # =================== VALIDACIÓ 3: PARAULES OFENSIVES ===================
        # Llista de paraules prohibides que no es poden enviar
        forbidden_words = [
            'puta', 'puto', 'gilipollas', 'idiota', 'mierda'
        ]

        # Convertir el missatge a minúscules per fer una comparació case-insensitive
        lower_message = message.lower().strip()
        
        # Comprovar si alguna paraula prohibida apareix al missatge
        for word in forbidden_words:
            if word in lower_message:
                raise forms.ValidationError('El missatge conté paraules ofensives.')

        # Si totes les validacions passen, retornar el missatge net
        return message