import typing

import bson
import datetime

from nosql.car import Car
from nosql.engine import Engine
from nosql.owner import Owner
from nosql.service_record import ServiceRecord


def create_owner(name: str) -> Owner:
    owner = Owner(name=name)
    owner.save()

    return owner


def create_car(model: str, make: str, year: int,
               horsepower: int, liters: float,
               mpg: float, mileage: int) -> Car:
    engine = Engine(horsepower=horsepower, liters=liters, mpg=mpg)
    car = Car(model=model, make=make, year=year, engine=engine, mileage=mileage)
    car.save()

    return car


def record_visit(customer):
    Owner.objects(name=customer).update_one(inc__number_of_visits=1)


def find_cars_by_make(make) -> Car:
    car = Car.objects(make=make).first()
    return car


def find_owner_by_name(name) -> Owner:
    t0 = datetime.datetime.now()
    owner = Owner.objects(name=name).first()
    dt = datetime.datetime.now() - t0
    print("Owner found in {} ms".format(dt.total_seconds() * 1000))

    return owner


def find_owner_by_id(owner_id) -> Owner:
    owner = Owner.objects(id=owner_id).first()
    return owner


def find_cars_with_bad_service(limit=10) -> typing.List[Car]:
    cars = Car.objects(service_history__customer_rating__lt=4)[:limit]
    return list(cars)


def percent_cars_with_bad_service():
    t0 = datetime.datetime.now()
    bad = Car.objects().filter(service_history__customer_rating__lte=1).count()
    dt = datetime.datetime.now() - t0
    print("bad computed in {} ms, bad: {:,}".format(dt.total_seconds() * 1000, bad))

    all_cars = Car.objects().count()

    percent = 100 * bad / max(all_cars, 1)
    return percent


def find_car_by_id(car_id: bson.ObjectId) -> Car:
    car = Car.objects(id=car_id).first()
    Car.objects().filter(id=car_id).first()
    return car


def add_service_record(car_id, description, price, customer_rating):
    record = ServiceRecord(description=description, price=price, customer_rating=customer_rating)

    res = Car.objects(id=car_id).update_one(push__service_history=record)
    if res != 1:
        raise Exception("No car with id {}".format(car_id))


def add_owner(owner_id, car_id):
    res = Owner.objects(id=owner_id).update_one(add_to_set__car_ids=car_id)
    if res != 1:
        raise Exception("No owner with id {}".format(owner_id))
