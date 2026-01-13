from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event

class Command(BaseCommand):
    help = 'Actualitza automàticament els estats dels esdeveniments segons la data i la durada'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        events = Event.objects.all()

        for event in events:

            # Si està programat i ja ha començat → en directe  
            if event.status == 'scheduled' and event.scheduled_date <= now:
                event.status = 'live'
                event.save()
                continue

            # Si està en directe → comprovem la durada
            if event.status == 'live':
                duration = event.get_duration()
                finish_time = event.scheduled_date + duration

                if finish_time <= now:
                    event.status = 'finished'
                    event.save()

        self.stdout.write(self.style.SUCCESS('Estats actualitzats correctament'))
