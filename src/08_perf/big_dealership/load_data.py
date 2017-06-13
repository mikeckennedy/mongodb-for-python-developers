import nosql.mongo_setup as mongo_setup
import services.car_service as car_service
from nosql.car import Car
from nosql.engine import Engine
from nosql.owner import Owner

from datetime import datetime
import random
from faker import Faker

from nosql.service_record import ServiceRecord


def main():
    # large data DB example
    car_count = 250_000
    owner_count = 100_000

    # simple DB example
    # car_count = 200
    # owner_count = 100

    mongo_setup.init()
    clear_db()

    t0 = datetime.now()

    fake = create_faker_and_seed()
    owners = create_owners(fake, count=owner_count)
    print("Created {:,.0f} owners".format(len(owners)))
    cars = create_cars(count=car_count)
    print("Created {:,.0f} cars".format(len(cars)))
    if cars and owners:
        add_cars_to_owners(owners, cars)
        create_service_records(cars, fake)

    dt = datetime.now() - t0
    print("Done in {} sec".format(dt.total_seconds()))


models = [
    'Ferrari 488 GTB',
    'Ferrari 360 modena',
    'F430',
    '599 GTB Fiorano',
    '458 Italia',
    'LaFerrari',
    'Testarossa',
    'F12 Berlinetta',
    '308 GTB/GTS',
    'F355',
    'California',
    '575M Maranello',
    'F50',
    'F40',
    'Enzo Ferrari',
]

service_operations = [
    ('Oil change', 200),
    ('New tires', 1000),
    ('New engine', 15000),
    ('Body repair', 4000),
    ('New seat', 5000),
    ('Tune up', 1500),
    ('Air filter', 100),
    ('Flat tire', 200),
]


def create_faker_and_seed():
    fake = Faker()
    fake.seed(42)
    random.seed(42)
    return fake


def clear_db():
    Car.drop_collection()
    Owner.drop_collection()


def create_owners(fake, count=100):
    current_owner_count = Owner.objects().count()
    if current_owner_count >= count:
        print("There are currently {:,} owners. Skipping create.")
        return []

    count = count - current_owner_count

    datetime_start = datetime(year=2000, month=1, day=1)
    datetime_end = datetime(year=datetime.now().year, month=1, day=1)

    owners = []
    print("Building owners")
    for _ in range(0, count):
        owner = Owner()
        owner.name = fake.name()
        owner.created = fake.date_time_between_dates(datetime_start=datetime_start,
                                                     datetime_end=datetime_end,
                                                     tzinfo=None)
        owners.append(owner)

    print("Saving owners")
    Owner.objects().insert(owners, load_bulk=True)

    return list(Owner.objects())


def create_cars(count=200):
    current_car_count = Car.objects().count()
    if current_car_count >= count:
        print("There are currently {:,} cars. Skipping create.")
        return []

    count = count - current_car_count

    hp_factor = 660
    mpg_factor = 21
    liters_factor = 4

    cars = []
    print("Building cars...")
    for _ in range(0, count):
        model = random.choice(models)
        make = 'Ferrari'
        year = random.randint(1985, datetime.now().year)
        mileage = random.randint(0, 150000)

        mpg = int((mpg_factor + mpg_factor * random.random() / 4) * 10) / 10.0
        horsepower = int(hp_factor + hp_factor * random.random() / 2)
        liters = int((liters_factor + liters_factor * random.random() / 2) * 100) / 100.0

        engine = Engine(horsepower=horsepower, liters=liters, mpg=mpg)
        car = Car(model=model, make=make, year=year, engine=engine, mileage=mileage)
        cars.append(car)

    print("Saving cars...")
    Car.objects().insert(cars)

    return list(Car.objects())


def add_cars_to_owners(owners: list, cars: list):
    for o in owners:
        counter = random.randint(0, 5)
        for _ in range(0, counter):
            car = random.choice(cars)
            car_service.add_owner(o.id, car.id)


def create_service_records(cars, fake):
    datetime_start = datetime(year=2000, month=1, day=1)
    datetime_end = datetime(year=datetime.now().year, month=1, day=1)

    for car in cars:
        counter = random.randint(0, 10)
        is_positive = random.randint(0, 1) == 1
        for _ in range(0, counter):
            s = random.choice(service_operations)
            sr = ServiceRecord()
            sr.description = s[0]
            sr.date = fake.date_time_between_dates(datetime_start=datetime_start,
                                                   datetime_end=datetime_end,
                                                   tzinfo=None)
            sr.price = int(s[1] + (random.random() - .5) * s[1] / 4)
            if is_positive:
                sr.customer_rating = random.randint(4, 5)
            else:
                sr.customer_rating = random.randint(1, 3)
            car.service_history.append(sr)
        car.save()


if __name__ == '__main__':
    main()
