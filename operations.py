# Book Operations

from database_connection import connect_database
from mysql.connector import Error
from datetime import datetime, timedelta

library = {}

# Book Operations in the menu
def book_operations():
    print("Book Operations")
    print("1. Add a book\n2. Borrow a book\n3. Return a book\n4. Search for a book\n5. Display all books")
    bo_choice = input("Please select an option from above: ")
    if bo_choice == '1':
        print("Add a book")
        add_book(library)
    elif bo_choice == '2':
        print("Borrow a book")
        borrow_book(library)
    elif bo_choice == '3':
        print("Return a book")
        check_in_book(library)
    elif bo_choice == '4':
        print("Search for a book")
        search_book_by_title(library)
    elif bo_choice == '5':
        print("Display all books")
        display_all_books(library)

    else:
        print("Sorry invalid input.")

class Book:
    def __init__(self, title, author, genre, publish_date):
        self.title = title
        self.author = author
        self.genre = genre
        self.publish_date = publish_date
        self.availability = True

    def get_title(self):
        return self.title
    
    def get_author(self):
        return self.author
    
    def get_genre(self):
        return self.genre
    
    def get_publish_date(self):
        return self.publish_date
    
    def borrow_book(self):
        if self.availability == True:
            self.availability = False
            return True
        return False
    
    def return_book(self):
        if self.availability == False:
            self.availability = True
            return True
        return False

# Function to add a book
def add_book(library):
    # User inputted data
    isbn = input("Enter the book ISBN: ")
    title = input("Enter book title: ")
    author = input("Enter authors name: ")
    publish_date = input("Enter book publish date: ")
    availability = True

    # Inserting data into SQL database
    try:
        # Connecting to database
        conn = connect_database()
        if conn is not None:
            cursor = conn.cursor()

            # Checking if there is an author with the name inputted
            cursor.execute("SELECT id FROM authors WHERE name = %s", (author,))
            author_record = cursor.fetchone()

            # If we have a record of the author we gather the id
            if author_record:
                author_id = author_record[0]
            # If no record of the author, we insert the author into the authors table and gather the id from the row we just created
            else:
                cursor.execute("INSERT INTO authors (name) VALUES (%s)", (author,))
                author_id = cursor.lastrowid

            # Setting up the tuple for the execution
            new_book = (title, author_id, isbn, publish_date, availability)

            # Query that is adding the book into the database
            query = """
            INSERT INTO books (title, author_id, isbn, publication_date, availability)
            VALUES (%s, %s, %s, %s, %s)
            """

            # Executing the query that will add the book
            cursor.execute(query, new_book)
            conn.commit()
            print("New book has been added to the database")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function for the user to borrow the book
def borrow_book(library):
    isbn = input("Enter the ISBN of the book you would like to borrow: ")
    user = input("Enter the users name who is borrowing the book: ")
    
    try:
        # Connecting to database
        conn = connect_database()
        if conn is not None:
            cursor = conn.cursor()

            # Checking if there is an author with the name inputted
            cursor.execute("SELECT availability FROM books WHERE isbn = %s", (isbn,))
            book_availability = cursor.fetchone()
            print(book_availability)

            # Checking if the book is available
            if book_availability[0] == 0:
                print("The book you are trying to borrow is currently checked out.")
            else:
                # If the book is available we will set the availability to False and inform the user that it has been checked out
                cursor.execute("UPDATE books SET availability = 0 WHERE isbn = %s", (isbn,))
                print("You have checked out the book! Enjoy your reading.")

            # Shows user the book info that they checked out
            cursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
            book_info = cursor.fetchone()
            print(book_info)

            # Shows the User info to the user who checked the book out and grabs the user if they are in the users table
            cursor.execute("SELECT id FROM users WHERE name = %s", (user,))
            user_record = cursor.fetchone()

            # If there is a record in the users table, we set our variables to be inserted into the borrowed_books table
            if user_record:
                user_id = user_record[0]
                today = datetime.today().date()
                due_date = today + timedelta(weeks=2)
                book_id = book_info[0]
                borrow_date = today
                return_date = due_date
                
                # Query that will insert our variables into the table
                query = """
                INSERT INTO borrowed_books (user_id, book_id, borrow_date, return_date)
                VALUES (%s, %s, %s, %s)
                """

                # Executing the query
                borrowing_book = (user_id, book_id, borrow_date, return_date)
                cursor.execute(query, borrowing_book)
            else:
                print("Please make a user profile before checking out a book.")


            conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function that checks in the book if it has been checked out
