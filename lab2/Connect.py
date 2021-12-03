import psycopg2


def MakeConnection():
    return psycopg2.connect(
        user="postgres",
        password="1111",
        host="localhost",
        database="lab_1",
    )


def CloseConnection(connection):
    connection.commit()
    connection.close()