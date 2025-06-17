from dotenv import load_dotenv
import os
import pymysql

load_dotenv()  # Cargar variables de entorno desde .env

def get_connection():
    host = os.getenv("MYSQL_HOST")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    database = os.getenv("MYSQL_DATABASE")

    print(f"🔍 Conectando a MySQL:")
    print(f"    HOST: {host}")
    print(f"    USER: {user}")
    print(f"    DB:   {database}")

    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )

