import pandas as pd
import datetime
#imperative
members = [
    {"id": 101, "name": "Alice Johnson", "email": "alice.johnson@example.com", "borrowing_limit": 5},
    {"id": 102, "name": "Bob Smith", "email": "bob.smith@example.com", "borrowing_limit": 3},
    {"id": 103, "name": "Charlie Davis", "email": "charlie.davis@example.com", "borrowing_limit": 4},
    {"id": 104, "name": "Diana Evans", "email": "diana.evans@example.com", "borrowing_limit": 2},
    {"id": 105, "name": "Evan Garcia", "email": "evan.garcia@example.com", "borrowing_limit": 6},
    {"id": 106, "name": "Fiona Harris", "email": "fiona.harris@example.com", "borrowing_limit": 5},
    {"id": 107, "name": "George King", "email": "george.king@example.com", "borrowing_limit": 3},
    {"id": 108, "name": "Hannah Lewis", "email": "hannah.lewis@example.com", "borrowing_limit": 4},
    {"id": 109, "name": "Ian Moore", "email": "ian.moore@example.com", "borrowing_limit": 2},
    {"id": 110, "name": "Julia Perez", "email": "julia.perez@example.com", "borrowing_limit": 6}
]
members_df = pd.DataFrame(members)
borrowing_records = []
#books id , title , 
books_dataset = pd.read_csv("books_scraped.csv")
# print(books_dataset.head())
books_dataset['id'] = range(1 , len(books_dataset )+1)
books_dataset_final = pd.DataFrame(books_dataset[:10])
print(books_dataset_final.info())
#defining datastructures
#________________
def add_book(books_dataset_final, book_title, book_category, book_rating, price, stock, quantity):
    rownew = {'Title': book_title, 'Book_category': book_category,
              'Star_rating': book_rating, 'Price': price, 'Stock': stock, 'Quantity': quantity, 'id' : len(books_dataset_final)+1}
    rownew_df = pd.DataFrame([rownew])
    books_dataset_final = pd.concat([books_dataset_final, rownew_df], ignore_index=True)
    return books_dataset_final

# books_dataset_final = add_books(books_dataset_final , 'omar', '7arre2a' , 'two' , 231 , "In stock" , 123)
# print(books_dataset_final)
def remove_book(books_dataset_final, book_title) :
    i = books_dataset_final[(books_dataset_final.Title == book_title)].index
    books_dataset_final.drop(i, inplace = True)
    return books_dataset_final
# books_dataset_final = remove_books(books_dataset_final , 'omar')
# print(books_dataset_final)
def update_book(books_dataset_final, book_title, **kwargs):
    if book_title in books_dataset_final["Title"].values:
        # Find the index of the book with the given title
        book_index = books_dataset_final[books_dataset_final["Title"] == book_title].index[0]
        
        # Update the book's details based on kwargs
        for key, value in kwargs.items():
            if key in books_dataset_final.columns:
                books_dataset_final.at[book_index, key] = value
            else:
                print(f"Invalid column name: {key}")
    else:
        print(f"Book with title '{book_title}' not found.")
    
    return books_dataset_final
# Update book information (e.g., change price and stock)
# books_dataset_final = update_book_by_name(books_dataset_final, 'Sharp Objects', Quantity=0, Stock="Out of stock")
# print(books_dataset_final)
def search_book(books_dataset_final, keyword):
    results = books_dataset_final[books_dataset_final["Title"].str.contains(keyword, case=False)]
    return results

def register_member(members_df, name, email, borrowing_limit):
    new_id = members_df["id"].max() + 1 if not members_df.empty else 1
    new_member = {"id": new_id, "name": name, "email": email, "borrowing_limit": borrowing_limit}
    members_df = pd.concat([members_df, pd.DataFrame([new_member])], ignore_index=True)
    return members_df

def borrow_book(books_dataset_final, members_df, borrowing_records, book_id, member_id):
    if book_id in books_dataset_final["id"].values and member_id in members_df["id"].values:
        book = books_dataset_final.loc[books_dataset_final["id"] == book_id]
        member = members_df.loc[members_df["id"] == member_id]

        if book.iloc[0]["Quantity"] > 0:
            borrowing_records.append({
                "Book ID": book_id,
                "Member ID": member_id,
                "Borrow Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            books_dataset_final.loc[books_dataset_final["id"] == book_id, "Quantity"] -= 1
        else:
            print(f"Book '{book.iloc[0]['Title']}' is out of stock.")
    else:
        print("Invalid book or member ID.")
    return books_dataset_final, borrowing_records

def display_available_books(books_dataset_final):
    return books_dataset_final[books_dataset_final["Quantity"] > 0]

def view_borrowing_history(borrowing_records):
    return pd.DataFrame(borrowing_records)
while True:
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
        field = input("Enter field to update (Title, Category, Rating, Price, Stock, Quantity): ")
        value = input("Enter new value: ")
        if field in ["Rating", "Price", "Quantity"]:
            value = float(value) if field != "Quantity" else int(value)
        books_dataset_final = update_book(books_dataset_final, book_id, **{field: value})
        print("Book updated successfully.")

    elif choice == "4":
        keyword = input("Enter keyword to search: ")
        results = search_book(books_dataset_final, keyword)
        print(results)

    elif choice == "5":
        name = input("Enter member name: ")
        email = input("Enter member email: ")
        borrowing_limit = int(input("Enter borrowing limit: "))
        members_df = register_member(members_df, name, email, borrowing_limit)
        print("Member registered successfully.")

    elif choice == "6":
        book_id = int(input("Enter book ID to borrow: "))
        member_id = int(input("Enter member ID: "))
        books_dataset_final, borrowing_records = borrow_book(books_dataset_final, members_df, borrowing_records, book_id, member_id)
        print("Book borrowed successfully.")

    elif choice == "7":
        available_books = display_available_books(books_dataset_final)
        print(available_books)

    elif choice == "8":
        # history = view_borrowing_history(borrowing_records)
        if(view_borrowing_history(borrowing_records).empty) :
            print("No borrowing history found")
        else :
            print(view_borrowing_history(borrowing_records))

    elif choice == "9":
        print("Exiting the system. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
