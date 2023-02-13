# Bookstore

#### Project Description
Project bookstore.py makes it easy for a bookstore to keep track of the books it holds.
The program utilises SQLite by storing each book's data in a database called 'ebookstore.db'.
The data held for each book is the book's id, title, author and quantity. 
The data is stored in a table called 'books'.
The program has built-in error handling, prevention against injection hacks and 
various looping systems that allow the user always to return to the main menu or quit.


#### What program does 
It allows the staff to:
- Enter the data for a new book
- Update the data of a current book, that is update either:
  - quantity
  - title
  - author
- Delete a book (i.e. store no longer wants to stock it)
- Search for a book to see if it's on the store's system

#### What technologies used
The program uses SQL commands to interact with the database through SQLite.


#### Features to add in the future
* When a user adds a book the program should search each column in the database to check
the book isn't already on the database - this avoids the same books being 
added with different id's.
* Add a function that identifies the last id number added and suggests said number plus 1.
* Add a function that prints all the books to the terminal to show the user what books
are on the system and to show changes take effect.
  * Use this in the delete/ update and search section. 
* In the search section add searching by name/ title or quantity instead of just by book id.
* Limit quantity to positive integers and put more restrictions on possible id numbers.
* Could change like 244 into a function.
* Build a GUI into this


### How to install the project
Download bookstore.py and run the program to use.

### How to use the project
The program works on the user selecting one of the main menu options by typing its number.
The program automatically loops back to the main menu after options have 
been successful or terminated. 
