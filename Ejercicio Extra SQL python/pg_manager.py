import psycopg2


class PgManager:
    def __init__(self, dbname, user, password, host, port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.connection = self.create_connection()
        if self.connection:
            print("Connected to the database")
            self.cursor = self.connection.cursor()

    def create_connection(self):
        try:
            connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed")

    def execute_query(self, query, params=None):
        try:
            if params is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, params)

            self.connection.commit()

            # Check if the query returns any results
            if self.cursor.description:
                return self.cursor.fetchall()

        except Exception as error:
            print("Error executing query:", error)
            return None