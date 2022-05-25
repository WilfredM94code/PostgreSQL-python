# -----------------------------------------------------------------
# ---------------- PostgreSQL Create tables using -----------------
# ---------------------------- Python -----------------------------
# -----------------------------------------------------------------

# To work with Postgresql with python there must be installed the
# 'psycopg2' module

import psycopg2

connection = psycopg2.connect(
    database = 'company_sales',
    user = 'wm',
    password = '2828',
    host = 'localhost',
    port = '5432'
)
# The 'psycopg2.connect()' recieves several arguments to stablish a 
# connection to a database
print (connection)
# This print returns some values referent to the stablished connection 
# such as username, the databasename, the host name, etc.
print (type(connection))
# The 'psycopg2.connect()' method returns a 
# '<class 'psycopg2.extensions.connection'>' object that stablishes a 
# connection for a particular database and allows to manage it


cursor = connection.cursor()
print (cursor)
print (type(cursor))
# The '.cursor()' returns a '<class 'psycopg2.extensions.cursor'>' object

cursor.execute('''
        CREATE TABLE sales
        (order_num INT PRIMARY KEY,
        order_type TEXT,
        cus_name TEXT,
        prod_number TEXT,
        prod_name TEXT,
        quantity INT,
        price REAL,
        discount REAL,
        order_total REAL
        )
''')
# There has been created a SQL query which wont have effect until 
# commited that is meant to be executed

connection.commit ()
# The '.commit()' method allows to commit every query stored in the current
# connection

connection.close ()
# Once done the connection has to be terminated under the '.close ()' 
# method

# From the 'SQL Shell (psql)' the tables created can be shown, for that
# The user must be logged in under a valid role, once logend in there 
# must be stablished a connection between the terminal and a database 
# using the '\c databasename' command and then, to watch the tables from
# that database there has to be used the '\dt' command (the '\d' command)
# works the same

# -----------------------------------------------------------------
# ----------------- PostgreSQL insert data into a -----------------
# ------------------- database using a CSV file -------------------
# -----------------------------------------------------------------

# There is a way to import data from a CSV file using the 'SQL Shell (psql)'
# using the next command line

# \copy table_name FROM csv_file_path WITH DELIMITER ',' CSV HEADER;

# Note: Working with a path in a shell there must be added '\\' for every 
# '\' to make it work like in the next example

# '\copy sales FROM 'C:\\Users\\Wilfred M PRO\\Desktop\\portfolio\\study\\PostgreSQL-python\\resources\\company_sales.csv' WITH DELIMITER ',' CSV HEADER;'

# That command line imports the CSV file into the table 'sales' from the
# 'company_sales' database

# To check the definition of the comuns of the table there can be used the 
# '\d sales' command

# -----------------------------------------------------------------
# ----------------- PostgreSQL fetch data from a ------------------
# --------------------- database using Python ---------------------
# -----------------------------------------------------------------

connection = psycopg2.connect(
    database = 'company_sales',
    user = 'wm',
    password = '2828',
    host = 'localhost',
    port = '5432'
)

cursor = connection.cursor()

cursor.execute('SELECT * FROM sales LIMIT 10')
print (cursor.fetchall())
# A SQL query is meant to be executed and it will return a set of 
# values ment to be seen using the 'cursor.fetchall()' method


connection.close()

# -----------------------------------------------------------------
# ------------------ PostgreSQL record data in a ------------------
# --------------------- database using Python ---------------------
# -----------------------------------------------------------------

connection = psycopg2.connect(
    database = 'company_sales',
    user = 'wm',
    password = '2828',
    host = 'localhost',
    port = '5432'
)

cursor = connection.cursor()

cursor.execute('''INSERT INTO sales (order_num, order_type, cus_name, prod_number, prod_name, quantity, price, discount, order_total)
                VALUES (5000,'PYTHON','PYTHON','PYTHON','PYTHON',5000,5000,5000,5000)''')
# There has been created a SQL query which wont have effect until 
# commited that is meant to be executed

connection.commit ()
# The '.commit()' method allows to commit every query stored in the current
# connection

cursor.execute('''SELECT s.cus_name, s.prod_number FROM sales s WHERE order_type = 'PYTHON' ''')
print (cursor.fetchall())
# A SQL query is meant to be executed and it will return a set of 
# values ment to be seen using the 'cursor.fetchall()' method
connection.close()

# This way there can be inserted data in a table within a database with PSQL

# Every query can be executed either on a Python script using this methods
# or within the 'SQL Shell (psql)' terminal

# -----------------------------------------------------------------
# ----------------- PostgreSQL Python interactions ----------------
# -------------------- with a Postgres database -------------------
# -----------------------------------------------------------------

# Several interacion with Python can allow to manage PostgreSQL databases
# and

