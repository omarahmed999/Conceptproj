import datetime

# Sample dataset for books
books_dataset_final = [
    {"id": 1, "Title": "Book One", "Book_category": "Fiction", "Star_rating": 4.5, "Price": 12.99, "Stock": "In stock", "Quantity": 10},
    {"id": 2, "Title": "Book Two", "Book_category": "Non-fiction", "Star_rating": 4.0, "Price": 15.99, "Stock": "In stock", "Quantity": 5},
    {"id": 3, "Title": "Book Three", "Book_category": "Mystery", "Star_rating": 4.7, "Price": 10.99, "Stock": "In stock", "Quantity": 8},
    {"id": 4, "Title": "Book Four", "Book_category": "Science", "Star_rating": 3.9, "Price": 9.99, "Stock": "In stock", "Quantity": 2},
    {"id": 5, "Title": "Book Five", "Book_category": "Fantasy", "Star_rating": 5.0, "Price": 20.99, "Stock": "In stock", "Quantity": 7},
]

members = [
    {"id": 101, "name": "Alice Johnson", "email": "alice.johnson@example.com", "borrowing_limit": 5},
    {"id": 102, "name": "Bob Smith", "email": "bob.smith@example.com", "borrowing_limit": 3},
]

borrowing_records = []

# Functional helpers
def add_book(books, book_title, book_category, book_rating, price, stock, quantity):
    return books + [{
        "id": len(books) + 1,
        "Title": book_title,
        "Book_category": book_category,
        "Star_rating": book_rating,
        "Price": price,
        "Stock": stock,
        "Quantity": quantity
    }], books

def remove_book(books, book_title):
    return list(filter(lambda book: book["Title"] != book_title, books)), books

def update_book(books, book_id, **kwargs):
    updated_books = [
        dict(book, **kwargs) if book["id"] == book_id else book for book in books
    ]
    return updated_books, books

def search_book(books, keyword):
    return [book for book in books if keyword.lower() in book["Title"].lower()]

def display_available_books(books):
    return [book for book in books if book["Quantity"] > 0]

def borrow_book(books, records, book_id, member_id):
    updated_books = []
    new_records = records[:]
    
    for book in books:
        if book["id"] == book_id:
            if book["Quantity"] > 0:
                new_records.append({
                    "Book ID": book_id,
                    "Member ID": member_id,
                    "Borrow Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                updated_books.append({**book, "Quantity": book["Quantity"] - 1})
            else:
                updated_books.append(book)
        else:
            updated_books.append(book)
    return updated_books, new_records

def view_borrowing_history(records):
    return records

def return_book(books, records, book_id, member_id):
    updated_books = []
    updated_records = [record for record in records if not (record["Book ID"] == book_id and record["Member ID"] == member_id)]

    book_found = False
    for book in books:
        if book["id"] == book_id:
            book_found = True
            updated_books.append({**book, "Quantity": book["Quantity"] + 1})
        else:
            updated_books.append(book)

    if not book_found:
        return ("Book ID not found.", records)
    
    if len(records) == len(updated_records):
        return ("No matching borrowing record found for this member and book.", records)
    
    return updated_books, updated_records


def register_member(members, name, email, borrowing_limit):
    new_id = max(member["id"] for member in members) + 1 if members else 101
    new_member = {"id": new_id, "name": name, "email": email, "borrowing_limit": borrowing_limit}
    return members + [new_member], members

def view_member_details(members, member_id):
    return next((member for member in members if member["id"] == member_id), None)

# Higher-order function for handling user choices
def handle_choice(choice, books, members, records):
    operations = {
        "1": lambda: add_book(books, *get_input_for_new_book()),
        "2": lambda: remove_book(books, input("Enter book title to remove: ")),
        "3": lambda: update_book(books, int(input("Enter book ID to update: ")), **get_book_update_input()),
        "4": lambda: (search_book(books, input("Enter keyword to search: ")),),
        "5": lambda: borrow_book(books, records, int(input("Enter book ID to borrow: ")), int(input("Enter member ID: "))),
        "6": lambda: (display_available_books(books),),
        "7": lambda: (view_borrowing_history(records),),
        "8": lambda: register_member(members, *get_input_for_new_member()),
        "9": lambda: view_member_details(members, int(input("Enter member ID to view details: "))),
        "10": lambda: return_book(books, records, int(input("Enter book ID to return: ")), int(input("Enter member ID: "))),
    }
    
    return operations.get(choice, lambda: ("Invalid choice. Please try again.",))()

# Helper functions for gathering inputs
def get_input_for_new_book():
    return (
        input("Enter book title: "),
        input("Enter book category: "),
        float(input("Enter book rating: ")),
        float(input("Enter book price: ")),
        input("Enter stock status: "),
        int(input("Enter quantity: "))
    )

def get_book_update_input():
    field = input("Enter field to update (Title, Book_category, Star_rating, Price, Stock, Quantity): ")
    value = input(f"Enter new value for {field}: ")
    if field in ["Star_rating", "Price", "Quantity"]:
        value = float(value) if field != "Quantity" else int(value)
    return {field: value}

def get_input_for_new_member():
    return (
        input("Enter member name: "),
        input("Enter member email: "),
        int(input("Enter borrowing limit: "))
    )

# Sample interaction loop
while True:
    print("\nLibrary Management System")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Update Book")
    print("4. Search Books")
    print("5. Borrow Book")
    print("6. Display Available Books")
    print("7. View Borrowing History")
    print("8. Register Member")
    print("9. View Member Details")
    print("10. Return Book")
    print("11. Exit")

    choice = input("Enter your choice: ")
    
    if choice == "11":
        print("Exiting the system. Goodbye!")
        break

    result = handle_choice(choice, books_dataset_final, members, borrowing_records)

    if isinstance(result, tuple):
        # Unpack the result if it's a tuple
        if len(result) == 2:
            books_dataset_final, borrowing_records = result
        else:
            print(result[0])  # Handle the single value result (like search or view)
    else:
        print(result)
