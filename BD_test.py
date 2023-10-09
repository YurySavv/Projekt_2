import sqlite3
import datetime
from faker import Faker

fake = Faker()

# Создаем соединение с базой данных
conn = sqlite3.connect('inventory_management.db')
cursor = conn.cursor()

# Создаем таблицу "Категории товаров"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProductCategories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')

# Создаем таблицу "Характеристики товаров"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProductCharacteristics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')

# Создаем таблицу "Производители"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Manufacturers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')

# Создаем таблицу "Поставщики"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact_info TEXT
    )
''')

# Создаем таблицу "Товары"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        characteristic_id INTEGER,
        manufacturer_id INTEGER,
        supplier_id INTEGER,
        name TEXT,
        code TEXT UNIQUE,
        description TEXT,
        expiration_date DATE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES ProductCategories(id),
        FOREIGN KEY (characteristic_id) REFERENCES ProductCharacteristics(id),
        FOREIGN KEY (manufacturer_id) REFERENCES Manufacturers(id),
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
    )
''')

# Создаем таблицу "Цены и Скидки"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PriceDiscounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        supplier_id INTEGER,
        price REAL,
        discount REAL,
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
    )
''')

# Создаем таблицу "Склады"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Warehouses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        name TEXT,
        location_text TEXT,
        location_coordinates TEXT
    )
''')

# Создаем таблицу "Сотрудники"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        position TEXT,
        contact_info TEXT,
        warehouse_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (warehouse_id) REFERENCES Warehouses(id)
    )
''')

# Создаем таблицу "Клиенты"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category_id INTEGER,
        contact_info TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES CustomerCategories(id)
    )
''')

# Создаем таблицу "Категории клиентов"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CustomerCategories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')

# Создаем таблицу "Заказы"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        employee_id INTEGER,
        date DATETIME,
        status TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES Customers(id),
        FOREIGN KEY (employee_id) REFERENCES Employees(id)
    )
''')

# Создаем таблицу "Товары в Заказе"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS OrderItems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price_per_unit REAL,
        discount REAL,
        total_price REAL,
        FOREIGN KEY (order_id) REFERENCES Orders(id),
        FOREIGN KEY (product_id) REFERENCES Products(id)
    )
''')

# Создаем таблицу "Движение товаров"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS StockMovements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        warehouse_id INTEGER,
        movement_type TEXT,
        quantity INTEGER,
        movement_date DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (warehouse_id) REFERENCES Warehouses(id)
    )
''')

# Создаем таблицу "Остатки товаров"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS StockBalances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        warehouse_id INTEGER,
        quantity INTEGER,
        balance_date DATE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (warehouse_id) REFERENCES Warehouses(id)
    )
''')

# Создаем таблицу "Документы"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        content BLOB,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        employee_id INTEGER,
        FOREIGN KEY (employee_id) REFERENCES Employees(id)
    )
