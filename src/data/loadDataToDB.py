# Global moduls
import pandas as pd
from os import path, remove
# from sqlalchemy.types import INTEGER, DateTime, Float

# Interior imports
from .createDB import MyDatabase, db_backend, db_name, AIRLY_DATA, AIRLY_LOCATIONS

dbms = MyDatabase(db_backend, db_name)


class airly():
    def __init__(self):
        self._data_path = path.join('data', 'raw', 'smogathon_airly')

    def read_measurements(self):
        measurements = pd.read_csv(path.join(self._data_path, 'measurements.csv'))
        measurements.to_parquet(
            path.join('data', 'interim', 'measurements.pq'), compression=None)

    def save_meaurements(self):
        data_path = path.join('data', 'interim', 'measurements.pq')
        data = pd.read_parquet(data_path)
        # Loading to DB
        # dtypes = {'id': INTEGER(), 'time': DateTime(), 'pm10': Float(), 'pm25': Float(
        # ), 'temperature': Float(), 'humidity': Float(), 'pressure': Float()}
        data.to_sql(AIRLY_DATA, dbms.db_engine, if_exists='append', index=False)
        remove(data_path)

    def read_locations(self):
        data = pd.read_csv(path.join(self._data_path, 'installations.csv'))
        data.to_parquet(path.join('data', 'interim', 'installations.pq'), compression=None)

    def save_locations(self):
        data_path = path.join('data', 'interim', 'installations.pq')
        data = pd.read_parquet(data_path)
        data.to_sql(AIRLY_LOCATIONS, dbms.db_engine, if_exists='append', index=False)
        remove(data_path)


def main():
    al = airly()
    al.read_measurements()
    al.save_meaurements()
    al.read_locations()
    al.save_locations()


if __name__ == "__main__":
    main()
