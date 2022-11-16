# Test Frubana

## Setup database
There is an instance of postgres db wit no data using the `docker-compose.yml`

```bash
docker compose up -d
```

In order to load the dataset follow these steps:

```bash
docker compose up -d
docker compose exec postgres bash
psql -U demo -W < /data/demo-small-en-20170815.sql
```

You can find db, user and password in `docker-compose.yml` file.

## Exercises
In the main dir there is jupyter notebook `test_frubana.ipynb` that contains exercises from 4 through 7.

Exercise 8 is a separate command `search_flights.py`.

## Search Flights
In order to execute `search_flights.py` command:

1. Install the requirements
```bash
pip install -r requirements.txt 
```

2. Execute command
```bash
python search_flights.py --airport KHV
```