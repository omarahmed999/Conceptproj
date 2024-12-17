import pandas as pd
from datetime import datetime

# Initial data
members = [
    {"id": 101, "name": "Alice Johnson", "email": "alice.johnson@example.com", "borrowing_limit": 5},
    {"id": 102, "name": "Bob Smith", "email": "bob.smith@example.com", "borrowing_limit": 3},
    {"id": 103, "name": "Charlie Davis", "email": "charlie.davis@example.com", "borrowing_limit": 4},
    # More members...
]
members_df = pd.DataFrame(members)

books_dataset = pd.read_csv("books_scraped.csv")
books_dataset['id'] = range(1, len(books_dataset) + 1)
books_dataset_final = books_dataset.head(10)
borrowing_records = []

# Functional functions
def add_book(books_dataset, book_title, book_category, book_rating, price, stock, quantity):
    new_book = {
        'Title': book_title,
        'Book_category': book_category,
        'Star_rating': book_rating,
        'Price': price,
        'Stock': stock,
        'Quantity': quantity,
        'id': len(books_dataset) + 1
    }
    return pd.concat([books_dataset, pd.DataFrame([new_book])], ignore_index=True)

def remove_book(books_dataset, book_title):
    return books_dataset[books_dataset["Title"] != book_title]

def update_book(books_dataset, book_title, **kwargs):
    updated_books = books_dataset.copy()
    if book_title in updated_books["Title"].values:
        for key, value in kwargs.items():
            if key in updated_books.columns:
                updated_books.loc[updated_books["Title"] == book_title, key] = value
    return updated_books

def search_book(books_dataset, keyword):
    return books_dataset[books_dataset["Title"].str.contains(keyword, case=False)]

def register_member(members_df, name, email, borrowing_limit):
    new_id = members_df["id"].max() + 1 if not members_df.empty else 1
    new_member = {"id": new_id, "name": name, "email": email, "borrowing_limit": borrowing_limit}
    return pd.concat([members_df, pd.DataFrame([new_member])], ignore_index=True)

def borrow_book(books_dataset, members_df, borrowing_records, book_id, member_id):
    if book_id in books_dataset["id"].values and member_id in members_df["id"].values:
        book = books_dataset.loc[books_dataset["id"] == book_id]
        member = members_df.loc[members_df["id"] == member_id]

        if book.iloc[0]["Quantity"] > 0:
            borrowing_record = {
                "Book ID": book_id,
                "Member ID": member_id,
                "Borrow Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            updated_books = books_dataset.copy()
            updated_books.loc[updated_books["id"] == book_id, "Quantity"] -= 1
            return updated_books, borrowing_records + [borrowing_record]
        else:
            print(f"Book '{book.iloc[0]['Title']}' is out of stock.")
    return books_dataset, borrowing_records

def display_available_books(books_dataset):
    return books_dataset[books_dataset["Quantity"] > 0]

def view_borrowing_history(borrowing_records):
    return pd.DataFrame(borrowing_records)

# Functional menu system
def handle_choice(choice, books, members, records):
    if choice == "1":
        title = input("Enter book title: ")
        category = input("Enter book category: ")
        rating = float(input("Enter book rating: "))
        price = float(input("Enter book price: "))
        stock = input("Enter stock status: ")
        quantity = int(input("Enter quantity: "))
        books = add_book(books, title, category, rating, price, stock, quantity)
        print("Book added successfully.")
    elif choice == "2":
        title = input("Enter book title to remove: ")
        books = remove_book(books, title)
        print("Book removed successfully.")
    elif choice == "3":
        title = input("Enter book title to update: ")
        field = input("Enter field to update (Title, Book_category, Star_rating, Price, Stock, Quantity): ")
        value = input("Enter new value: ")
        if field in ["Star_rating", "Price", "Quantity"]:
            value = float(value) if field != "Quantity" else int(value)
        books = update_book(books, title, **{field: value})
        print("Book updated successfully.")
    elif choice == "4":
        keyword = input("Enter keyword to search: ")
        results = search_book(books, keyword)
        print(results)
    elif choice == "5":
        name = input("Enter member name: ")
        email = input("Enter member email: ")
        borrowing_limit = int(input("Enter borrowing limit: "))
        members = register_member(members, name, email, borrowing_limit)
        print("Member registered successfully.")
    elif choice == "6":
        book_id = int(input("Enter book ID to borrow: "))
        member_id = int(input("Enter member ID: "))
        books, records = borrow_book(books, members, records, book_id, member_id)
        print("Book borrowed successfully.")
    elif choice == "7":
        available_books = display_available_books(books)
        print(available_books)
    elif choice == "8":
        history = view_borrowing_history(records)
        print(history)
    elif choice == "9":
        print("Exiting the system. Goodbye!")
        return books, members, records, False
    else:
        print("Invalid choice. Please try again.")
    return books, members, records, True

# Run functional program
def main():
    books = books_dataset_final.copy()
    members = members_df.copy()
    records = []
    running = True

    while running:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Update Book")
        print("4. Search Books")
        print("5. Register Member")
        print("6. Borrow Book")
        print("7. Display Available Books")
        print("8. View Borrowing History")
        print("9. Exit")

        choice = input("Enter your choice: ")
        books, members, records, running = handle_choice(choice, books, members, records)

if __name__ == "__main__":
    main()
