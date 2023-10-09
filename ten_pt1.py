con = sl.connect('st10.db')
with con:
    con.execute("""
                CREATE TABLE IF NOT EXISTS Orders (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(15),
                    salary INTEGER,
                    cab INTEGER
                );
            """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS Choose_operation (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            fio VARCHAR(50),
            data_of_birth DATA,
            tel VARCHAR(15),
            position INTEGER,
            FOREIGN KEY (position) REFERENCES Orders (id)
                ON DELETE RESTRICT ON UPDATE CASCADE


        );
    """)
    con.execute("""
                CREATE TABLE IF NOT EXISTS Warehouses (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50),
                    price INTEGER,
                    duration TIME,
                    position INTEGER,
                    FOREIGN KEY (position) REFERENCES Orders (id)
                        ON DELETE RESTRICT ON UPDATE CASCADE
                );
            """)
    con.execute("""
                    CREATE TABLE IF NOT EXISTS Clients (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        fio VARCHAR(50),                            
                        tel VARCHAR(15),
                        data_of_birth DATA,
                        comment MEDIUMTEXT 
                    );
                """)
    con.execute("""
                    CREATE TABLE IF NOT EXISTS Category (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        time DATETIME,
                        client INTEGER,
                        Choose_operation INTEGER,
                        service INTEGER,
                        FOREIGN KEY (service) REFERENCES Warehouses (id)
                            ON DELETE RESTRICT ON UPDATE CASCADE,
                        FOREIGN KEY (Choose_operation) REFERENCES Choose_operation (id)
                            ON DELETE RESTRICT ON UPDATE CASCADE,
                        FOREIGN KEY (client) REFERENCES Clients (id)
                            ON DELETE RESTRICT ON UPDATE CASCADE    
                    );
                """)

sql_insert = "INSERT OR IGNORE INTO Orders (name, salary, cab) values(?, ?, ?)"
sql_insert2 = "INSERT OR IGNORE INTO Choose_operation (fio, data_of_birth, tel, position) values(?, ?, ?, (SELECT id FROM Orders ORDER BY id DESC LIMIT 1))"
sql_insert3 = "INSERT OR IGNORE INTO Warehouses (name, price, duration, position) values(?, ?, ?, (SELECT id FROM Orders ORDER BY id DESC LIMIT 1))"
sql_insert4 = "INSERT OR IGNORE INTO Clients (fio, tel, data_of_birth, comment) values(?, ?, ?, ?)"
sql_insert5 = "INSERT OR IGNORE INTO Category (time, client, Choose_operation, service) values(?, (SELECT id FROM Clients ORDER BY id DESC LIMIT 1), (SELECT id FROM Choose_operation ORDER BY id DESC LIMIT 1), (SELECT id FROM Warehouses ORDER BY id DESC LIMIT 1))"

list1 = [('хирург', 50, 12), ('ортопед', 40, 36), ('терапевт', 45, 152), ('окулист', 45, 66), ('кардиолог', 53, 23)]
list2 = [('Пупа Олег Викторович', '1972-02-15', '375259998845'),
         ('Лупа Станислав Николаевич', '1973-05-25', '375259379992'),
         ('Шалопай Петр Валерьевич', '1992-04-12', '375256556882'),
         ('Косой Виктор Петрович', '1992-04-12', '375256660777'),
         ('Сердецеедова Светлана Михайловна', '1992-04-12', '375252627282',)]
list3 = [('консультация', 12, '00:20'), ('гипсование', 12, '00:30'),
         ('осмотр', 12, '00:20'), ('проверка зрения', 12, '00:07'),
         ('консультация', 12, '00:20')]
list4 = [
    ('Летов Игорь Фёдорович', '375259998845', '1964-09-10', None),
    ('Горшнёв Михаил Юрьевич', '375259669523', '1973-08-07', None),
    ('Цой Виктор Робертович', '375251235564', '1962-06-21', None),
    ('Высоцкий Владимир Семёнович', '375296256612', '1938-12-25', None),
    ('Тальков Игорь Владимирович', '375335623142', '1956-11-04', None)]

list5 = [('2022-12-06 10:20:15',), ('2022-12-05 18:23:22',), ('2022-12-07 10:37:22',), ('2022-12-02 19:19:22',),
         ('2022-12-09 12:17:22',)]

with con:
    for item in range(4):
        con.execute(sql_insert, list1[item])
        con.execute(sql_insert2, list2[item])
        con.execute(sql_insert3, list3[item])
        con.execute(sql_insert4, list4[item])
        con.execute(sql_insert5, list5[item])

