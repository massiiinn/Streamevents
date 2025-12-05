from django import forms
from .models import Event

# Formulari per crear esdeveniments
class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'scheduled_date', 'thumbnail', 'max_viewers', 'tags', 'stream_url']
        widgets = {
            # Estils per als camps del formulari
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'max_viewers': forms.NumberInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'stream_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

# Formulari per actualitzar esdeveniments
class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "category",
            "scheduled_date",
            "status",
            "thumbnail",
            "max_viewers",
            "tags",
            "stream_url",
        ]
        widgets = {
            # Estils per als camps del formulari
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "scheduled_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "thumbnail": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "max_viewers": forms.NumberInput(attrs={"class": "form-control"}),
            "tags": forms.TextInput(attrs={"class": "form-control"}),
            "stream_url": forms.URLInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajusta la data perquè el camp datetime-local mostri correctament la data existent
        if self.instance and self.instance.scheduled_date:
            self.initial["scheduled_date"] = self.instance.scheduled_date.strftime("%Y-%m-%dT%H:%M")

# Formulari de cerca per als esdeveniments
class EventSearchForm(forms.Form):
    q = forms.CharField(required=False)  # Cerca per títol
    category = forms.ChoiceField(
        required=False,
        choices=[("", "Totes"), ("gaming", "Gaming"), ("music", "Música"), ("sports", "Esports"),
                 ("education", "Educació"), ("technology", "Tecnologia"), ("entertainment", "Entreteniment"),
                 ("art", "Art"), ("other", "Altres")],
    )
    status = forms.ChoiceField(
        required=False,
        choices=[("", "Tots"), ("scheduled", "Programat"), ("live", "En directe"), ("finished", "Finalitzat")],
    )
