from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import pymongo

from events.models import Event
from semantic_search.services.embeddings import embed_text, model_name

class Command(BaseCommand):
    help = "Genera y guarda embeddings para todos los eventos existentes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force", 
            action="store_true", 
            help="Recalcula embeddings incluso si ya existen"
        )
        parser.add_argument(
            "--limit", 
            type=int, 
            default=0, 
            help="Limita el número de eventos a procesar (0 = todos)"
        )

    def handle(self, *args, **options):
        force = options["force"]
        limit = options["limit"]

        db_settings = settings.DATABASES['default']
        client = pymongo.MongoClient(db_settings['CLIENT']['host'])
        db = client[db_settings['NAME']]
        collection = db['events_event']  

        query = {}
        if not force:
            query['embedding'] = {'$exists': False}
        
        cursor = collection.find(query).sort('created_at', 1)
        
        if limit and limit > 0:
            cursor = cursor.limit(limit)

        total_count = collection.count_documents(query)
        self.stdout.write(f"Procesando {total_count} eventos...")

        processed = 0
        skipped = 0
        
        for doc in cursor:
            event_id = doc.get('_id')
            
            text = " | ".join([
                (doc.get('title') or "").strip(),
                (doc.get('description') or "").strip(),
                (doc.get('category') or "").strip(),
                (doc.get('tags') or "").strip(),
            ]).strip()

            if not text:
                skipped += 1
                self.stdout.write(
                    self.style.WARNING(f"⚠ Skipped ID {event_id}: sin texto")
                )
                continue

            # Generar embedding
            try:
                vec = embed_text(text)
                
                collection.update_one(
                    {'_id': event_id},
                    {'$set': {
                        'embedding': vec,
                        'embedding_model': model_name(),
                        'embedding_updated_at': timezone.now()
                    }}
                )
                
                processed += 1
                    
                if processed % 5 == 0:
                    self.stdout.write(f"✓ Procesados: {processed}/{total_count}")
                    
            except Exception as ex:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error en evento ID {event_id}: {type(ex).__name__}: {str(ex)}")
                )
                skipped += 1

        client.close()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Completado: {processed} embeddings generados, {skipped} omitidos"
            )
        )