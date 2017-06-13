from nosql import mongo_setup
from nosql.car import Car
from nosql.owner import Owner


def main():
    mongo_setup.init()

    print("Computing stats, this WILL take awhile...", flush=True)

    cars = list(Car.objects())
    print("There are {:,} cars.".format(len(cars)))

    owners = list(Owner.objects())
    print("There are {:,} owners.".format(len(owners)))
    owned_cars = sum((len(o.car_ids) for o in owners))
    print("Each owner owns an average of {:.2f} cars.".format(owned_cars / len(owners)))

    service_histories = sum((len(c.service_history) for c in cars))
    print("There are {:,} service histories.".format(service_histories))
    print("Each car has an average of {:.2f} service records.".format(service_histories / len(cars)))


main()