def check_in_book(library):
    isbn = input("Enter the ISBN of the book you would like to return: ")

    try:
        # Connecting to database
        conn = connect_database()
        if conn is not None:
            cursor = conn.cursor()

            # Checking if there is a book with the books isbn
            cursor.execute("SELECT id FROM books WHERE isbn = %s", (isbn,))
            book = cursor.fetchone()
            
            # Checks if the book with the provided isbn is in the table
            if book is None:
                print("The book with that isbn can not be found.")
                return
            
            book_id = book[0]
            print(book_id)

            # Checks if the book is inside the borrowed_books table
            cursor.execute("SELECT * FROM borrowed_books WHERE book_id = %s", (book_id,))
            borrowed_book = cursor.fetchone()

            # If the book the user is trying to return is borrowed then it will return it
            if borrowed_book:
                print("Thank you for returning your book!")

                # Sets the availability back True
                cursor.execute("UPDATE books SET availability = 1 WHERE isbn = %s", (isbn,))
                
                # Delete's the book from the borrowed books table
                cursor.execute("DELETE FROM borrowed_books WHERE book_id = %s", (book_id,))
                conn.commit()
                print("The book has been checked in successfully.")
            else:
                print("Sorry that book is not checked out. Check it out in another menu.")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Displays all books to the user
def display_all_books(library):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Query that will find all the books and the authors name for the user to see
            query = """
            SELECT b.id, b.title, a.name, b.isbn, b.publication_date, b.availability
            FROM books b, authors a
            WHERE b.author_id = a.id
            """

            # Executes the query
            cursor.execute(query)

            # Goes through each row and prints the books in the table
            for book in cursor.fetchall():
                print(book)
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            cursor.close()
            conn.close()

# Function that searches the book by the inputted title
def search_book_by_title(library):
    searched_book = input("Please enter the title of the book you would like to search: ")
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Executes the query
            cursor.execute("SELECT * FROM books WHERE title = %s", (searched_book,))

            books = cursor.fetchall()

            # Check if any books were found
            if books:
                # Shows the books with the provided title
                print(f"Books found with title '{searched_book}':")
                for book in books:
                    print(book)
            else:
                print(f"No books found with the title '{searched_book}'.")

        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            cursor.close()
            conn.close()

# User Operations

users = {}

# User operation menu actions
def user_operations():
    print("User Operations")
    print("1. Add a new user\n2. View user details\n3. Display all users")
    uo_choice = input("Please select an option from above: ")
    if uo_choice == '1':
        print("Add a new user")
        add_new_user(users)
    elif uo_choice == '2':
        print("View user details")
        display_user_info(users)
    elif uo_choice == '3':
        print("Display all users")
        display_all_users(users)
    else:
        print("Invalid option.")

class User:
    def __init__(self, name, library_id):
        self.name = name
        self.library_id = library_id
        self.borrowed_books = {}

    def display_user_name(self):
        return self.name
    
    def display_user_library_id(self):
        return self.library_id
    
def add_new_user(users):
    name = input("Please enter the name of the new user: ")
    library_id = input("Enter the library ID of the user: ")

# Inserting data into SQL database
    conn = connect_database()
    if conn is not None:
        try:
            print("Accessing database")
            cursor = conn.cursor()

            # Checking if there are any users with the name provided
            cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
            user_record = cursor.fetchone()

            # If we have a record of the user we gather the id
            if user_record:
                print("User is already in our system!")
            else:
                # If no record found, we add the new user
                print("Inserting new user...")
                query = """
                INSERT INTO users (name, library_id)
                VALUES (%s, %s)
                """
                cursor.execute(query, (name, library_id))
                conn.commit()
                print("New user has been added to the database")

        except Error as e:
            print(f"Error: {e}")
        finally:
                cursor.close()
                conn.close()


