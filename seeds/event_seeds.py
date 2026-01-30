"""
Seeds per crear esdeveniments de prova.
Executa: python3 manage.py shell -c "from seeds.event_seeds import create_sample_events; create_sample_events()"
"""

from django.utils import timezone
from datetime import timedelta
from events.models import Event
from users.models import CustomUser


def create_sample_events():
    """Crea 10 esdeveniments variats per a proves de cerca semàntica"""
    
    # Agafem el primer usuari o mostrem error
    creator = CustomUser.objects.first()
    if not creator:
        print("⚠️  No hi ha usuaris. Crea'n un primer amb: python3 manage.py createsuperuser")
        return
    
    print(f"✅ Creant esdeveniments per l'usuari: {creator.username}\n")
    
    # Llista d'esdeveniments amb varietat de categories i temes
    events_data = [
        {
            "title": "Festival de Jazz a la Plaça",
            "description": "Gran festival de jazz amb artistes nacionals i internacionals. Gaudeix d'una tarda de música en directe amb els millors músics de jazz del moment.",
            "category": "music",
            "tags": "jazz, música en viu, festival, Barcelona",
            "days_ahead": 5,
        },
        {
            "title": "Torneig de FIFA 2024",
            "description": "Competició d'eSports de FIFA amb premis en metàl·lic. Inscripcions obertes per a jugadors de tots els nivells. Gran premi final de 1000€.",
            "category": "gaming",
            "tags": "fifa, eSports, torneig, videojocs, competició",
            "days_ahead": 10,
        },
        {
            "title": "Xerrada sobre Intel·ligència Artificial",
            "description": "Ponència sobre les últimes tendències en IA i machine learning. Experts del sector compartiran els seus coneixements sobre LLMs i models generatius.",
            "category": "technology",
            "tags": "IA, tecnologia, machine learning, innovació",
            "days_ahead": 3,
        },
        {
            "title": "Partit de Bàsquet Lliga ACB",
            "description": "Emocionant partit de la lliga ACB al Palau Blaugrana. Vine a animar el teu equip en aquest partit decisiu per la classificació.",
            "category": "sports",
            "tags": "bàsquet, esports, ACB, competició",
            "days_ahead": 7,
        },
        {
            "title": "Curs de Python per a Principiants",
            "description": "Aprèn les bases de programació amb Python en aquest curs intensiu de cap de setmana. Inclou exercicis pràctics i projecte final.",
            "category": "education",
            "tags": "python, programació, curs, formació, codi",
            "days_ahead": 12,
        },
        {
            "title": "Concert de Música Electrònica",
            "description": "Nit de música electrònica amb els millors DJs de la escena underground. Techno, house i més en una sala espectacular.",
            "category": "music",
            "tags": "electrònica, DJ, techno, festa, música",
            "days_ahead": 2,
        },
        {
            "title": "Marató de Speedrunning de Mario",
            "description": "Streamers competeixen per acabar Super Mario Bros el més ràpid possible. Veure les millors tècniques i rutes de speedrun.",
            "category": "gaming",
            "tags": "speedrun, mario, retro, streaming, videojocs",
            "days_ahead": 8,
        },
        {
            "title": "Taller de Pintura i Art Contemporani",
            "description": "Sessions creatives on aprendràs tècniques de pintura moderna. Material inclòs. No calen coneixements previs.",
            "category": "art",
            "tags": "pintura, art, taller, creativitat",
            "days_ahead": 15,
        },
        {
            "title": "Debat sobre Política Digital",
            "description": "Col·loqui sobre privacitat, drets digitals i regulació de tecnologies. Experts en dret i tecnologia debatran sobre el futur digital.",
            "category": "talk",
            "tags": "debat, política, digital, privacitat, drets",
            "days_ahead": 20,
        },
        {
            "title": "Nit de Cinema: Clàssics de Ciència-Ficció",
            "description": "Projecció de pel·lícules clàssiques de sci-fi: Blade Runner, Matrix i més. Inclou col·loqui posterior amb cinèfils.",
            "category": "entertainment",
            "tags": "cinema, pel·lícules, sci-fi, entreteniment",
            "days_ahead": 6,
        },
    ]
    
    # Creem els esdeveniments
    created_count = 0
    for event_data in events_data:
        # Calculem la data futura
        scheduled_date = timezone.now() + timedelta(days=event_data["days_ahead"])
        
        # Creem l'esdeveniment
        event = Event.objects.create(
            title=event_data["title"],
            description=event_data["description"],
            category=event_data["category"],
            tags=event_data["tags"],
            scheduled_date=scheduled_date,
            creator=creator,
            status='scheduled',
            max_viewers=100,
        )
        
        created_count += 1
        print(f"✅ {event.title} ({event.category}) - {scheduled_date.strftime('%d/%m/%Y')}")
    
    print(f"\n🎉 Total esdeveniments creats: {created_count}")
    print(f"\n⚡ Ara executa: python3 manage.py backfill_event_embeddings")


# Per executar directament
if __name__ == "__main__":
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    create_sample_events()