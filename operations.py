# Book Operations

library = {}

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

def add_book(library):
    isbn = input("Enter the book ISBN: ")
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    genre = input("Enter book genre: ")
    publish_date = input("Enter book publish date: ")
    library[isbn] = Book(title, author, genre, publish_date)
    print(f"Book: {title}, Author: {author}, Genre: {genre}, Publish Date: {publish_date}")
    print(library)

def borrow_book(library):
    isbn = input("Enter the ISBN of the book you would like to borrow: ")
    user = input("Enter the user who is borrowing the book: ")
    if isbn in library and library[isbn].borrow_book():
        print(f"Book ISBN: '{isbn} checked out to {user}.")
    else:
        print("Book not available or not found")

def check_in_book(library):
    isbn = input("Enter the ISBN of the book you would like to return: ")
    if isbn in library and library[isbn].return_book():
        print(f"Book ISBN: '{isbn}' has been returned")
    else:
        print("The book was not borrowed.")

def display_all_books(library):
    for isbn, book in library.items():
        print(f"ISBN: {isbn}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}, Publish Date: {book.publish_date}, Available: {book.availability}")

def search_book_by_title(library):
    searched_book = input("Please enter the title of the book you would like to search: ")
    if searched_book in library:
        print(f"We found {searched_book} in our library")
    else:
        print(f"We could not find {searched_book} in our library")

# User Operations

users = {}

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
    borrowed_books = {}
    users[library_id] = User(name, borrowed_books)

def display_user_info(users):
    selected_user = input("Please enter the Library ID of the user you want to see the details of: ")
    if selected_user in users:
        user = users[selected_user]
        print(f"Name: {user.display_user_name()}, Library ID: {selected_user}, Borrowed Books: {user.borrowed_books}")

def display_all_users(users):
    for library_id, user in users.items():
        print(f"Library ID: {library_id}, Name: {user.name}, Borrowed Books: {user.borrowed_books}")

# Author Operations
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
    borrowed_books = {}
    users[library_id] = User(name, borrowed_books)

def display_user_info(users):
    selected_user = input("Please enter the Library ID of the user you want to see the details of: ")
    if selected_user in users:
        user = users[selected_user]
        print(f"Name: {user.display_user_name()}, Library ID: {selected_user}, Borrowed Books: {user.borrowed_books}")

def display_all_users(users):
    for library_id, user in users.items():
        print(f"Library ID: {library_id}, Name: {user.name}, Borrowed Books: {user.borrowed_books}")

# Author Operations

authors = {}

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
    
def add_new_author(authors):
    author_id = input("What is the author id: ")
    name = input("What is the name of the author? ")
    biography = input("Short biography of the author: ")
    authors[author_id] = Author(name, biography)

def display_author_details(authors):
    selected_author = input("Please enter the author ID of the author you want to see the details of: ")
    if selected_author in authors:
        author = authors[selected_author]
        print(f"Name: {author.display_author_name()}, Author ID: {selected_author}, Biography: {author.biography}")

def display_all_authors(authors):
    for author_id, author in authors.items():
        print(f"Author ID: {author_id}, Name: {author.name}, Biography: {author.biography}")