import Connect
from View import View
from tabulate import tabulate


class Model:
    @staticmethod
    def GetTables():
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        cursor.execute("""SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'""")
        tables = cursor.fetchall()
        for i in range(0, len(tables)):
            tables[i] = tables[i][0]
        return tables

    @staticmethod
    def GetFields(table):
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        cursor.execute("""SELECT column_name
             from information_schema.columns 
             where table_name = '{}'
             order by ordinal_position""".format(table))
        names = cursor.fetchall()
        for i in range(0, len(names)):
            names[i] = names[i][0]
        cursor.close()
        Connect.CloseConnection(connection)
        return names

    @staticmethod
    def IfInDatabase(name):
        if name in Model.GetTables():
            return True
        else:
            return False

    @staticmethod
    def ShowTable(table):
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM public.{};""".format(table))
        viewObj = View(table, Model.GetFields(table), cursor.fetchall())
        viewObj.Show()
        cursor.close()
        Connect.CloseConnection(connection)

    @staticmethod
    def ShowAllTables():
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        for table in cursor.fetchall():
            Model.ShowTable(table[0])
        cursor.close()
        Connect.CloseConnection(connection)

    @staticmethod
    def InsertInTable(table):
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        try:
            opperation = View.InsertionView(table)
            cursor.execute(opperation)
            print(f"[Insertion is done]\n[{opperation}]\n")
        except Exception as error:
            print("[ERROR, data are not suitable]\n")
        cursor.close()
        Connect.CloseConnection(connection)


    @staticmethod
    def DeleteFromTable(table):
        fields = Model.GetFields(table)
        result = View.DeletionView(fields)
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        try:
            opperation = """DELETE FROM "{}" WHERE {}='{}'""".format(table, result[0], result[0])
            cursor.execute(opperation)
            print(f"[Deletion is done]\n[{opperation}]\n")
        except Exception as error:
            print("[ERROR, this record is connected with another table]\n")
        cursor.close()
        Connect.CloseConnection(connection)

    @staticmethod
    def UpdateTable(table):
        fields = Model.GetFields(table)
        res = View.UpdateView(fields)
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        try:
            result = """UPDATE "{}"
            SET {}
            WHERE {}='{}'""".format(table, res[0], res[1], res[2])
            cursor.execute(result)
            print(f"[Update is done]\n[{result}]\n")
        except Exception as error:
            print("[ERROR, argument is out of range]\n")
        cursor.close()
        Connect.CloseConnection(connection)

    @staticmethod
    def IsIdentity(table, column, cursor):
        cursor.execute(
            """select is_identity
                from information_schema.columns
                where table_name = '{}' and 
                column_name = '{}'""".format(table, column))
        return cursor.fetchone()[0] == 'NO'


    @staticmethod
    def GetColumnType(table, column):
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        cursor.execute(
            """select data_type
            from information_schema.columns
            where table_name = '{}' and
            column_name = '{}'""".format(table, column))
        res = cursor.fetchone()[0]
        cursor.close()
        Connect.CloseConnection(connection)
        return res

    @staticmethod
    def GenerateDataForTable(table, times):
        fields = Model.GetFields(table)
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        fieldsTypes = []
        for i in range(0, len(fields)):
            if Model.IsIdentity(table, fields[i], cursor):
                type = Model.GetColumnType(table, fields[i])
                result = View.CheckIfFk(table, fields[i])
                if result is not None:
                    fieldsTypes.append(View.FindType(result))
                else:
                    fieldsTypes.append(View.FindType(type))
            else:
                fieldsTypes.append('(SELECT MAX(' + fields[i] + ')+1 FROM "' + table + '")')
        try:
            word = """INSERT INTO "{}" ({}) 
            VALUES ({});""".format(table, ", ".join(fields), ", ".join(fieldsTypes))
            for i in range(0, times):
                cursor.execute(word)
            print(str(times) + " random fields were insert into " + str(table) + " table")
            print(word)
        except Exception as error:
            print("[ERROR, something went wrong]", error)
        cursor.close()
        Connect.CloseConnection(connection)


    @staticmethod
    def FindSameColumns(first, second):
        names = []
        for i in Model.GetFields(first):
            for j in Model.GetFields(second):
                if i == j:
                    names.append(i)
        return names


    @staticmethod
    def SearchForDataInTables():
        names = ["one", "two", "three", "four", "five"]
        tables = Model.GetTables()
        data = []
        while True:
             print("Please choose one of the tables(" + ", ".join(tables) + "): ", end="")
             tableInput = input()
             if tableInput in tables:
                 tables.remove(tableInput)
                 columns = Model.GetFields(tableInput)
                 print("You can chose from (" + ", ".join(columns) + "): ", end="")
                 columnInput = input()
                 if columnInput in columns:
                     columnType = Model.GetColumnType(tableInput, columnInput)
                     print("The type is " + columnType)
                     if columnType == 'character varying':
                         inputValue = input("Find by name: ")
                         data.append([tableInput, columnInput, columnType, inputValue])
                     else:
                         inputValue = input("Find within the boundaries?: ")
                         if inputValue == 'yes':
                             leftBound = input("Left bound: ")
                             rightBound = input("Right bound: ")
                             data.append([tableInput, columnInput, columnType, [leftBound, rightBound]])
                         else:
                             inputValue = input("Find by value: ")
                             data.append([tableInput, columnInput, columnType, inputValue])
             else:
                 cond = input("Do you want to stop? ")
                 if cond == 'yes' and len(tables) < 4:
                     break
        upperWord = 'SELECT * from "' + data[0][0] + '" as ' + names[0]
        lowerWord = 'WHERE' + View.ChooseOperationByType(data[0][2], data[0][3], names[0], data[0][1])
        for i in range(1, len(data)):
            sameColumns = ""
            upperWord = upperWord + ' inner join "' + data[i][0] + '" as ' + names[i]
            for j in range(0, i):
                res = Model.FindSameColumns(data[j][0], data[i][0])
                for k in range(0, len(res)):
                    sameColumns = sameColumns + names[j] + '."' + res[k] + '"=' + names[i] + '."' + res[k] + '" and '
            if len(sameColumns) > 1:
                upperWord = upperWord + " on " + sameColumns[:-4]
            lowerWord = lowerWord + View.ChooseOperationByType(data[i][2], data[i][3], names[i], data[i][1])
        connection = Connect.MakeConnection()
        cursor = connection.cursor()
        try:
            cursor.execute(upperWord + lowerWord[:-4])
            info = cursor.fetchall()
            for i in info:
                print(i)
        except Exception as error:
            print("[ERROR, something went wrong]: ")
        cursor.close()
        Connect.CloseConnection(connection)