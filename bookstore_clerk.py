import sqlite3
import sys  # To exit a Python script with a status code


# ============================================ FUNCTIONS ====================================================

def connect_to_database(file_name):
    # Function to connect to a database named file_name.
    return sqlite3.connect(file_name + ".db")


def insert_initial_data():
    # Run function after table books has been created to input initial data (which cannot already be in the table).
    cursor.executemany("""INSERT INTO books VALUES(?,?,?,?)""",
                       [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                        (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                        (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
                        (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
                        (3005, "Alice in Wonderland", "Lewis Carroll", 12)])
    conn.commit()


def menu():
    # User menu function which returns the menu choice the user selected.
    return input("""
    Welcome to the bookstore clerk's program.
    Please choose from one of the following options by typing it's number:
    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    0. Exit
    """)


def valid_columns_in_books_table():
    # Creates a list of valid column names for table 'books' to reduce risk of injection hacks.
    cursor.execute("""PRAGMA table_info(books)""")
    valid = [header_details[1] for header_details in cursor]
    # cursor object invokes fetchall() automatically.
    return valid


def id_in_books_table():
    # Creates a list of all ids in table 'books'.
    cursor.execute("""SELECT id FROM books""")
    id_list = [entry[0] for entry in cursor]
    return id_list


def update_column():
    # Function updates the book 'book_to_be_updated' in attribute 'column_name' in table 'books'.
    # The entry is updated to 'update_info'. A completion message is then returned.
    # Function allows only a limited set of column names (generated by function 'valid_columns_in_books_table')
    # to be used in the SQL statement to reduce the risk of injection hacks.
    if column_name not in valid_columns_in_books_table():
        raise ValueError("Invalid column name")
    cursor.execute("""UPDATE books SET {}=? WHERE id = ?""".format(column_name),
                   (update_info, book_to_be_updated_id))
    conn.commit()
    return "Update successful."


def exit_script():
    sys.exit(0)


def zero_or_enter_choice(reason):
    # When the user inputs incorrectly the function provides the 'reason' to help correct the input and then
    # allows the user two options: to return to the main menu or try again.
    # It also considers if either of these two options are entered wrong then the function 'user_quit_option' runs.
    user_choice = input(f"{reason} Type 0 to return to main menu or enter to try again. ")
    if user_choice == "0":
        pass
    elif user_choice == "":
        global return_to_loop
        # global allows me to modify the outer scope variable return_to_loop within this inner scope.
        # Without it, I would be creating a return_to_loop variable here (in the inner scope) which has nothing
        # to do with the variable under the same name in the other scope.
        return_to_loop = True
    else:
        user_quit_choice()
    return user_choice


def user_quit_choice():
    # When the user has incorrectly inputted twice in a row, function allows them the option to quit the program.
    user_input = input("You have entered an invalid input. Do you wish to quit the program? (y/n) ")
    if user_input == "n":
        pass
    elif user_input == "y":
        exit_script()
    else:
        print("Invalid input, the program will now quit. ")
        exit_script()


# ============================================ CODE ====================================================
# Connecting to the database and establishing a cursor to interactive with the database.
conn = connect_to_database("ebookstore")
cursor = conn.cursor()

# Creating main table (if not exists) called books
cursor.execute("""CREATE TABLE IF NOT EXISTS books
(id INTEGER PRIMARY KEY,
Title TEXT NOT NULL,
Author TEXT DEFAULT unknown,
Qty INTEGER DEFAULT 0)""")

print(id_in_books_table())
print(type(id_in_books_table()[1]))

return_to_loop = False
book_to_be_updated_id = None        # I have done this to get rid of the error that this variable could be undefined.

while True:
    return_to_main_menu = False     # Variable defined here so each time it resets when the program returns to menu.
    user_menu_option = menu().strip(".").strip(" ")
    # Strip method removes error if user enters a dot/ space bar after there number choice.

    if user_menu_option == "0":
        # try-accept here for closing the database or could put whole loop in try and then
        break

    if user_menu_option == "1":
        # Info from users about book to be added, while loops to ensure unique id and correct value types are given.
        while True:
            try:
                # Could add a feature which gives a suggested book id.
                enter_id = int(input("Book id: "))
                if enter_id in id_in_books_table():
                    print("This number is already a book id. Try again. ")
                    continue
                break

            except ValueError as e:
                if zero_or_enter_choice("Please enter a valid book id - it must be a unique integer. ") == "0":
                    # edit - to make option of n after second incorrect input lead back to the main menu.
                    return_to_main_menu = True
                    break
                continue

        if return_to_main_menu:
            continue

        enter_title = input("Book title:  ")
        enter_author = input("Author's name: ")

        while True:
            try:
                enter_qty = int(input("Book quantity: "))
                break
            except ValueError as e:
                print("Quantity of books must be an integer. Try again. ")

        # Adding record to table books.
        cursor.execute("""INSERT INTO books VALUES (?,?,?,?)""", (enter_id, enter_title, enter_author, enter_qty))
        # I believe that enter_id will always be defined... pyCharm doesn't agree... not sure why.
        conn.commit()
        print("Entry successful.")

    if user_menu_option == "2":
        while True:
            try:
                book_to_be_updated_id = int(input("What is the id of the book you wish to update? "))
                if book_to_be_updated_id in id_in_books_table():
                    print("This number is already a book id. Try again with a unique integer.")
                    continue
                # could add feature that suggests a book id number
                break

            except ValueError as e:
                zero_or_enter_choice("The book id must be an integer.")
                if return_to_loop:
                    return_to_loop = False
                    continue
                return_to_main_menu = True
                break

        if return_to_main_menu:
            continue

        while True:
            update_author_title_quantity = input(f"What information for book id {book_to_be_updated_id} "
                                                 f"do you want to update? (author/title/quantity) ").strip(" ")

            if update_author_title_quantity == "author":
                update_info = input("What is the new author's name? ")
                column_name = "Author"

            elif update_author_title_quantity == "title":
                update_info = input("What is the new title? ")
                column_name = "Title"

            elif update_author_title_quantity == "quantity":
                update_info = input("What is the updated quantity of the book? ")
                column_name = "Qty"

            else:
                zero_or_enter_choice("Please select a valid option. ")
                if return_to_loop:
                    return_to_loop = False
                    continue
                return_to_main_menu = True
                break

            print(update_column())      # Updates the database through function.
            break

    if user_menu_option == "3":
        # Option to delete a book
        while True:
            try:
                book_id_delete = int(input("What is the id of the book you want to delete? "))
                if book_to_be_updated_id not in id_in_books_table():
                    if zero_or_enter_choice("There is no record of books with given id number. ") == "0":
                        # Bug: if I go here and then through to the (n/y) option and then click n.
                        # There is an error in returning to the main menu.
                        return_to_main_menu = True
                        break
                    # Could add - would you like to see current books in the database?
                    continue
                break
            except ValueError:
                zero_or_enter_choice("Invalid book id. ")
                if return_to_loop:
                    return_to_loop = False
                    continue
                return_to_main_menu = True
                break
        if return_to_main_menu:
            continue

        cursor.execute("""DELETE FROM books WHERE id = ?""", (book_id_delete,))
        conn.commit()
        print("Record has been successfully deleted.")

    if user_menu_option == "4":
        while True:
            try:
                search_id = int(input("What is the book id? "))
                if search_id not in id_in_books_table():
                    print("There is no record of books with given id number. Try again.")
                    # Could add would you like to search by name/ title/ quantity.
                    continue
                break
            except ValueError:
                zero_or_enter_choice("Invalid book id. ")
                if return_to_loop:
                    return_to_loop = False
                    continue
                return_to_main_menu = True
                break
        if return_to_main_menu:
            continue

        cursor.execute("""SELECT id, Title, Author, Qty FROM books WHERE id = ?""", (search_id,))
        print("-----------------------------------------------------------------------------------------------------")
        for record in cursor:
            print("id: {}\t Title: {}\t Author: {}\t Quantity: {}\t".format(*record))
        print("-----------------------------------------------------------------------------------------------------")
# After the user has finished using the program (as the loop has been broken from) the connection will close
conn.close()


# Potential edits in the future:
# When adding a book, search in each column that the new information is original,
# i.e. the book isn't already on the database, so no two same books with different id's get added.
