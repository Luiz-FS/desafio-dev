import json
import psycopg2
import psycopg2.extras


class PostgresqlEventsRepository:
    def __init__(self, db_uri):
        self._db_conn = psycopg2.connect(db_uri)

    def save(self, name, data):
        """Method to save the event in the database.

        Parameters
        ----------
        name : str
            Event name
        data : dict
            Event data
        """
        cursor = self._db_conn.cursor()
        sql = "INSERT INTO events (name, data) VALUES (%s, %s)"
        cursor.execute(sql, (name, json.dumps(data)))
        self._db_conn.commit()
        cursor.close()

    def close_connection(self):
        """Méthod to close database connection."""
        self._db_conn.close()
