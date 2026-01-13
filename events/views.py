from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from .models import Event
from .forms import EventCreationForm, EventUpdateForm, EventSearchForm
from chat.forms import ChatMessageForm


# Llista general d'esdeveniments amb paginació i filtres
class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    paginate_by = 9

    def get_queryset(self):
        form = EventSearchForm(self.request.GET)
        queryset = Event.objects.all().order_by("scheduled_date")

        if form.is_valid():
            q = form.cleaned_data.get("q")
            category = form.cleaned_data.get("category")
            status = form.cleaned_data.get("status")

            if q:
                queryset = queryset.filter(title__icontains=q)
            if category:
                queryset = queryset.filter(category=category)
            if status:
                queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = EventSearchForm(self.request.GET)
        return context


# Detall d'un esdeveniment individual
class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadimos el formulario del chat
        context['chat_form'] = ChatMessageForm()
        return context


# Crear un nou esdeveniment (usuari autenticat)
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventCreationForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


# Mixin per assegurar que només el creador pot editar/eliminar
class CreatorRequiredMixin(UserPassesTestMixin):
    def test_user_passes(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs.get("pk"))
        return event.creator == self.request.user

    def test_func(self):
        event = self.get_object()
        return event.creator == self.request.user


# Actualitzar un esdeveniment (usuari creador)
class EventUpdateView(LoginRequiredMixin, CreatorRequiredMixin, UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        # Manté la data si no s'ha modificat
        if not form.cleaned_data.get("scheduled_date"):
            form.instance.scheduled_date = self.object.scheduled_date

        # Elimina la imatge si es marca el checkbox
        if "thumbnail-clear" in self.request.POST:
            form.instance.thumbnail = None

        return super().form_valid(form)


# Eliminar un esdeveniment (usuari creador)
class EventDeleteView(LoginRequiredMixin, CreatorRequiredMixin, DeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("events:event_list")


# Llista dels esdeveniments creats per l'usuari autenticat
class MyEventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/my_events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user).order_by("-created_at")
