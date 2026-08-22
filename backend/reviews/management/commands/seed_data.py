from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reviews.models import Actor, Movie, Review

import os

ADMIN_PASSWORD = os.environ.get("DJANGO_ADMIN_PASSWORD")

class Command(BaseCommand):
    help = "Seed the database with dummy data for demo purposes."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", ADMIN_PASSWORD)
            self.stdout.write("Superuser 'admin' created.")
        
        if Movie.objects.exists():
            self.stdout.write("Data already present, skipping seed.")
            return

        actors = [
            Actor.objects.create(first_name="aaaaa", last_name="AAAAA"),
            Actor.objects.create(first_name="bbbbb", last_name="BBBBB"),
            Actor.objects.create(first_name="ccccc", last_name="CCCCC"),
            Actor.objects.create(first_name="ddddd", last_name="DDDDD"),
            Actor.objects.create(first_name="eeeee", last_name="EEEEE"),
        ]

        for i in range(1, 13):
            movie = Movie.objects.create(
                title=f"Movie {i}",
                description="d" * 5 * i,
            )
            movie.actors.set(actors[: (i % 5) + 1])

            for grade in [1, 2, 3, 4, 5][: (i % 5) + 1]:
                Review.objects.create(movie=movie, grade=grade)

        self.stdout.write(self.style.SUCCESS("Database seeded."))