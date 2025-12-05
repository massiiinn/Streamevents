from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    MyEventsView,
)

app_name = "events"

urlpatterns = [
    # Llista d'esdeveniments públics
    path("", EventListView.as_view(), name="event_list"),

    # Crear un nou esdeveniment
    path("create/", EventCreateView.as_view(), name="event_create"),

    # Veure detall d'un esdeveniment per ID
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),

    # Editar un esdeveniment existent per ID
    path("<int:pk>/edit/", EventUpdateView.as_view(), name="event_update"),

    # Eliminar un esdeveniment per ID
    path("<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),

    # Llista dels esdeveniments creats per l'usuari actual
    path("my-events/", MyEventsView.as_view(), name="my_events"),
]
