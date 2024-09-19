import operations as oper

# Library Management System
print("Welcome to the Library Management System!")
# UI

def main():
    while True:
        print("Main Menu")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Quit")
        choice = input("What would you like to do? (1-4)")

        if choice == '1':
            oper.book_operations()

        elif choice == '2':
            oper.user_operations()

        elif choice == '3':
            oper.author_operations()

        elif choice == '4':
            print("Quitting, thank you for using the library management system!")
            quit()
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()

