import model


if __name__ == '__main__':
    new_model = model.Model()
    new_model.print_table('customer')
    print(new_model.search_for_data_two_tables())
    new_model.print_table('customer')
    #new_model.delete('customer', 8)
