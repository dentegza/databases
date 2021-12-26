import psycopg2
import time

cursor = None
connection = None


def connect():
    try:
        global cursor, connection
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            database="hostel_db",
            port="5432"
        )

        cursor = connection.cursor()

        print("Successfully CONNECTED to database HOSTEL")

    except Exception as _ex:
        print("Failed CONNECTION to database HOSTEL", _ex)


def disconnect():
    try:
        cursor.close()
        connection.close()
        print("Successfully DISCONNECTED from database HOSTEL")
    except Exception as _ex:
        print("Impossible to DISCONNECT from database HOSTEL", _ex)


def insert(choice: int, data: list) -> bool:
    if connection is None or cursor is None:
        return False
    else:
        try:
            match choice:
                case 1:
                    cursor.execute(f"""INSERT INTO public.\"dormitory\" (number, type, address, faculty) \
                                    VALUES ({data[0]}, \'{data[1]}\', \'{data[2]}\', \'{data[3]}\');""")
                case 2:
                    cursor.execute(f"""INSERT INTO public.\"room_type\" (seats, furniture, gender) \
                                    VALUES ({data[0]}, {data[1]}, \'{data[2]}\');""")
                case 3:
                    cursor.execute(f"""INSERT INTO public.\"inmate\" (name, surname, gender, study_year, dormitory_id) \
                                    VALUES (\'{data[0]}\', \'{data[1]}\', \'{data[2]}\', {data[3]}, {data[4]});""")
                case 4:
                    cursor.execute(f"""INSERT INTO public.\"room\"(number, floor, settlement, eviction, dormitory_id, \
                    room_type_id) VALUES({data[0]}, {data[1]}, \'{data[2]}\', \'{data[3]}\', {data[4]}, {data[5]});""")
                case 5:
                    cursor.execute(f"""INSERT INTO public.\"room/inmate\" (room_id, inmate_id) \
                                    VALUES ({data[0]}, {data[1]});""")
            connection.commit()
        except Exception as _ex:
            print(f"Impossible to INSERT data: {data}; into table with choice: {choice}", _ex)
            return False
    return True


def delete(table: str, key_name: str, key_val: str) -> bool:
    if connection is None or cursor is None:
        return False
    else:
        try:
            cursor.execute(f"""DELETE FROM public.\"{table}\" WHERE {key_name} = \'{key_val}\';""")
            connection.commit()
        except Exception as _ex:
            print(f"Impossible to DELETE data from table {table} in database HOSTEL", _ex)
            return False
    return True


def select_by_key(table: str, key_name: str, key_val: str) -> list:
    if connection is None or cursor is None:
        return []
    else:
        try:
            cursor.execute(f"""SELECT * FROM public.\"{table}\" WHERE {key_name} = \'{key_val}\';""")
        except Exception as _ex:
            print(f"Impossible to SELECT data from table {table} by key {key_name} in database HOSTEL", _ex)
            return []
    return cursor.fetchall()


def select_by_table(table: str, quantity: str = '100', offset: str = '0') -> list:
    if connection is None or cursor is None:
        return []
    else:
        try:
            if table == 'room/inmate':
                cursor.execute(f"""SELECT * FROM public.\"{table}\" ORDER BY {"room_id"} \
                                                ASC limit {quantity} offset {offset};""")
            else:
                cursor.execute(f"""SELECT * FROM public.\"{table}\" ORDER BY {table + "_id"} \
                                                ASC limit {quantity} offset {offset};""")
        except Exception as _ex:
            print(f"Impossible to SELECT data from table {table} in database HOSTEL", _ex)
            return []
    return cursor.fetchall()


