## Prérequis

- Docker et Docker Compose installés.

## Lancer le projet

Depuis la racine du repo :

```bash
docker compose up --build
```

Au premier démarrage, le backend applique automatiquement les migrations et remplit la base avec des données de démonstration (films, acteurs, avis). Ce seed est idempotent : il ne s'exécute que si la base est vide, donc relancer `docker compose up` plusieurs fois ne duplique rien.

Aucune autre commande n'est nécessaire.

## Accès

| Service | URL |
|---|---|
| Frontend (application) | http://localhost:5173 |
| Backend API | http://localhost:8000/api/ |
| Admin Django | http://localhost:8000/admin/ |

## Identifiants admin

Un superutilisateur est créé automatiquement au premier démarrage :

- **Utilisateur** : `admin`
- **Mot de passe** : `admin` (par défaut, configurable via la variable d'environnement `DJANGO_ADMIN_PASSWORD` dans `docker-compose.yml`)