from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, INTEGER, DateTime, Float, ForeignKey
import configparser
from os import path

# Importing config
config = configparser.ConfigParser()
conf_path = path.join('config', 'conf.ini')
try:
    config.read(conf_path)
except FileNotFoundError:
    print("No config file")
except Exception as e:
    print('Error when reading the config file: {}'.format(e))


# Global variables
db_backend = config['DATABASE']['db_backend']
db_name = config['DATABASE']['db_name']


# Table Names
AIRLY_DATA = 'airly_raw_data'
AIRLY_LOCATIONS = 'airly_locs'


class MyDatabase:
    # If another backend will be needed we can add it below:
    DB_ENGINE = {
        'sqlite': 'sqlite:///{DB}'
    }

    db_engine = None

    def __init__(self, dbtype, dbname, username='', password='', port=0000):
        """[summary]

        Parameters
        ----------
        dbtype : str
            Type of database, possible choices: [SQLITE]
        username : str, optional
            NOT USED, by default ''
        password : str, optional
            NOT USED, by default ''
        dbname : str
            Name of the database, by default ''
        port : int, optional
            NOT USED, by default 0000
        """
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print('DBType is not found in DB_ENGINE')

    def create_db_tables(self):
        metadata = MetaData()
        stations = Table(AIRLY_LOCATIONS, metadata,
                         Column('id', INTEGER, primary_key=True),
                        Column('lat', Float),
                        Column('lng', Float),
                        Column('city', String),
                        Column('street', String),
                         Column('elevation', Float))

        airly_data = Table(AIRLY_DATA, metadata,
                           Column('id', INTEGER,
                                  ForeignKey(AIRLY_LOCATIONS+'.id')),
                        Column('time', DateTime, nullable=True),
                        Column('pm10', Float, nullable=True), 
                        Column('pm25', Float, nullable=True),
                        Column('temperature', Float, nullable=True),
                        Column('humidity', Float, nullable=True),
                        Column('pressure', Float, nullable=True))

        try:
            metadata.create_all(self.db_engine)
            print('Tables created')
        except Exception as e:
            print('Error occured during Table creation!')
            print(e)

    def execute_query(self, query=''):
        if query == '':
            return
        print(query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)


def main():
    dbms = MyDatabase(db_backend, db_name)
    dbms.create_db_tables()


if __name__ == '__main__':
    main()
