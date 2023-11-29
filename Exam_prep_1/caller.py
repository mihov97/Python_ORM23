import os
import django
from django.db.models import Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie


# Create and run your queries within functions
def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    all_directors = []

    if search_name is None:
        all_directors = Director.objects.filter(
            nationality__icontains=search_nationality
        ).order_by("full_name")

    elif search_nationality is None:
        all_directors = Director.objects.filter(
            full_name__icontains=search_name
        ).order_by("full_name")

    else:
        all_directors = Director.objects.filter(
            full_name__icontains=search_name,
            nationality__icontains=search_nationality
        ).order_by('full_name')

    if not all_directors:
        return ""

    final_result = []
    
    for director in all_directors:
        final_result.append(f"Director: {director.full_name}, nationality: {director.nationality}, "
                            f"experience: {director.years_of_experience}")

    return '\n'.join(final_result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return f"Top Director: {top_director.full_name}, movies: {top_director.total_movies}."


def get_top_actor():
    top_actor = Actor.objects.annotate(
        total_starring_movies=Count('actor_movies'),
        average_rating_movies=Avg('actor_movies__rating'))\
        .order_by('-total_starring_movies', 'full_name')\
        .first()

    if not top_actor or not top_actor.total_starring_movies:
        return ""

    top_actor_movies = ', '.join([m.title for m in top_actor.actor_movies.all() if m])

    return f"Top Actor: {top_actor.full_name}, starring in movies: {top_actor_movies}, movies average rating: {top_actor.average_rating_movies:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.prefetch_related('all_actor_movies')\
        .annotate(total_movies=Count('all_actor_movies'))\
        .order_by('-total_movies', 'full_name')[:3]

    if not actors or not actors[0].total_movies:
        return ""

    final_result = []
    for actor in actors:
        final_result.append(f"{actor.full_name}, participated in {actor.total_movies} movies")

    return '\n'.join(final_result)


def get_top_rated_awarded_movie():
    top_rated_movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if not top_rated_movie:
        return ""

    starring_actor = top_rated_movie.starring_actor.full_name if top_rated_movie.starring_actor else 'N/A'
    participating_actors = ', '.join([a.full_name for a in top_rated_movie.actors.order_by('full_name')])

    return f"Top rated awarded movie: {top_rated_movie.title}, " \
           f"rating: {float(top_rated_movie.rating):.1f}. " \
           f"Starring actor: {starring_actor}. Cast: {participating_actors}."


def increase_rating():
    movies = Movie.objects.filter(
        is_classic=True,
        rating__lt=10
    )

    if not movies:
        return f"No ratings increased."

    updated_movies = movies.update(rating=F('rating') + 0.1)

    return f"Rating increased for {updated_movies} movies."