''')

# Заполняем таблицы тестовыми данными

# Заполняем таблицу "Категории товаров"
categories = ["Электроника", "Одежда", "Бытовая техника"]
for category in categories:
    cursor.execute("INSERT INTO ProductCategories (name) VALUES (?)", (category,))

# Заполняем таблицу "Характеристики товаров"
characteristics = ["Цвет", "Размер", "Вес"]
for characteristic in characteristics:
    cursor.execute("INSERT INTO ProductCharacteristics (name) VALUES (?)", (characteristic,))

# Заполняем таблицу "Производители"
manufacturers = ["Samsung", "Apple", "LG"]
for manufacturer in manufacturers:
    cursor.execute("INSERT INTO Manufacturers (name) VALUES (?)", (manufacturer,))

# Заполняем таблицу "Поставщики"
suppliers = [("Поставщик 1", "Телефон: 123-456"), ("ИП Иванов И.И.", "Email: ivanov@example.com")]
for supplier in suppliers:
    cursor.execute("INSERT INTO Suppliers (name, contact_info) VALUES (?, ?)", supplier)

# Заполняем таблицу "Товары"
products = [("Телефон", 1, 1, 1, "Телефон Samsung Galaxy", "12345", "Смартфон", None, None),
            ("Футболка", 2, 2, 2, "Футболка размер M", "67890", "Красная футболка", None, None),
            ("Холодильник", 3, 3, 1, "Холодильник LG", "24680", "Двухкамерный холодильник", None, None)]
for product in products:
    cursor.execute("INSERT INTO Products (name, category_id, characteristic_id, manufacturer_id, supplier_id, code, description, expiration_date, image, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", product)

# Заполняем таблицу "Цены и Скидки"
price_discounts = [(1, 1, 500, 0.1), (2, 2, 30, 0.05), (3, 1, 1000, 0.15)]
for price_discount in price_discounts:
    cursor.execute("INSERT INTO PriceDiscounts (product_id, supplier_id, price, discount) VALUES (?, ?, ?, ?)", price_discount)

# Заполняем таблицу "Склады"
warehouses = [("Адрес склада 1", "Склад 1", "Геолокация склада 1"), ("Адрес склада 2", "Склад 2", "Геолокация склада 2")]
for warehouse in warehouses:
    cursor.execute("INSERT INTO Warehouses (address, name, location_text) VALUES (?, ?, ?)", warehouse)

# Заполняем таблицу "Сотрудники"
employees = [("Иванов Иван", "Менеджер", "Email: ivanov@example.com", 1),
             ("Петров Петр", "Кладовщик", "Email: petrov@example.com", 2)]
for employee in employees:
    cursor.execute("INSERT INTO Employees (name, position, contact_info, warehouse_id, created_at, updated_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", employee)

# Заполняем таблицу "Клиенты"
customers = [("Клиент 1", 1, "Email: client1@example.com"), ("Клиент 2", 2, "Email: client2@example.com")]
for customer in customers:
    cursor.execute("INSERT INTO Customers (name, category_id, contact_info, created_at, updated_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", customer)

# Заполняем таблицу "Категории клиентов"
customer_categories = ["Категория 1", "Категория 2"]
for category in customer_categories:
    cursor.execute("INSERT INTO CustomerCategories (name) VALUES (?)", (category,))

# Заполняем таблицу "Заказы"
orders = [(1, 1, datetime.datetime.now(), "в обработке"), (2, 2, datetime.datetime.now(), "выполнен")]
for order in orders:
    cursor.execute("INSERT INTO Orders (customer_id, employee_id, date, status, created_at, updated_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", order)

# Заполняем таблицу "Товары в Заказе"
order_items = [(1, 1, 1, 300, 0.05, 285), (2, 2, 2, 25, 0, 25)]
for item in order_items:
    cursor.execute("INSERT INTO OrderItems (order_id, product_id, quantity, price_per_unit, discount, total_price) VALUES (?, ?, ?, ?, ?, ?)", item)

# Заполняем таблицу "Движение товаров"
stock_movements = [(1, 1, "поступление", 100, "2023-10-02 12:00:00"),
                   (2, 2, "отгрузка", 20, "2023-08-09 18:00:00")]
for movement in stock_movements:
    cursor.execute("INSERT INTO StockMovements (product_id, warehouse_id, movement_type, quantity, movement_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", movement)

# Заполняем таблицу "Остатки товаров"
stock_balances = [(1, 1, 80, datetime.date.today()), (2, 2, 30, datetime.date.today())]
for balance in stock_balances:
    cursor.execute("INSERT INTO StockBalances (product_id, warehouse_id, quantity, balance_date, created_at, updated_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", balance)

# Заполняем таблицу "Документы"
documents = [("накладная", "Содержание накладной", 1), ("счет-фактура", "Содержание счет-фактуры", 2)]
for document in documents:
    cursor.execute("INSERT INTO Documents (type, content, employee_id, created_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", document)

# Применяем изменения
conn.commit()

# Закрываем соединение с базой данных
conn.close()