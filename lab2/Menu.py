from Model import Model
from View import View

class Menu:
    @staticmethod
    def MainMenu():
        while True:
            inputValue = input('Input: ')
            if inputValue == 'instruction':
                View.GetInstruction()
            elif inputValue == 'all':
                Model.ShowAllTables()
            elif inputValue == 'print':
                inputValue = input('Table name:')
                if Model.IfInDatabase(inputValue):
                    Model.ShowTable(inputValue)
                else:
                    print("[No such table found]\n")
            elif inputValue == 'insert':
                inputValue = input('Table name:')
                if Model.IfInDatabase(inputValue):
                    Model.InsertInTable(inputValue)
                else:
                    print("[No such table found]\n")
            elif inputValue == 'delete':
                inputValue = input('Table name:')
                if Model.IfInDatabase(inputValue):
                    Model.DeleteFromTable(inputValue)
                else:
                    print("[No such table found]\n")
            elif inputValue == 'update':
                inputValue = input('Table name:')
                if Model.IfInDatabase(inputValue):
                    Model.UpdateTable(inputValue)
                else:
                    print("[No such table found]\n")
            elif inputValue == 'random':
                inputValue = input('Table name:')
                inputValue2 = int(input('Times:'))
                if Model.IfInDatabase(inputValue):
                    Model.GenerateDataForTable(inputValue, inputValue2)
                else:
                    print("[No such table found]\n")
            elif inputValue == 'search':
                Model.SearchForDataInTables()
            elif inputValue == 'exit':
                return
            else:
                print("bad input")
