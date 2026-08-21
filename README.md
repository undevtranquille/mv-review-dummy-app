# Movie Review

Application de gestion d'avis sur des films.
Backend : Django + Django REST Framework (SQLite).
Frontend : Vue 3 + Vue Router + Pinia + Vuetify + Axios.
Les deux services tournent dans des containers Docker, lancés via un seul `docker-compose.yml`.

## Prérequis

- Docker et Docker Compose installés (Docker Desktop suffit).

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
- **Mot de passe** : `admin1234` (par défaut, configurable via la variable d'environnement `DJANGO_ADMIN_PASSWORD` dans `docker-compose.yml`)

## Arrêter le projet

```bash
docker compose down
```

Pour repartir d'une base de données vide (efface aussi les données saisies manuellement) :

```bash
docker compose down -v
docker compose up --build
```

## Endpoints API principaux

| Méthode | URL | Description |
|---|---|---|
| GET | `/api/movies/?page=N` | Liste paginée des films (5 par page), avec note moyenne |
| GET | `/api/movies/{id}/` | Détail d'un film : description, acteurs, avis, note moyenne |
| PATCH | `/api/movies/{id}/` | Édition partielle (description et/ou acteurs) |
| POST | `/api/reviews/` | Ajout d'un avis (`{ "movie": id, "grade": 1-5 }`) |
| GET / POST | `/api/actors/` | Liste des acteurs / création d'un nouvel acteur |

## Choix techniques et arbitrages

- **Base de données** : SQLite, choisi pour sa simplicité vu le périmètre de l'exercice (pas de séparation dev/prod). En production, Postgres serait préférable.
- **Note moyenne** : calculée à la volée côté backend (agrégation SQL `Avg`), jamais stockée en base, pour éviter tout risque de désynchronisation.
- **Pagination** : gérée nativement par Django REST Framework (`PageNumberPagination`, 5 éléments par page), conformément à l'énoncé.
- **Pas d'authentification** : conforme à l'énoncé, tout le monde peut éditer un film ou ajouter un avis.
- **Sécurité** : `ALLOWED_HOSTS` restreint à `localhost`/`127.0.0.1`, le mot de passe admin est configurable via variable d'environnement plutôt qu'en dur dans le code. Ces réglages restent adaptés à un contexte d'exercice local, pas à une exposition en production.