Assignment 2- Library inventory & borrowing System
Kirti Khatri
2501201005
BCA(AI/DS)
sem 1

#Library Book Manager- Python CLI

#Add a new book
def add_book():
    title = input("Python programming: ")
    author = input("John Smith: ")
    book_id = input("B101: ")
    book={"title": title, "author": author, "book_id": book_id, "available": True, "borrower": None}
    books.append(book)
    print(f"Book '{title}' added successfully.")

#View all books
def view_books():
    if not books:
        print("No books in the inventory.")
        return
    for book in books:
        status = "Available" if book["available"] else f"Borrowed by {book['borrower']}"
        print(f"ID: {book['book_id']}, Title: {book['title']}, Author: {book['author']}, Status: {status}")

#Borrow a book
def borrow_book():
    book_id = input("B101: ")
    borrower = input("kirti: ")
    for book in books:
        if book["B101"] == book_id:
            if book["available"]:
                book["available"] = False
                book["kirti"] = borrower
                print(f"You have borrowed '{book['title']}'.")
            else:
                print(f"Sorry, '{book['title']}' is currently borrowed by {book['borrower']}.")
            return
    print("Book ID not found.")

#Return a book
def return_book():
    book_id = input("B101: ")
    for book in books:
        if book["book_id"] == book_id:
            if not book["available"]:
                book["available"] = True
                book["borrower"] = None
                print(f"You have returned '{book['title']}'.")
            else:
                print(f"'{book['title']}' was not borrowed.")
            return
    print("Book ID not found.")

#update records

def update_book():
    book["available"] = True
    book["borrower"] = None
    print("Book returned successfully.")

#Main Menu
def menu():
    while True:
        print("\nLibrary Book Manager")
        print("1. Add Book")
        print("2. View Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            borrow_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

#Start the program
menu()