# Function that displays the user info with the provided library id
def display_user_info(users):
    selected_user = input("Please enter the Library ID of the user you want to see the details of: ")

    conn = connect_database()
    if conn is not None:
        try:
            print("Accessing database")
            cursor = conn.cursor()

            # Checking if there is a user with the id inputted
            cursor.execute("SELECT id FROM users WHERE library_id = %s", (selected_user,))
            user_record = cursor.fetchone()

            # If we have a record of the user we inform them
            if user_record:
                print("Finding the user...")
                query = """
                SELECT * FROM users WHERE library_id = %s
                """
                cursor.execute(query, (selected_user,))
                user_details = cursor.fetchone()
                print(user_details)
            else:
                print("User is not already in our system!")
                

        except Error as e:
            print(f"Error: {e}")
        finally:
                cursor.close()
                conn.close()

# Displays all users in the library system
def display_all_users(users):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Query to fetch all the users
            query = """
            SELECT id, name, library_id FROM users
            """

            # Executes query
            cursor.execute(query)

            # Prints all the users
            for user in cursor.fetchall():
                print(user)
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            cursor.close()
            conn.close()

# User Operations
def user_operations():
    print("User Operations")
    print("1. Add a new user\n2. View user details\n3. Display all users")
    uo_choice = input("Please select an option from above: ")
    if uo_choice == '1':
        print("Add a new user")
        add_new_user(users)
    elif uo_choice == '2':
        print("View user details")
        display_user_info(users)
    elif uo_choice == '3':
        print("Display all users")
        display_all_users(users)
    else:
        print("Invalid option.")

authors = {}

# Author menu operations
def author_operations():
    print("Author Operations")
    print("1. Add a new author\n2. View author details\n3.Display all authors")
    ao_choice = input("Please select an option from above: ")
    if ao_choice == '1':
        print("Add a new author")
        add_new_author(authors)
    elif ao_choice == '2':
        print("View author details")
        display_author_details(authors)
    elif ao_choice == '3':
        print("Display all authors")
        display_all_authors(authors)

class Author:
    def __init__(self, name, biography):
        self.name = name
        self.biography = biography

    def display_author_name(self):
        return self.name
    
    def display_author_biography(self):
        return self.biography
    
# Function that adds a new author
def add_new_author(authors):
    author_id = input("What is the author id: ")
    name = input("What is the name of the author? ")
    biography = input("Short biography of the author: ")
    
    conn = connect_database()
    if conn is not None:
        try:
            print("Accessing database")
            cursor = conn.cursor()

            # Checking if there is an author with the id inputted
            cursor.execute("SELECT id FROM authors WHERE id = %s", (author_id,))
            author_record = cursor.fetchone()

            # If we have a record of the user we gather the id
            if author_record:
                print("Author is already in our system!")
            else:
                # If no record found, insert the new author
                print("Inserting new author...")
                query = """
                INSERT INTO authors (name, biography)
                VALUES (%s, %s)
                """
                cursor.execute(query, (name, biography))
                conn.commit()
                print("New author has been added to the database")
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            cursor.close()
            conn.close()

# Displays a specified authors details
def display_author_details(authors):
    selected_author = input("Please enter the author ID of the author you want to see the details of: ")
    
    conn = connect_database()
    if conn is not None:
        try:
            print("Accessing database")
            cursor = conn.cursor()

            # Checking if there is an author with the id inputted
            cursor.execute("SELECT id FROM authors WHERE id = %s", (selected_author,))
            user_record = cursor.fetchone()

            # If we have a record of the user we inform them of the details
            if user_record:
                print("Finding the author...")
                query = """
                SELECT * FROM authors WHERE id = %s
                """
                cursor.execute(query, (selected_author,))
                user_details = cursor.fetchone()
                print(user_details)
            else:
                # Tells the user if there is no author in the system
                print("User is not already in our system!")
                

        except Error as e:
            print(f"Error: {e}")
        finally:
                cursor.close()
                conn.close()

# Displays all the authors in the system
def display_all_authors(authors):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Query to grab all the authors in the table
            query = """
            SELECT id, name, biography FROM authors
            """

            # Executes the query
            cursor.execute(query)

            # Prints all the rows in the table, providing all the authors
            for user in cursor.fetchall():
                print(user)
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            cursor.close()
            conn.close()