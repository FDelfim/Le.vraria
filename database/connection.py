import psycopg2


class Database:
    def __init__(self,
                 db_name="mwobjifl",
                 db_user="mwobjifl",
                 db_pass="sDXBJ7pdX_teihPsOZtQ6PWdFWLP5D-4",
                 db_host="motty.db.elephantsql.com",
                 db_port="5432"):

        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                database=self.db_name, user=self.db_user, password=self.db_pass, host=self.db_host,
                port=self.db_port)
        except psycopg2.OperationalError as err:
            print("A conexão com o banco de dados falhou ", err.message)

    def open(self):
        self.connect()
        self.cursor = self.connection.cursor()

    def update(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

