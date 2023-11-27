from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from main_app.managers import DirectorManager


class Director(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    birth_date = models.DateField(
        default='1900-01-01'
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )

    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    objects = DirectorManager()

class Actor(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    birth_date = models.DateField(
        default='1900-01-01'
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )

    is_awarded=models.BooleanField(
        default=False
    )

    last_updated = models.DateTimeField(
        auto_now=True
    )

class Movie(models.Model):
    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5)
        ]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        blank=True,
        null=True,
    )

    GENRE_CHOISES = (
        ("Action", "Action"),
        ("Comedy", "Comedy"),
        ("Drama", "Drama"),
        ("Other", "Other")
    )

    genre = models.CharField(
        max_length=6,
        choices=GENRE_CHOISES,
        default="Other"

    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[
            MinValueValidator(0), MaxValueValidator(10)
        ]
    )

    is_classic = models.BooleanField(
        default=False
    )

    is_awarded = models.BooleanField(
        default=False
    )

    last_updated = models.DateTimeField(
        auto_now=True
    )

    director = models.ForeignKey(
        to="Director",
        on_delete=models.CASCADE,
        related_name="director_movies"
    )

    starring_actor = models.ForeignKey(
        to='Actor',
        on_delete=models.SET_NULL,
        null=True,
        related_name="actor_movies"
    )

    actors = models.ManyToManyField(
        to='Actor',
        related_name="all_actor_movies"
    )