def update(choice: int, data: list, id1: int, id2: int = 0) -> bool:
    if connection is None or cursor is None:
        return False
    else:
        try:
            match choice:
                case 1:
                    cursor.execute(f"""UPDATE public.\"dormitory\" SET number = {data[0]}, type = \'{data[1]}\', \
                    address = \'{data[2]}\', faculty = \'{data[3]}\' WHERE dormitory_id = {id1};""")
                case 2:
                    cursor.execute(f"""UPDATE public.\"room_type\" SET seats = {data[0]}, furniture = {data[1]}, \
                    gender = \'{data[2]}\' WHERE room_type_id = {id1};""")
                case 3:
                    cursor.execute(f"""UPDATE public.\"inmate\" SET name = \'{data[0]}\', surname = \'{data[1]}\', \
                    gender = \'{data[2]}\',study_year = {data[3]}, dormitory_id = {data[4]} WHERE inmate_id = {id1};""")
                case 4:
                    cursor.execute(f"""UPDATE public.\"room\" SET number = {data[0]}, floor = {data[1]}, \
                    settlement = \'{data[2]}\', eviction = \'{data[3]}\', dormitory_id = {data[4]}, \
                    room_type_id = {data[5]} WHERE room_id = {id1};""")
                case 5:
                    cursor.execute(f"""UPDATE public.\"room/inmate\" SET room_id = {data[0]}, \
                    inmate_id = {data[1]} WHERE room_id = {id1} AND inmate_id = {id2};""")
            connection.commit()
        except Exception as _ex:
            print(f"Impossible to UPDATE data: {data}; into table with choice: {choice}", _ex)
            return False
    return True


def generate(choice: int, count: int) -> bool:
    if connection is None or cursor is None:
        return False
    try:
        for i in range(count):
            match choice:
                case 1:
                    cursor.execute(f"""INSERT INTO public.\"dormitory\" (number, type, address, faculty) \
                                    VALUES ((floor(random() * (30 - 1 + 1)) + 1), substr(md5(random()::text), 0, 8), \
                                        substr(md5(random()::text), 0, 12), substr(md5(random()::text), 0, 5));""")
                case 2:
                    cursor.execute(f"""INSERT INTO public.\"room_type\" (seats, furniture, gender) \
                                    VALUES ((floor(random() * (4 - 1 + 1)) + 1), (round(random())::int)::boolean, \
                                        substr(md5(random()::text), 0, 6));""")
                case 3:
                    cursor.execute(f"""INSERT INTO public.\"inmate\" (name, surname, gender, study_year, dormitory_id) \
                                    SELECT substr(md5(random()::text), 0, 10), \
                                        substr(md5(random()::character varying(12)), 0, 12), \
                                        substr(md5(random()::text), 0, 6), \
                                        (floor(random() * (2022 - 1975 + 1)) + 1975), \
                                        dormitory_id FROM public."dormitory" order by random() limit 1;""")
                case 4:
                    cursor.execute(f"""INSERT INTO public.\"room\"(number, floor, settlement, eviction, dormitory_id, \
                                    room_type_id) \
                                    SELECT floor(random() * (1000 - 10 + 1) + 10), floor(random() * (500 - 1 + 1) + 1),\
                                        NOW() + (random() * (NOW() - NOW() - '16000 days')), \
                                        NOW() + (random() * (NOW() - NOW() + '36000 days')), \
                                        dormitory_id, room_type_id FROM public."dormitory", public."room_type" \
                                        order by random() limit 1;""")
                case 5:
                    cursor.execute(f"""INSERT INTO public.\"room/inmate\" (room_id, inmate_id) \
                                    SELECT room_id, inmate_id FROM public."room", public."inmate" \
                                        order by random() limit 1;""")
        connection.commit()
    except Exception as _ex:
        print("Impossible to GENERATE data to database HOSTEL", _ex)
        return False
    return True


def search(tables: list[str], key: str, value: str) -> tuple:
    if connection is None or cursor is None:
        return ()
    try:
        request = f"""SELECT * FROM public.\"{tables[0]}\" as first INNER JOIN public.\"{tables[1]}\" as second on first.\"{key}\" = second.\"{key}\" WHERE {value}"""
        print(f"SQL request: {request}")
        start_time = time.time_ns()
        cursor.execute(request)
        rows = cursor.fetchall()
        run_time = time.time_ns() - start_time
    except Exception as _ex:
        print("Impossible to SEARCH data in database HOSTEL", _ex)
        return ()
    return rows, run_time
