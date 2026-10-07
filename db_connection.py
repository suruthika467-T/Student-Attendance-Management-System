import oracledb

def get_connection():
    return oracledb.connect(
        user="dbms_user",
        password="dbms123",
        dsn="localhost/XEPDB1"
    )
