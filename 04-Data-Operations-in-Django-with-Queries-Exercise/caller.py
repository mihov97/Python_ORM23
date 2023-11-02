import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom

def create_pet(name: str, species: str):
    Pet.objects.create(
        name=name,
        species=species
    )

    return f"{name} is a very cute {species}!"

def create_artifact(name:str, origin:str, age:int, description:str, is_magical:bool):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
)
    return f"The artifact {name} is {age} years old!"

def delete_all_artifacts():
    Artifact.objects.all().delete()

def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')

    return '\n'.join(str(l) for l in locations)


def new_capital() -> None:
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals() :
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location() -> None:
    Location.objects.first().delete()

def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        percent = sum(int(el) for el in str(car.year)) / 100
        discount = float(car.price) * percent
        car.price_with_discount = float(car.price) - discount
        car.save()

def get_recent_cars():
    return Car.objects.filter(year__gte=2020).values('model', 'price_with_discount')

def delete_last_car():
    Car.objects.last().delete()

def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(str(el) for el in unfinished_tasks)

def complete_odd_tasks():
    tasks = Task.objects.all()

    for t in tasks:
        if t.id % 2 != 0:
            t.is_finished = True
            t.save()

def encode_and_replace(text: str, task_title: str):
    tasks_with_title = Task.objects.filter(title=task_title)
    dec_text = ''.join(chr(ord(el) - 3) for el in text)

    for t in tasks_with_title:
        t.description = dec_text
        t.save()

def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe")
    deluxe_rooms = [el for el in deluxe_rooms if el.id % 2 == 0]
    return '\n'.join([f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!" for r in deluxe_rooms])


def increase_room_capacity():
    all_rooms = HotelRoom.objects.all().order_by('id')

    for el in range(len(all_rooms)):
        room = all_rooms[el]

        if not room.is_reserved:
            continue

        if el == 0:
            room.capacity += room.id
        else:
            room.capacity += HotelRoom.objects.get(id=room.id - 1).capacity

        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.all().first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.all().last()

    if last_room.is_reserved:
        last_room.delete()