import mysql.connector
from mysql.connector import Error

def create_table():
    connection = None
    try:
        # Conectar al servidor MySQL y seleccionar la base de datos
        connection = mysql.connector.connect(
            host='database-2.cnouiecoqkxd.eu-north-1.rds.amazonaws.com',
            user='',
            password='',
            database='database-2'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS queries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    query_text TEXT NOT NULL,
                    response_text TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            print("Table `queries` created successfully")
            cursor.close()
            
    except Error as e:
        print("Error while creating table", e)
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    create_table()
import mysql.connector
from mysql.connector import Error

def create_and_connect_database():
    connection = None  # Inicializar la variable connection
    try:
        # Conectar al servidor MySQL sin especificar una base de datos
        connection = mysql.connector.connect(
            host='database-2.cnouiecoqkxd.eu-north-1.rds.amazonaws.com',
            user='',
            password=''
        )
        if connection.is_connected():
            print("Successfully connected to the server")

            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()

            # Verificar si la base de datos existe
            db_exists = any(db[0] == 'database-2' for db in databases)

            if not db_exists:
                # Crear la base de datos si no existe
                cursor.execute("CREATE DATABASE `database-2`;")
                print("Database `database-2` created successfully")
            else:
                print("Database `database-2` already exists")

            # Seleccionar la base de datos
            connection.database = 'database-2'
            print("Connected to database `database-2`")

            # Realiza operaciones en la base de datos aquí
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("Tables in `database-2`:", tables)
            
            return connection  # Devolver la conexión para uso posterior
            
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            print("MySQL connection is ready for further operations")

if __name__ == "__main__":
    connection = create_and_connect_database()
    if connection:
        print("Connection established successfully.")
    else:
        print("Connection failed.")
