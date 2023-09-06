# from django.db import connection
import psycopg2
import os

class OpenPostgresConnectionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("in the middleware")
        # Open Postgres connection
        db_params = {
            'dbname': os.getenv('data_db_database', 'UI-POC'),
            'user': os.getenv('data_db_user', 'postgres'),
            'password': os.getenv('data_db_pass', '123456'),
            'host': os.getenv('data_db_host', '114.143.58.70'),
            'port': os.getenv('data_db_port', '8503'),
        }


        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        request.db_connection = connection
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'poc'
        """

        cursor.execute(query)

        table_names = cursor.fetchall()
        print(table_names)
        return self.get_response(request)

class ClosePostgresConnectionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Close Postgres connection
        if hasattr(request, 'db_connection'):
            request.db_connection.close()
        print("Closed")
        return response
