# StreamEvents  

Aplicació Django per gestionar esdeveniments i usuaris
(extensible): base educativa amb bones pràctiques
(entorns, estructura, separació de templates/static,
etc.). Opcionalment es pot integrar MongoDB (via djongo)
més endavant.

---

## 🎯 Objectius  

- Practicar un projecte Django modular.  
- Treballar amb un usuari personalitzat (app users).  
- Organitzar templates, estàtics i media correctament.  
- Introduir fitxers d’entorn (.env) i bones pràctiques amb Git.  
- Preparar el terreny per a futures funcionalitats (API, auth avançada, etc.).  

---

## 🧱 Stack Principal  

---

## 📂 Estructura Simplificada  

streamevents/     
│── manage.py
│── streamevents/     
│── users/            
│── templates/        
│── static/           
│── media/            
│── fixtures/          
│── seeds/            
│── requirements.txt  
│── .env               
│── env.example        
│── README.md
│── .gitignore

---

## ✅ Requisits previs  

- **Python 3.11+** instal·lat  
- **Pip** i **venv** disponibles  
- **Git** per clonar i versionar el projecte  

---

## 🚀 Instal·lació ràpida  

---

## 🔐 Variables d'entorn (env.example)

SECRET_KEY=canvia-aixo
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
MONGO_URL=mongodb://localhost:27017
DB_NAME=streamevents_db

---

## 👤 Superusuari

python manage.py createsuperuser # Serveix per crear superusuari per accedir al admin de Django

---

## 🗃️ Migrar a MongoDB (opcional futur)

---

## 🛠️ Comandes útils
```bash
# Activar entorn virtual
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

# Executar servidor
python manage.py runserver

# Migracions
python manage.py makemigrations
python manage.py migrate

# Crear superusuari
python manage.py createsuperuser

# Omplir dades amb fixtures
python manage.py loaddata fixtures/nom_fitxer.json
```

---

## 💾 Fixtures (exemple)

- Carregar fixtures
```bash
# Primer carregar grups
python3 manage.py loaddata users/fixtures/01_groups.json

# Després carregar usuaris
python3 manage.py loaddata users/fixtures/02_users.json
```
- Verificació
```bash
# Comprovar grups
python3 manage.py shell -c "from django.contrib.auth.models import Group; print(Group.objects.all())"

# Comprovar usuaris
python3 manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); print(User.objects.all())"
```
---

## 🌱 Seeds (exemple d'script)
```bash
# Crear 10 usuaris de prova per defecte
python3 manage.py seed_users

# Crear 25 usuaris eliminant els existents
python3 manage.py seed_users --users 25 --clear
```
