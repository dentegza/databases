import model


def input_data(choice: int) -> list[str]:
    print("Input data separated by comma")
    data = ""
    match choice:
        case 1:
            data = input('Table: dormitory. Input: number->int, type->text, address->text, faculty->text\n')
        case 2:
            data = input('Table: room_type. Input: seats->int, furniture->boolean, gender->text\n')
        case 3:
            data = input('Table: inmate. Input: name->text, surname->text, gender->text, study_year->int, dormitory_id->int\n')
        case 4:
            data = input('Table: room. Input: number->int, floor->int, settlement->date, eviction->date, dormitory_id->int, room_type_id->int\n')
        case 5:
            data = input('Table: room/inmate. Input: room_id->int, inmate_id->int\n')
    return data.split(',')


def print_data(nums: list[int], rows):
    d = []
    for num in nums:
        match num:
            case 1:
                d += ['dormitory_id', 'number', 'type', 'address', 'faculty']
            case 2:
                d += ['room_type_id' ,'seats', 'furniture', 'gender']
            case 3:
                d += ['inmate_id', 'name', 'surname', 'gender', 'study_year', 'dormitory_id']
            case 4:
                d += ['room_id', 'number', 'floor', 'settlement', 'eviction', 'dormitory_id', 'room_type_id']
            case 5:
                d += ['room_id', 'inmate_id']
    names = []
    lengths = []
    rules = []
    rls = []
    for dd in d:
        names.append(dd)
        lengths.append(len(dd))
    for col in range(len(lengths)):
        for row in rows:
            rls.append(3 if type(row[col]) is not str else len(row[col]))
        lengths[col] = max([lengths[col]] + rls)
        rules.append("#" * lengths[col])
    format = " ".join(["%%-%ss" % l for l in lengths])
    result = [format % tuple(names), format % tuple(rules)]
    for row in rows:
        result.append(format % row)
    return "\n".join(result) + '\n'


def table_by_choice(choice: int) -> str:
    table = ""
    match choice:
        case 1:
            table = 'dormitory'
        case 2:
            table = 'room_type'
        case 3:
            table = 'inmate'
        case 4:
            table = 'room'
        case 5:
            table = 'room/inmate'
    return table


def print_request(choice: int, id: str = '', quantity: str = '0', offset: str = '0') -> str:
    if choice <= 0 or choice > 5:
        return ""
    table = table_by_choice(choice)
    if not id:
        if quantity == '0':
            quantity = str(input('Input quantity of rows to print: '))
        rows = model.select_by_table(table, quantity, offset)
    else:
        if choice == 5:
            rows = model.select_by_key(table, 'room_id', id)
        else:
            rows = model.select_by_key(table, table + '_id', id)
    return print_data([choice], rows)


def select_table(flag: bool = False) -> int:
    choice = -1
    if flag == True:
        print("\n1. Generate data for all tables\n2. Generate data for one table")
        choice = int(input('\nChoose the option: '))
        while choice != 1 and choice != 2:
            choice = int(input('\nError. Choose the option: '))
        if choice == 1:
            choice = 6
    if flag == False or choice == 2:
        print('1. dormitory\n2. room_type\n3. inmate\n4. room\n5. room/inmate\n0. menu')
        choice = int(input('\nChoose the table: '))
    if choice > 6 or choice < 0:
        print('Incorrect number, try one more time')
        if flag == True:
            select_table(True)
        else:
            select_table()
    return choice


def insert_request(choice: int):
    if choice <= 0 or choice > 6:
        return
    rows = [i.strip() for i in input_data(choice)]
    if model.insert(choice, rows):
        print("Data INSERTED successfully")
    else:
        print("Impossible to insert data")


