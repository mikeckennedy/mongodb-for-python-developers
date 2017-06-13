from nosql.car import Car
from nosql.owner import Owner
from datetime import datetime
import nosql.mongo_setup as mongo_setup


def timed(msg, func):
    t0 = datetime.now()

    func()

    dt = datetime.now() - t0
    print("{} Time: {:,.3f} ms".format(msg, dt.total_seconds() * 1000.0), flush=True)


mongo_setup.init()

print("Time to ask some questions")

timed(
    'How many owners?',
    lambda: Owner.objects().filter().count()
)
timed(
    'How many cars?',
    lambda: Owner.objects().filter().count()
)

timed(
    'Find the 10,000th owner by name?',
    lambda: Owner.objects().order_by('name')[10000:10001][0]
)

owner = Owner.objects().order_by('name')[10000:10001][0]


def find_cars_by_owner(owner_id):
    the_owner = Owner.objects(id=owner_id).first()
    cars = Car.objects().filter(id__in=the_owner.car_ids)
    return list(cars)


timed(
    'How many cars are owned by the 10,000th owner?',
    lambda: find_cars_by_owner(owner.id)
)


def find_owners_by_car(car_id):
    print(car_id)
    owners = Owner.objects(car_ids=car_id)
    return list(owners)


car = Car.objects()[10000:10001][0]
timed(
    'How many owners own the 10,000th car?',
    lambda: find_owners_by_car(car.id)
)

owner50k = Owner.objects()[50000:50001][0]
timed(
    'Find owner 50,000 by name?',
    lambda: Owner.objects(name=owner50k.name).first()
)

timed(
    'Cars with expensive service?',
    lambda: Car.objects(service_history__price__gt=16800).count()
)

timed(
    'Cars with expensive service and spark plugs?',
    lambda: Car.objects(service_history__price__gt=16800,
                        service_history__description='Spark plugs').count()
)

timed(
    'Load cars with expensive service and spark plugs?',
    lambda: list(Car.objects(service_history__price__gt=15000)[:100])
)

timed(
    'Load car name and ids with expensive service and spark plugs?',
    lambda: list(Car.objects(service_history__price__gt=15000)
                 .only('make', 'model', 'id')[:100])
)

timed(
    'Highly rated, high price service events?',
    lambda: Car.objects(service_history__customer_rating=5, service_history__price__gt=16800).count()
)

timed(
    'Low rated, low price service events?',
    lambda: Car.objects(service_history__customer_rating=1, service_history__price__lt=50).count()
)

timed(
    'How many high mileage cars?',
    lambda: Car.objects(mileage__gt=140000).count()
)