def insert_sale (connection,order_num,order_type,cus_name,prod_number,prod_name,quantity,price,discount):
    order_total = quantity * price
    if discount != 0:
        order_total = order_total * discount
    sale_data = (order_num,order_type,cus_name,prod_number,prod_name,quantity,price,discount,order_total)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO sales (order_num, order_type, cus_name, prod_number, prod_name, quantity, price, discount, order_total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',sale_data)
    connection.commit()
    cursor.execute('''SELECT s.cus_name, s.order_total FROM sales s WHERE order_num = %s''',(order_num,))
    rows = cursor.fetchall()
    for row in rows:
        print ('Costumer name: ',row[0])
        print ('Total Order: ',row[1])

if __name__ == '__main__':
    connection = psycopg2.connect(
    database = 'company_sales',
    user = 'wm',
    password = '2828',
    host = 'localhost',
    port = '5432')
    order_num = int(input('Input order_num\n'))
    order_type = input('Input order_type\n')
    cus_name = input('Input cus_name \n')
    prod_number = input('Input prod_number\n')
    prod_name = input('Input prod_name\n')
    quantity = input('Input quantity\n')
    price = float(input('Input price\n'))
    discount  = float(input('Input discount\n'))
    insert_sale (connection,order_num,order_type,cus_name,prod_number,prod_name,quantity,price,discount)
    connection.close()

# Example
insert_sale(connection,5003,'PYTHON-Course','PYTHON-Course','PYTHON-Course','PYTHON-Course',5002,5002,5002)

# -----------------------------------------------------------------
# ------------------- PostgreSQL SQLAlchemy core ------------------
# ------------------ interaction with a Postgres ------------------
# -----------------------------------------------------------------

# SQLAlcchemy can work with PostgreSQL to execute every functionallity
# If there's any doubt on how SQLAlchemy works go to the 'SQLAlchemy'
# repository on https://github.com/WilfredM94code/
from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table,Column,String,MetaData

engine = create_engine ("postgresql://wm:2828@localhost/company_sales")

# Writing data in a table
with engine.connect() as connection:
    meta = MetaData(engine)
    sales_table = Table ('sales', meta, autoload=True, autoload_with = engine)
    adding_record = sales_table.insert().values(order_num = 5004,
    order_type = 'Some order type',
    cus_name = 'Some user',
    prod_number = 'Some prod number',
    prod_name = 'Some product name',
    quantity = 5,
    price = 100,
    discount = 0,
    order_total = 500
    )
    connection.execute(adding_record)

# Reading data in a table
with engine.connect() as connection:
    meta = MetaData(engine)
    sales_table = Table ('sales', meta, autoload=True, autoload_with = engine)
    select_statement = sales_table.select().limit(10)
    result_set = connection.execute(select_statement)
    for result in result_set:
        print('Reading: ',result)


# Updating data in a table
with engine.connect() as connection:
    meta = MetaData(engine)
    sales_table = Table ('sales', meta, autoload=True, autoload_with = engine)
    # Check for value
    select_statement = sales_table.select().where(sales_table.c.order_num == 5004)
    result_set = connection.execute(select_statement)
    for result in result_set:
        print('Reading actual value: ',result)    
    update_statement = sales_table.update().where(sales_table.c.order_num == 5004).values(quantity = 5, order_total = 20)
    connection.execute(update_statement)
    # Check for updated value
    select_statement = sales_table.select().where(sales_table.c.order_num == 5004)
    result_set = connection.execute(select_statement)
    for result in result_set:
        print('Reading updated value: ',result)

# Deleting data in a table
with engine.connect() as connection:
    meta = MetaData(engine)
    sales_table = Table ('sales', meta, autoload=True, autoload_with = engine)
    delete_statement = sales_table.delete().where(sales_table.c.order_num == 5004)
    connection.execute(delete_statement)
    # Confirming delete
    select_statement = sales_table.select().where(sales_table.c.order_num == 5004)
    result_set = connection.execute(select_statement)
    print ('Deleted: ', result_set.rowcount)

# -----------------------------------------------------------------
# ------------------- PostgreSQL SQLAlchemy ORM -------------------
# ------------------ interaction with a Postgres ------------------
# -----------------------------------------------------------------

# SQLAlcchemy ORM can work with PostgreSQL to execute every functionallity
# If there's any doubt on how SQLAlchemy works go to the 'SQLAlchemy'
# repository on https://github.com/WilfredM94code/

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine ("postgresql://wm:2828@localhost/company_sales")
Base = declarative_base(engine)
Base.metadata.reflect(engine)

class Sales(Base):
    __table__ = Base.metadata.tables['sales']
    def __repr__(self):
        return '''<Sales(order_num = '{0}', order_type = '{1}', cus_name = '{2}',
        prod_number = '{3}', prod_name = '{4}', quantity = '{5}', price = '{6}', 
        discount = '{7}', order_total = '{8}')>'''.format(self.order_num, self.order_type,
                                                        self.cus_name, self.prod_number,
                                                        self.prod_name, self.quantity, self.price,
                                                        self.discount, self.order_total)


def load_session():
    Session = sessionmaker(bind = engine)
    session = Session()
    return session

# Reading data in a table
session = load_session()
smallest_sales = session.query(Sales).order_by(Sales.order_total).limit(10)
print (smallest_sales[0].cus_name)

# Inserting data in a table
insert_sale = Sales(order_num = 5007,
    order_type = 'Some order type',
    cus_name = 'Some user',
    prod_number = 'Some prod number',
    prod_name = 'Some product name',
    quantity = 5,
    price = 100,
    discount = 0,
    order_total = 500
    )
print (insert_sale)
session.add(insert_sale)
session.commit()
# Reading data in a table to check for insert
smallest_sales = session.query(Sales).where(Sales.order_num == 5007)
print (smallest_sales[0])


# Update data in a table
insert_sale.quantity = 4
insert_sale.order_total = 300
session.commit()
updated_sale = session.query(Sales).filter(Sales.order_num == 5007).first()
# Reading data in a table to check for insert
smallest_sales = session.query(Sales).where(Sales.order_num == 5007)
print (smallest_sales[0])


# Delete data in a table
returned_sale = session.query(Sales).filter(Sales.order_num == 5007).first()
session.delete(returned_sale)
session.commit()
# Reading data in a table to check for insert
smallest_sales = session.query(Sales).where(Sales.order_num == 5007).first()
print (smallest_sales)

# -----------------------------------------------------------------
# ----------------- PostgreSQL stored procedures ------------------
# -----------------------------------------------------------------

# Stored procedures are SQL queries that can be stored to be reused 
# whenever an user call it

# These procedures have to be written in the 'SQL Shell (psql)' prompt

# Note: while creating a procedure the only line meant to end with ';'
# is the one that ends the statement

# There will be created a procedure to simulate a case where a client
# wants to retrive a product back

# 'CREATE PROCEDURE return_nodiscounted_item(INT,INT)
# LANGUAGE plpgsql
# AS $$
# BEGIN
# UPDATE sales
# SET quantity = quantity - $2, order_total = order_total - price * $2
# WHERE prder_num = $1 AND discount = 0;
# COMMIT;
# END;
# $$;
# '

# To the use such procedure there has to be called using the next statement

# 'CALL return_nodiscounted_item(order_number,quantity)'
# Where order_number has to be an actual 'order_number' within the table
# and a quantity related to such sale, in this case the line will be

# 'CALL return_nodiscounted_item(5008,1)'

# -----------------------------------------------------------------
# ------------------ PostgreSQL calling Postgres ------------------
# ----------------- stored procedures with Python -----------------
# -----------------------------------------------------------------

import psycopg2

connection = psycopg2.connect(
    database = 'company_sales',
    user = 'wm',
    password = '2828',
    host = 'localhost',
    port = '5432'
)
connection.autocommit = True
#This 'connection.autocommit' attribute allows to commit every executed
# statemet
cursor = connection.cursor()
cursor.execute ('''CALL return_nodiscounted_item(5008,1)''')
cursor.execute ('''SELECT * FROM sales WHERE order_num = 5008''')
print(cursor.fetchall())

# -----------------------------------------------------------------
# ------------------ PostgreSQL calling Postgres ------------------
# --------------- stored procedures with SQLAlchemy ---------------
# ------------------------------ core -----------------------------
# -----------------------------------------------------------------

from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table,MetaData

engine = create_engine ("postgresql://wm:2828@localhost/company_sales")

with engine.connect() as connection:
    meta = MetaData(engine)
    sales_table = Table ('sales', meta, autoload=True, autoload_with = engine)
    connection.execute('COMMIT')
    connection.execute('CALL return_nodiscounted_item(%s,%s)',(5008,-7))
    select_statement = sales_table.select().where(sales_table.c.order_num == 5008)
    result_set = connection.execute(select_statement)
    for result in result_set:
        print('Reading: ',result)

# -----------------------------------------------------------------
# ------------------ PostgreSQL calling Postgres ------------------
# --------------- stored procedures with SQLAlchemy ---------------
# ------------------------------ ORM ------------------------------
# -----------------------------------------------------------------

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine ("postgresql://wm:2828@localhost/company_sales")
Base = declarative_base(engine)
Base.metadata.reflect(engine)

class Sales(Base):
    __table__ = Base.metadata.tables['sales']
    def __repr__(self):
        return '''<Sales(order_num = '{0}', order_type = '{1}', cus_name = '{2}',
        prod_name = '{4}', quantity = '{5}', order_total = '{8}')>'''.format(self.order_num, self.order_type,
                                                        self.cus_name, self.prod_name,
                                                        self.quantity, self.order_total)

with engine.connect() as connection:
    # Calling the stored procedure
    connection.execute('COMMIT')
    connection.execute('CALL return_nodiscounted_item (%s,%s)',(5008,-1))
    # Check the values update    
    select_statement = sales_table.select().where(sales_table.c.order_num == 5008)
    result_set = connection.execute(select_statement)
    for result in result_set:
        print('Reading updated value: ',result)

