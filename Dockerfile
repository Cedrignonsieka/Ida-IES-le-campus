# Utiliser une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Render (10000 par convention)
EXPOSE 10000

# Lancer l'application avec Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:10000"]
