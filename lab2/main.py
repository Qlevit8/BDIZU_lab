import Connect
from Menu import Menu

try:
    connection = Connect.MakeConnection()
    cursor = connection.cursor()
    Menu.MainMenu()
except Exception as error:
    print("[Connection Error]", error)
finally:
    cursor.close()
    connection.close()