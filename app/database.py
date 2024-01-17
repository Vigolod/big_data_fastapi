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

    def _fetchone(self, query, values=None):
        with self.conn as conn:
            cur = conn.cursor()
            cur.execute(query, values)
            result = cur.fetchone()
        return result

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

    def get_vehicle(self, vehicle):
        query = SQL("select * from {table} where {column} = %s;").format(
            column=Identifier(self.columns[0]),
            table=Identifier(self.table_name)
        )
        return self._fetchone(query, (vehicle,))
    
    def _get_extremums(self, col):
        min_query = SQL("select min({column}) from {table};").format(
            column=Identifier(col),
            table=Identifier(self.table_name)
        )

        max_query = SQL("select max({column}) from {table};").format(
            column=Identifier(col),
            table=Identifier(self.table_name)
        )

        min_ = self._fetchone(min_query)[0]
        max_ = self._fetchone(max_query)[0]

        return min_, max_
    
    def _get_vehicle_with_condition(self, col, value):
        query = SQL("select {veh_column} from {table} where {column}=%s").format(
            veh_column=Identifier(self.columns[0]),
            table=Identifier(self.table_name),
            column=Identifier(col)
        )
        result = self._fetchone(query, (value,))[0]
        return result

    def _get_extremum_vehicles_for_col(self, col):
        min_, max_ = self._get_extremums(col)
        min_vehicle = self._get_vehicle_with_condition(col, min_)
        max_vehicle = self._get_vehicle_with_condition(col, max_)
        result = {
            'MIN': {
                'vehicle': min_vehicle,
                'value': min_
            },
            'MAX': {
                'vehicle': max_vehicle,
                'value': max_
            }
        }
        return result 
    
    def get_extremum_vehicles(self):
        kd_col = "KD"
        wr_col = "WIN_RATE"
        result = {
            wr_col: self._get_extremum_vehicles_for_col(wr_col),
            kd_col: self._get_extremum_vehicles_for_col(kd_col)
        }
        return result



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
