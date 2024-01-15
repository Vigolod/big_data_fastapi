import psycopg2
from psycopg2.extensions import connection
from psycopg2.sql import Identifier, SQL


class Database:

    def __init__(self, config):
        self.config = config
        self._vehicles = {}
        self.columns = []
        self.conn = None
        self._vehicles = []
        self.table_name = self.config["BASE"]["table_name"]

    @property
    def vehicles(self):
        return self._vehicles

    def setup(self):
        self._setup_connection()
        self._setup_columns()
        self._get_vehicles()

    def _setup_connection(self):
        self.conn = create_connection(self.config["CONNECTION"])

    def _setup_columns(self):
        table_name = self.config["BASE"]["table_name"]
        self.columns = get_columns(table_name, self.conn)

    def _get_vehicles(self):
        query = SQL("select {column} from {table};").format(
                    column=Identifier(self.columns[0]),
                    table=Identifier(self.table_name)
        )
        with self.conn as conn:
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchall()
        self._vehicles = [v for (v,) in result]


def get_columns(table_name: str, conn: connection):
    query = "select column_name from information_schema.columns \
            where table_schema='public' \
            and table_name=%s;"
    with conn:
        cur = conn.cursor()
        cur.execute(query, (table_name, ))
        result = cur.fetchall()
    columns = [col for (col,) in result]
    return columns


def create_connection(conn_config):
    conn = psycopg2.connect(
        database=conn_config["database"],
        host=conn_config["host"],
        user=conn_config["user"],
        password=conn_config["password"],
        port=conn_config["port"]
    )
    return conn
