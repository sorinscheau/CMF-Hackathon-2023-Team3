import pyodbc
from pypika import Query, Table, Column
from KeyVaultIntegration import get_kv_secret


db_username = get_kv_secret('database-username')
db_password = get_kv_secret('database-password')
database = get_kv_secret('database-name')
server = get_kv_secret('database-server')
driver = '{ODBC Driver 17 for SQL Server}'
users_table = Table('Users')

# conn_string = f'Server=tcp:{server},1433;' \
#               f'Initial Catalog={database};' \
#               'Persist Security Info=False;' \
#               f'User ID={db_username};' \
#               f'Password={db_password};' \
#               'MultipleActiveResultSets=False;' \
#               'Encrypt=True;' \
#               'TrustServerCertificate=False;' \
#               'Connection Timeout=30;'

def create_table(table_name):
    tabl = Table(table_name)
    client_username = Column("username", "VARCHAR(100)")
    client_hash = Column("hash", "VARCHAR(100)")
    create_table_query = Query.create_table(tabl).columns(client_username, client_hash)
    
    with pyodbc.connect('DRIVER=' + driver +
                        ';SERVER=' + server +
                        ';PORT=1433;DATABASE=' + database +
                        ';UID=' + db_username +
                        ';PWD=' + db_password
                        ) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(str(create_table_query))
                row = cursor.fetchone()
                while row:
                    row = cursor.fetchone()
            except pyodbc.ProgrammingError as e:
                print(e)


def query_table_for_user(client_user):
    """

    :param client_user: str Name of the user to search for
    :return: bool True if user exists, False otherwise
    """
    query_users = Query.from_(users_table).select('username')
    with pyodbc.connect('DRIVER=' + driver +
                        ';SERVER=' + server +
                        ';PORT=1433;DATABASE=' + database +
                        ';UID=' + db_username +
                        ';PWD=' + db_password
                        ) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(str(query_users))
                row = cursor.fetchone()
                while row:
                    if client_user in row:
                        return True
                    row = cursor.fetchone()
            except pyodbc.ProgrammingError as e:
                print(e)
    return False


def add_user(user, pass_hash):
    user_exists = query_table_for_user(user)
    if not user_exists:
        insert_user = Query.into(users_table).insert(user, pass_hash)

        with pyodbc.connect('DRIVER=' + driver +
                            ';SERVER=' + server +
                            ';PORT=1433;DATABASE=' + database +
                            ';UID=' + db_username +
                            ';PWD=' + db_password
                            ) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(str(insert_user))
                    row = cursor.fetchone()
                    while row:
                        row = cursor.fetchone()
                except pyodbc.ProgrammingError as e:
                    pass


def get_user_hash(client_user):
    """

    :param client_user: str Name of the user to search for
    :return: bool True if user exists, False otherwise
    """
    query_users = Query.from_(users_table).select('username', 'hash').where(users_table.username == client_user)
    with pyodbc.connect('DRIVER=' + driver +
                        ';SERVER=' + server +
                        ';PORT=1433;DATABASE=' + database +
                        ';UID=' + db_username +
                        ';PWD=' + db_password
                        ) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(str(query_users))
                row = cursor.fetchone()
                if row:
                    print(row)
                    return row[1]
            except pyodbc.ProgrammingError as e:
                print(e)
    return False