def edit_request(choice: int):
    if choice <= 0 or choice > 5:
        return
    id = input("Enter id of row that you want to UPDATE\n"
               "\'p\' => print rows\n\'r\' => return to menu\n")
    id2 = ""
    if choice == 5:
        id2 = input("Enter id2 of row that you want to UPDATE\n")
    if id == 'r':
        return
    elif id == 'p':
        offset = '0'
        while True:
            print(print_request(choice, quantity='15', offset=offset))
            id = input("Enter id of row that you want to UPDATE\n"
                        "\'n\' => next 15 rows\n\'b\' => previous 15 rows\n\'r\' => return to menu\n")
            if choice == 5:
                id2 = input("Enter id2 of row that you want to UPDATE\n")
            if id == 'r':
                return
            elif id == 'n':
                offset = str(int(offset) + 15)
            elif id == 'b':
                offset = str(int(offset) - 15)
            else:
                break
    print_request(choice, id)
    print("If you don't want to UPDATE column -> write as it was")
    columns = input_data(choice)
    if choice == 5:
        flag = model.update(choice, columns, int(id), int(id2))
    else:
        flag = model.update(choice, columns, int(id))
    if flag:
        print('UPDATED successfully')
    else:
        print("Impossible to UPDATE table")


def delete_request(choice: int):
    if choice <= 0 or choice > 5:
        return
    table = table_by_choice(choice)
    id = input("Enter id of row that you want to DELETE\n"
               "\'p\' => print rows\n\'r\' => return to menu\n")
    if id == 'r':
        return
    elif id == 'p':
        offset = '0'
        while True:
            print(print_request(choice, quantity='15', offset=offset))
            id = input("Enter id of row that you want to DELETE\n"
                       "\'n\' => next 15 rows\n\'b\' => previous 15 rows\n\'r\' => return to menu\n")
            if id == 'r':
                return
            elif id == 'n':
                offset = str(int(offset) + 15)
            elif id == 'b':
                offset = str(int(offset) - 15)
            else:
                break
    if choice == 5:
        flag = model.delete(table, 'room_id', id)
    else:
        flag = model.delete(table, table + '_id', id)
    if flag:
        print('The row DELETED successfully')
    else:
        print("Impossible to DELETE the row")


def generator_request(choice: int):
    if choice <= 0 or choice > 6:
        return
    quantity = int(input('Input the data quantity to GENERATE: '))
    if choice == 6:
        print("Data GENERATED and INSERTED into table dormitory successfully") \
            if model.generate(1, quantity) else print("Impossible to GENERATE and INSERT data into table dormitory")
        print("Data GENERATED and INSERTED into table room_type successfully") \
            if model.generate(2, quantity) else print("Impossible to GENERATE and INSERT data into table room_type")
        print("Data GENERATED and INSERTED into table inmate successfully") \
            if model.generate(3, quantity) else print("Impossible to GENERATE and INSERT data into table inmate")
        print("Data GENERATED and INSERTED into table room successfully") \
            if model.generate(4, quantity) else print("Impossible to GENERATE and INSERT data into table room")
        print("Data GENERATED and INSERTED into table room/inmate successfully") \
            if model.generate(5, quantity) else print("Impossible to GENERATE and INSERT data into table room/inmate")
    elif 0 < choice < 6:
        print(f"Data GENERATED and INSERTED into table number {choice} successfully") \
            if model.generate(choice, quantity) \
            else print(f"Impossible to GENERATE and INSERT data into table number {choice}")


def search_request():
    tables = []
    tab = []
    print('Choose the first table')
    tab.append(select_table())
    tables.append(table_by_choice(tab[0]))
    print('Choose the second table')
    tab.append(select_table())
    tables.append(table_by_choice(tab[1]))
    key = input('Input the connecting key: ')
    print('Input the expression. Use "first" and "second" to address to the table attributes, if with string use like')
    value = input()
    rows = model.search(tables, key, value)
    print("\n", print_data(tab, rows[0]))
    print('Time of the executing program:', rows[1] / 1000, ' milliseconds')


def menu():
    while True:
        print('\n1. INSERT data in TABLE')
        print('2. EDIT data in TABLE')
        print('3. DELETE data from TABLE')
        print('4. PRINT ROWS')
        print('5. GENERATE random DATA')
        print('6. SEARCH data from TABLES')
        print('0. Exit')
        match int(input('\t\t\tChoose an option 1-6 or 0: ')):
            case 1:
                insert_request(select_table())
            case 2:
                edit_request(select_table())
            case 3:
                delete_request(select_table())
            case 4:
                print("\n", print_request(select_table()))
            case 5:
                generator_request(select_table(True))
            case 6:
                search_request()
            case 0:
                print("")
                return
