# Pharmacy-Management-System
A Python based desktop application which allows users to order medicines from the university pharmacy. This project uses Python's Tkinter package to create an appealing GUI and uses SQLite to create and modify the database. 
## Database
The database has 4 tables :<br/>
1. **Medicines** : Consists details about the medicines in stock at the pharmacy.
2. **Student** : Consists details of students currently enrolled at the university. Only the enrolled students are allowed to access the pharmacy through a login system.
3. **Transactions** : Consists details of the transactions made by each student.
4. **OutofStockMeds** : Consists data of medicines that are not in stock.
## Functionalities 
The first page is the login window where students enter their ID and password. In case of incorrect details, the user is prompted to re-enter. On successfully logging in, the user can see the list of medicines currently available at the pharmacy. The user can add medicines to the cart and delete them also. The search bar allows users to search medicine names by a partial or a full match. The price of the medicines is also displayed on the screen. On clicking the 'Buy' button, the user is prompted with a bill on the screen which displays the total amount due. Basic CRUD operations along with triggers are used to access the database. Some tables are also created and updated during runtime.

## Files
1. pharmacy.db is the database
2. Database.py is the backend code
3. Project-FrontEnd.py is the frontend GUI code

This project is a good reference for students pursuing a basic Database Systems course. Such projects are often a part of these courses. 
