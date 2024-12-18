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

# Helper functions
def add_book(books, book_title, book_category, book_rating, price, stock, quantity):
    new_book = {
        "id": len(books) + 1,
        "Title": book_title,
        "Book_category": book_category,
        "Star_rating": book_rating,
        "Price": price,
        "Stock": stock,
        "Quantity": quantity
    }
    books.append(new_book)
    return books

def remove_book(books, book_title):
    books = [book for book in books if book["Title"] != book_title]
    return books

def update_book(books, book_id, **kwargs):
    for book in books:
        if book["id"] == book_id:
            for key, value in kwargs.items():
                if key in book:
                    book[key] = value
            break
    return books

def search_book(books, keyword):
    return [book for book in books if keyword.lower() in book["Title"].lower()]

def display_available_books(books):
    return [book for book in books if book["Quantity"] > 0]

def borrow_book(books, records, book_id, member_id):
    for book in books:
        if book["id"] == book_id:
            if book["Quantity"] > 0:
                records.append({
                    "Book ID": book_id,
                    "Member ID": member_id,
                    "Borrow Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                book["Quantity"] -= 1
                print(f"Book '{book['Title']}' borrowed successfully.")
            else:
                print(f"Book '{book['Title']}' is out of stock.")
            break
    else:
        print("Book not found.")
    return books, records

def view_borrowing_history(records):
    return records

def register_member(members, name, email, borrowing_limit):
    new_id = max(member["id"] for member in members) + 1 if members else 101
    new_member = {"id": new_id, "name": name, "email": email, "borrowing_limit": borrowing_limit}
    members.append(new_member)
    return members

def view_member_details(members, member_id):
    for member in members:
        if member["id"] == member_id:
            return member
    print("Member not found.")
    return None

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
    print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Enter book title: ")
        category = input("Enter book category: ")
        rating = float(input("Enter book rating: "))
        price = float(input("Enter book price: "))
        stock = input("Enter stock status: ")
        quantity = int(input("Enter quantity: "))
        books_dataset_final = add_book(books_dataset_final, title, category, rating, price, stock, quantity)
        print("Book added successfully.")

    elif choice == "2":
        title = input("Enter book title to remove: ")
        books_dataset_final = remove_book(books_dataset_final, title)
        print("Book removed successfully.")

    elif choice == "3":
        book_id = int(input("Enter book ID to update: "))
        field = input("Enter field to update (Title, Book_category, Star_rating, Price, Stock, Quantity): ")
        value = input("Enter new value: ")
        if field in ["Star_rating", "Price", "Quantity"]:
            value = float(value) if field != "Quantity" else int(value)
        books_dataset_final = update_book(books_dataset_final, book_id, **{field: value})
        print("Book updated successfully.")

    elif choice == "4":
        keyword = input("Enter keyword to search: ")
        results = search_book(books_dataset_final, keyword)
        print(results)

    elif choice == "5":
        book_id = int(input("Enter book ID to borrow: "))
        member_id = int(input("Enter member ID: "))
        if member_id not in [member['id'] for member in members]:
            print("Member not found!")
        else:
            books_dataset_final, borrowing_records = borrow_book(books_dataset_final, borrowing_records, book_id, member_id)


    elif choice == "6":
        available_books = display_available_books(books_dataset_final)
        print(available_books)

    elif choice == "7":
        history = view_borrowing_history(borrowing_records)
        if not history:
            print("No borrowing history found.")
        else:
            print(history)

    elif choice == "8":
        name = input("Enter member name: ")
        email = input("Enter member email: ")
        borrowing_limit = int(input("Enter borrowing limit: "))
        members = register_member(members, name, email, borrowing_limit)
        print("Member registered successfully.")

    elif choice == "9":
        member_id = int(input("Enter member ID to view details: "))
        member_details = view_member_details(members, member_id)
        if member_details:
            print(member_details)

    elif choice == "10":
        print("Exiting the system. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
