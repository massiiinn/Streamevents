from django.contrib import admin
from .models import Event

# Registra el model Event a l'administració de Django
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # Mostra aquestes columnes a la llista d'esdeveniments
    list_display = ('title', 'creator', 'category', 'status', 'scheduled_date', 'is_featured')
    
    # Filtres laterals per categoria, estat i destacat
    list_filter = ('category', 'status', 'is_featured')
    
    # Camps pels quals es pot fer cerca
    search_fields = ('title', 'description', 'tags')
    
    # Mostra el camp creator com a raw_id (ID) per facilitar selecció d'usuaris
    raw_id_fields = ('creator',)
