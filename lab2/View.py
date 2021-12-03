import Connect
from tabulate import tabulate


class View:
    def __init__(self, table, fields, values):
        self.table = table
        self.fields = fields
        self.values = values

    def Show(self):
        print('Table:', self.table)
        print(tabulate(self.values, self.fields, tablefmt="fancy_grid"))


    @staticmethod
    def GetInstruction():
        print("all - Виводить всі таблиці, які є в базі даних\n"
              "print - Виводить задану за іменем таблицю з бази даних\n"
              "insert - Вставляє новий запис користувача в вибрану таблицю з бази даних\n"
              "delete - Видаляє рядок з таблиці за заданим індексом\n"
              "update - Оновлює вибрані значення певного рядка таблиці, вибрані користувачем\n"
              "random - Заповнює вибрану таблицю вибраною кількістю згенерованих рядків\n"
              "search - Реалізовю пошук за заданими атрибутами\n"
              "exit - Вихід з програми\n")

    @staticmethod
    def UpdateView(fields):
        print("Available columns:", end=" ")
        print(', '.join(fields))
        column = input("Input column name: ")
        element = input("Input value: ")
        valueString = ""
        for i in range(0, len(fields)):
            print("Do you want to change ", fields[i], "?")
            condition = input("(1-yes, 0-no):")
            if condition == '1':
                newValue = input("Input new value:")
                valueString = fields[i] + " = '" + newValue + "', " + valueString
        return [valueString[:-2], column, element]

    @staticmethod
    def DeletionView(fields):
        print("Available columns:", end=" ")
        print(', '.join(fields))
        column = input("Input column name: ")
        element = input("Input value: ")
        return [column, element]

    @staticmethod
    def InsertionView(table):
        if table == 'book_order':
            book_id = input("book_id: ")
            order_id = input("order_id: ")
            return """INSERT INTO "book_order" (book_id, order_id) VALUES ({}, {})""".format(book_id, order_id)
        elif table == 'book':
            title = input("title: ")
            author = input("author: ")
            genre = input("genre: ")
            price = input("price: ")
            return """INSERT INTO "book" (book_id, title, author, genre, price) 
                VALUES ((SELECT MAX(book_id)+1 FROM "book"), '{}', '{}', '{}', {})""".format(title, author, genre,
                                                                                             price)
        elif table == 'discount_card':
            date_of_expiring = input("date of expiring: ")
            percentage = input("percentage: ")
            customer_id = input("customer_id: ")
            return """INSERT INTO "discount_card" (discount_card_id, date_of_expiring, percentage, customer_id)
                VALUES ((SELECT MAX(discount_card_id)+1 FROM "discount_card"), '{}', {}, {})""".format(date_of_expiring,
                                                                                                       percentage,
                                                                                                       customer_id)
        elif table == 'order':
            date = input("date: ")
            discount_card_id = input("discount_card_id: ")
            customer_id = input("customer_id: ")
            return """INSERT INTO "order" (order_id, date, customer_id, discount_card_id)
                VALUES ((SELECT MAX(order_id)+1 FROM "order"), '{}', {}, {})""".format(date, customer_id,
                                                                                       discount_card_id)
        elif table == "customer":
            customer_name = input("customer_name: ")
            customer_surname = input("customer_surname: ")
            return """INSERT INTO "customer" (customer_id, customer_name, customer_surname) 
                VALUES ((SELECT MAX(customer_id)+1 FROM "customer"), '{}', '{}')""".format(customer_name,
                                                                                           customer_surname)


    @staticmethod
    def CheckIfFk(table, column):
        if column == 'customer_id' and (table == "discount_card" or table == "order"):
            tableName = "customer"
            ColumnName = "customer_id"
        elif column == 'discount_card_id' and table == "order":
            tableName = "discount_card"
            ColumnName = "discount_card_id"
        elif column == 'order_id' and table == "book_order":
            tableName = "order"
            ColumnName = "order_id"
        elif column == 'book_id' and table == "book_order":
            tableName = "book"
            ColumnName = "book_id"
        else:
            return
        return [tableName, ColumnName]


    @staticmethod
    def ChooseOperationByType(objType, objValue, objName, objColumn):
        if objType == 'integer':
            if type(objValue) is list:
                return " {}<={}.{} and {}.{}<={} and".format(objValue[0], objName, objColumn, objName, objColumn, objValue[1])
            else:
                return " " + objName + "." + objColumn + "=" + objValue + " and"
        elif objType == 'character varying':
            return " " + objName + "." + objColumn + " LIKE '" + objValue + "' and"
        else:
            if type(objValue) is list:
                return" {}.{} BETWEEN '{}'and '{}' and".format(objName, objColumn, objValue[0], objValue[1])
            else:
                return " " + objName + "." + objColumn + "='" + objValue + "' and"


    @staticmethod
    def FindType(typeName):
        if typeName == 'date':
            return View.DateType()
        elif typeName == 'character varying':
            return View.StringType()
        elif typeName == 'integer':
            return View.IntegerType()
        else:
            return View.ForeignKeyIntegerType(typeName)

    @staticmethod
    def ForeignKeyIntegerType(value):
        return '(select (1 + random()*(select max(' + value[1] +') FROM "' + value[0] + '"))::int)'

    @staticmethod
    def IntegerType():
        return "1 + random()*1000"

    @staticmethod
    def StringType():
        return "array_to_string(array(" \
               "select chr((" \
               "97 + round(random()*25)) ::integer) " \
               "FROM generate_series(1,7)), '')"

    @staticmethod
    def DateType():
        return "(SELECT NOW() + " \
               "(random()*(NOW()+'90 days' - NOW())) " \
               "+ '30 days')"