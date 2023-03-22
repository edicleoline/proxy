import apsw
import apsw.ext

def connection():
    connection = apsw.Connection("/home/berners/Documents/dev/proxy/data.db")
    connection.setbusytimeout(5000)
    connection.execute("PRAGMA journal_mode=WAL")
    return connection
