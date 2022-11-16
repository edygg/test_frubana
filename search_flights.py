import click
import sqlalchemy
import pandas as pd
import numpy as np
from collections import deque


class AirportRouter:
    routes: pd.DataFrame

    def __init__(self):
        # TODO Solicitar esta URI
        db_url = 'postgresql+psycopg2://demo:K2tinVstcd4WY5@localhost:5432/demo'
        engine = sqlalchemy.create_engine(db_url)

        with engine.connect().execution_options(autocommit=True) as conn:
            load_routes_query = f"""
            SELECT flight_no, departure_airport, arrival_airport, arrival_city FROM routes;
            """
            self.routes = pd.read_sql(load_routes_query, con=conn)

    @classmethod
    def get_service(cls):
        if not hasattr(cls, "instance"):
            cls.instance = AirportRouter()

        return cls.instance

    def airport_code_exists(self, airport_code):
        search_result = (airport_code in self.routes["departure_airport"].values) or \
                      (airport_code in self.routes["arrival_airport"].values)

        return search_result

    def cities_reached(self, airport_code):
        list_cities_reached = np.array([], dtype=str)
        airports_reached = np.array([], dtype=str)
        airport_stack = deque()
        airport_stack.append(airport_code)  # Push initial airport

        while len(airport_stack) > 0:
            current_airport = airport_stack.pop()

            if current_airport not in airports_reached:
                airports_reached = np.append(airports_reached, current_airport)

            current_routes = self.routes[self.routes["departure_airport"] == current_airport]

            for index, arrival_airport in current_routes["arrival_airport"].items():
                if arrival_airport not in airports_reached:
                    airport_stack.append(arrival_airport)

                current_city = current_routes["arrival_city"][index]

                if current_city not in list_cities_reached:
                    list_cities_reached = np.append(list_cities_reached, current_city)

        return list_cities_reached


@click.command()
@click.option("--airport", prompt="Airport Code", help="Airport code ie KHV")
def search_flights(airport):
    starting_airport = str(airport).upper()
    airport_router_service = AirportRouter.get_service()

    if not airport_router_service.airport_code_exists(starting_airport):
        click.echo(f"Airport `{starting_airport}` does not exists.")
        return

    cities_reach = airport_router_service.cities_reached(starting_airport)

    if cities_reach.size < 1:
        click.echo("There is no cities.")
        return

    click.echo(f"List of cities ({cities_reach.size} cities):\n\n")
    for city in cities_reach:
        click.echo(city)


if __name__ == '__main__':
    search_flights()