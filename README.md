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
│── streamevents/      # Configuració principal del projecte (settings.py, urls.py...)
│── users/             # App amb CustomUser
│── templates/         # Plantilles globals (base.html, layouts, etc.)
│── static/            # Arxius estàtics (css/, js/, img/)
│── media/             # Fitxers pujats per usuaris (NO a Git)
│── fixtures/          # (opc.) JSON amb dades d’exemple
│── seeds/             # (opc.) Scripts per omplir dades
│── requirements.txt   # Dependències del projecte
│── .env               # Variables d’entorn (privat)
│── env.example        # Exemple públic de .env
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

---

## 👤 Superusuari

---

## 🗃️ Migrar a MongoDB (opcional futur)

---

## 🛠️ Comandes útils

---

## 💾 Fixtures (exemple)

---

## 🌱 Seeds (exemple d'script)
