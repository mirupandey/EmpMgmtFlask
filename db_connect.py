from sqlalchemy import create_engine, MetaData

from db_creation import create_tables_and_insert_dummy_data


class DatabaseConnection:
    def __init__(self):
        self._db_connection = None
        self._metadata = None
        self._engine = None
        self._create_db()

    def __del__(self):
        self.close_connection()

    def _create_db(self) -> None:
        meta, conn, engine = self._create_connection()
        if len(engine.table_names()) == 0:
            create_tables_and_insert_dummy_data(meta, engine)

    def _create_connection(self) -> tuple:
        self._engine = create_engine('sqlite:///EmpMgmt.db')
        self._metadata = MetaData()
        self._metadata.bind = self._engine
        self._db_connection = self._engine.connect()
        return self._metadata, self._db_connection, self._engine

    def get_connection(self):
        if self._db_connection is None:
            self._metadata, self._db_connection, self._engine = self._create_connection()
        return self._metadata, self._db_connection

    def close_connection(self):
        if self._db_connection:
            self._db_connection.close()


database_connection = DatabaseConnection()
db_connection = database_connection.get_connection()[1]
meta = database_connection.get_connection()[0]

'''def establish_connection():
    try:

        is_connect = True

    # If connection is not successful
    except():
        print("Can't connect to database")
        return 0

    # If Connection Is Successful
    print("Connected")
    return db_connection


conn = establish_connection()
'''