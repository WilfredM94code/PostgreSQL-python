''' Tasks
1- Create a library DB to store authors and their books
2- The DB will have 3 table; authors, books, authorbooks
3- The Authors table will have the following columns; id, first name & last name
4- The Books table will have the following columns; id, title & number of pages
5- The AuthorBooks table will have the following columns; id, author id & book id

-- Separating the author books allows us to easily store multiple books by the same author. 
-- For books with multiple authors, multiple entries would be added to the authorbooks table

-- Once the database is created with the necessary tables, you will add functionality to add a new book to the DB. The following operations must be added.

6- The books table should be updated with the new book
7- if author is a new author, then authors table should be updated to include the new author, if the author is not a new author, then the author will not be added to the authors table again
8- You will also add a new pairing to the authorbooks table
9- all these operations must be done within a transaction, so the DB will never end up in a half done state. for this you can use stored procedures or transactions

---------------------------------------------------
You can use psycopg2 module, SQLAlchemy Core or SQLAlchemy ORM.
My Solution will focus on SQLAlchemy ORM '''

# Function DEF
def table_check (cursor):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS books(
            book_id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            edition INT NOT NULL,
            country TEXT NOT NULL,
            editorial TEXT NOT NULL,
            year INT NOT NULL,
            pages INT NOT NULL,
            volume INT NOT NULL,
            volume_total INT NOT NULL,
            isbn TEXT UNIQUE
            );
    ''')
    # connection.commit ()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors(
            author_id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
            );
    ''')
    # connection.commit ()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS authorbooks(
            book_id INT REFERENCES books(book_id),
            author_id INT REFERENCES authors(author_id),
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
            );
    ''')


def check_author(first,last,book_id):
    while True:
        query = f'''SELECT author_id
        FROM authors
        WHERE
        first_name = '{first}' AND last_name = '{last}';
        '''
        cursor.execute(query)
        connection.commit ()
        author_id = cursor.fetchall()[:]
        if len(author_id) == 0:
            query = f'''INSERT INTO authors 
            (first_name,last_name)
            VALUES
            ('{first}','{last}')
            RETURNING
            author_id
            ;'''
            cursor.execute(query)
            connection.commit ()
            author_id = cursor.fetchall()[0][0]
        elif len(author_id) != 0:
            query = f'''INSERT INTO authorbooks 
            (book_id,author_id,first_name,last_name)
            VALUES ('{book_id}','{author_id[0][0]}','{first}','{last}')
            '''
            cursor.execute(query)
            connection.commit ()
            return author_id[0][0]

def check_book (book_info):
    while True:
        query = f'''INSERT INTO books(
        title,
        edition,
        country,
        editorial,
        year,
        pages,
        volume,
        volume_total,
        isbn
        )
        VALUES(
        '{book_info['title']}',
        {book_info['edition']},
        '{book_info['country']}',
        '{book_info['editorial']}',
        {book_info['year']},
        {book_info['pages']},
        {book_info['volume']},
        {book_info['volume_total']},
        '{book_info['isbn']}')
        RETURNING
        book_id
        ;'''
        cursor.execute(query)
        connection.commit ()
        book_id = cursor.fetchall()[0][0]
        return book_id


def new_book_save_1 (book_info):
    # Data preparing
    book_id = check_book (book_info)
    for first,last in zip(book_info['author_first_name'], book_info ['author_last_name']):
        check_author(first,last,book_id)


def new_book_input ():
    book_info = {
    'title' : None,
    'edition' : None,
    'country' : None,
    'editorial' : None,
    'year' : None,
    'pages' : None,
    'volume' : None,
    'volume_total' : None,
    'isbn' : None,
    'author_first_name' : [],
    'author_last_name' : []
    }
    while True:
        author_names = ', '.join([first + ' ' + last for first,last in zip(book_info['author_first_name'], book_info ['author_last_name'])])
        if author_names == '':
            author_names = None
            print (book_info['author_first_name'])
            print (book_info ['author_last_name'])
        try:
            opt = input (f'''Input book data
            0 - Title : {book_info['title']}
            1 - Author/s : {author_names}
            2 - Edition : {book_info ['edition']}
            3 - Country : {book_info ['country']}
            4 - Editorial : {book_info ['editorial']}
            5 - Year : {book_info ['year']}
            6 - Number of pages : {book_info ['pages']}
            7 - Volume : {book_info ['volume']}
            8 - Total volume : {book_info ['volume_total']}
            9 - ISBN : {book_info ['isbn']}
            S - Save
            X - Exit\n''')
            try:
                opt = int(opt)
                if opt in range (0,10):
                    if opt == 0:
                        book_info ['title'] = input ('Input title\n')
                    elif opt == 1:
                        auth_opt = input('''0 - Add\n1 - Edit\n2 - Delete\n''')
                        try:
                            auth_opt = int (auth_opt)
                            if auth_opt == 0:
                                book_info ['author_first_name'].append (input ("Input author's first name\n"))
                                book_info ['author_last_name'].append (input ("Input author's last name\n"))
                            elif auth_opt == 1 or auth_opt == 2:
                                print ('Select an option:')
                                author_list = [first + ' ' + last for first,last in zip(book_info['author_first_name'], book_info ['author_last_name'])]
                                for index,item in enumerate(author_list):
                                    print (f'{index} : {item}')
                                edit_opt = int(input ('\nInput an option\n'))
                                if auth_opt == 1:
                                    book_info ['author_first_name'][edit_opt] = input ("Input author's first name\n")
                                    book_info ['author_last_name'][edit_opt] = input ("Input author's last name\n")
                                elif auth_opt == 2:
                                    book_info ['author_first_name'].pop(edit_opt)
                                    book_info ['author_last_name'].pop(edit_opt)
                            else:
                                print ('Input an useful value')
                        except:
                            print ('Input an useful value')
                    elif opt == 2:
                        book_info ['edition'] = input ('Input edition\n')
                    elif opt == 3:
                        book_info ['country'] = input ('Input country\n')
                    elif opt == 4:
                        book_info ['editorial'] = input ('Input editorial\n')
                    elif opt == 5:
                        book_info ['year'] = input ('Input year\n')
                    elif opt == 6:
                        book_info ['pages'] = input ('Input total pages\n')
                    elif opt == 7:
                        book_info ['volume'] = input ('Input volume\n')
                    elif opt == 8:
                        book_info ['volume_total'] = input ('Input total volumes\n')
                    elif opt == 9:
                        book_info ['isbn'] = input ('Input ISBN\n')
                else:
                    print ('Input an useful value')
            except:
                if opt.lower() == 's':
                    new_book_save_1 (book_info)
                    print ('Data saved')
                    break
                elif opt.lower() == 'x':
                    break
                else:
                    print ('Input an useful value')
        except KeyboardInterrupt:
            print ('Input ended')
            break


# 1st approach psycopg2
import psycopg2

name_Database   = "first_approach"

while True:
    try:
        connection = psycopg2.connect(
            database = name_Database,
            user = 'wm',
            password = '2828',
            host = 'localhost',
            port = '5432')
        cursor = connection.cursor()
        print ('Connected to database')
        connection.autocommit = True
        table_check (cursor)
        new_book_input ()
        connection.close ()
        break
    except:
        print ('Creating database')
        connection = psycopg2.connect(
            database = 'postgres',
            user = 'wm',
            password = '2828',
            host = 'localhost',
            port = '5432')
        # Obtain a DB Cursor
        connection.autocommit = True
        cursor = connection.cursor()
        # Create table statement
        query = 'DROP DATABASE IF EXISTS ' + name_Database+";"
        cursor.execute(query)
        query = "CREATE DATABASE "+name_Database+";"
        # Create a table in PostgreSQL database
        cursor.execute(query)
        print ('Database created')
        # connection.autocommit = False
        # connection.commit ()
        # Create tables 'authors, books, authorbooks'
        connection.close()



# 2nd approach SQLAlchemy Core

# 3rd approach SQLAlchemy ORM




