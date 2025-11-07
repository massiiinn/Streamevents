from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from faker import Faker
import random
import unicodedata

User = get_user_model()

class Command(BaseCommand):
    """Comandament de Django per generar usuaris de prova a StreamEvents."""

    help = "Genera usuaris de prova per a StreamEvents amb dades realistes i coherents."

    def add_arguments(self, parser):
        """Afegeix els arguments opcionals del comandament."""
        parser.add_argument('--users', type=int, default=10, help='Nombre d’usuaris a crear')
        parser.add_argument('--clear', action='store_true', help='Elimina usuaris existents (excepte superusers)')
        parser.add_argument('--with-follows', action='store_true', help='Crea relacions de seguiment aleatòries')

    def handle(self, *args, **options):
        """Executa el comandament principal i gestiona la creació d’usuaris i grups."""
        num_users = options['users']
        clear = options['clear']
        with_follows = options['with_follows']

        fake = Faker('es_ES')
        if clear:
            users_to_delete = list(User.objects.filter(is_superuser=False))
            deleted = len(users_to_delete)
            for u in users_to_delete:
                u.delete()
            self.stdout.write(self.style.WARNING(f'🧹 Eliminats {deleted} usuaris existents.'))

        with transaction.atomic():
            groups = self.create_groups()
            self.create_admin(groups['Organitzadors'])
            created = self.create_fake_users(num_users, groups, fake)
            if with_follows:
                self.create_follows()
        
        self.stdout.write(self.style.SUCCESS(f'✅ {created} usuaris de prova creats correctament.'))

    def create_groups(self):
        """Crea els grups principals: Organitzadors, Participants i Moderadors."""
        group_names = ['Organitzadors', 'Participants', 'Moderadors']
        groups = {}
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            groups[name] = group
            if created:
                self.stdout.write(f'🏷️ Grup creat: {name}')
        return groups

    def create_admin(self, org_group):
        """Crea el superusuari administrador si no existeix."""
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@streamevents.com',
                'display_name': '🔧 Administrador',
                'bio': 'Superusuari del sistema StreamEvents',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            admin.groups.add(org_group)
            self.stdout.write(self.style.SUCCESS('👑 Superusuari "admin" creat correctament.'))

    def create_fake_users(self, num_users, groups, fake):
        """Genera usuaris de prova amb dades realistes mitjançant Faker."""
        created_count = 0
        for i in range(num_users):
            first = fake.first_name()
            last = fake.last_name()
            username_base = f"{self.clean_username(first)}.{self.clean_username(last)}{i+1}"
            email = f"{username_base}@streamevents.com"

            if (i + 1) % 5 == 0:
                role = 'Organitzadors'
                emoji = '🎯'
            elif (i + 1) % 3 == 0:
                role = 'Moderadors'
                emoji = '🛡️'
            else:
                role = 'Participants'
                emoji = ''

            user, created = User.objects.get_or_create(
                username=username_base,
                defaults={
                    'email': email,
                    'first_name': first,
                    'last_name': last,
                    'display_name': f"{emoji} {first} {last}".strip(),
                    'bio': f"{role[:-1]} d’esdeveniments en streaming.",
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password123')
                user.groups.add(groups[role])
                user.save()
                created_count += 1
                self.stdout.write(f'👤 {emoji} Usuari creat: {user.username} → {role}')
        return created_count

    def create_follows(self):
        """Crea relacions de seguiment aleatòries si existeix el model Follow."""
        try:
            from users.models import Follow
            users = list(User.objects.exclude(is_superuser=True))
            count = 0
            for user in users:
                followed = random.sample(users, random.randint(0, 3))
                for f in followed:
                    if f != user:
                        Follow.objects.get_or_create(follower=user, followed=f)
                        count += 1
            self.stdout.write(self.style.SUCCESS(f'🔗 {count} relacions de seguiment creades.'))
        except Exception:
            self.stdout.write(self.style.WARNING('⚠️ El model Follow no existeix, s’ometen les relacions.'))

    def clean_username(self, text):
        """Elimina accents i caràcters especials dels noms d’usuari."""
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
        return text.lower()
