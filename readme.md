# Library API

This project manage `Library API` system.

The system consists of those things:

***REST API Server*** that allow the end user connect with the system safely and get info, update info add and delete info.

***Data Base Server*** that contain the data, and allow the CRUD actions.

***OOP Management Classes*** each class manage specific table and allow safely CRUD actions, under the system rules 

----
## Technologies Used

- Python
- FastAPI
- MySQL
- Docker
- Pydantic 

----

### How to ***run*** the Library API
**first** make sure have on your computer those programs:
- python in version >= 3
- docker
- git

**second** run those commend these commends, by order.

***clone the to your one computer***

- `git clone https://github.com/ShlomoShoov/Library.git`

***setting docker and project up:***
*you should navigate to the project folder*

- `docker pull mysql:latest`

- `docker run --name library-sql mysql 
-e MYSQL_ROOT_PASSWORD = secret -e MYSQL_DATABASE = library_db -p 3306:3306 -d mysql:latest`

- `docker start library-sql`

-  `python -m venv .venv`

- `.venv/Scripts/activate`

- `pip install -r req.txt`

***run the server and start the project:***

- `python app/main.py`

**that's all :)**



_____
## Check List to buil this Project:

**&#x2611;** build the files structure \
**&#x2610;** build a basic server and  check connection to data base \
**&#x2610;** build the basic libraries and files **without** write the CRUD functions, just make sure that we can start testing \
**--start coding root by root**\
**&#x2610;** create a test for the root we are do \
**&#x2610;** build the function one by one and router\
**&#x2610;** test this route

---
## Files structure

```
library-api/
│
├── app/
│ ├── main.py 
│ ├── database/
│ │ ├── db_connection.py
│ │ ├── book_db.py
│ │ └── member_db.py
│ │ └── crud_manager.py
│ ├── routes/
│ │ ├── book_routes.py
│ │ ├── member_routes.py
│ │ └── report_routes.py
│ └── logs/
│ └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore
```


---

## Database Information

**Database Name:**  `library_db`
used in mysql

---

## Database Tables

### Table: `books`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| **id**| INT | PRIMARY KEY |  |
| **title** | VARCHAR(50) | NOT NULL |the book title|
| **author** | VARCHAR(50) |NOT NULL | |
| **genre**|ENUM(Fiction, Non-Fiction,Science, History, Other) |  | |
| **is_available**|BOOLEAN | NUT NULL DEFAULT TRUE| |
| **borrowed_by_member_id**|INT | DEFAULT NULL | if null -> the bool is not borrowed|

---

### Table: `members`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| **id**| INT | PRIMARY KEY |  |
| **name** | VARCHAR(50) | NUT NULL |  |
|**email** |VARCHAR(255) |NUT NULL UNIQUE | |
|**is_active** |BOOLEAN | NOT NULL  DEFAULT TRUE |does the member active and can barrow books |
|**total_borrows** |INT |NUL NULL DEFAULT 0 | |


---

## System Rules

1. ***creating a book*** -> the user send post with  `title/author/genre` the system add. default : `is_available=True` , `borrowed_by=NULL`
2.  ***allowed genre values*** -> `Fiction / Non-Fiction / Science / History / Other` , any other will return an error
3. ***creating a member*** -> the user send post with `name/email` 
default; `is_active=True, total_borrows=0`
4. ***email uniqueness*** -> has to be unique, (don't try to open a second account so you can barrow more books!)
5. ***inactive members*** -> can not barrow books (you are basically ***inactive***!)
6. ***borrowing already-borrowed books*** Don't do it, You'll get an error
7. ***maximum books per member*** 3, don't try to barrow more!
8. ***who can return a book*** only the one who had borrowed it (we are trying to stay logical...)

---

## API Endpoints

### Books Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST |/books | create book | dict[NewBookModel] | 201(created) / 422 (unsupported values)  |
| GET |/books|see all books | |list[dict] |
| GET | /books/{id} | see specific book  |  | dict(id found) / 404(id not found) |
| PUT | /books/{id} | update book details | dict(UpdateBookModel)  | 200(everything went well) / 422(unsupported or invalid params )/ 404(book not exist) |
| PUT| /books/{id}/borrow/{member_id} | borrow book |   | 200(all went well) / 404(book or member not found) /  409(book is already borrowed or inactive member or over-borrow books (>3))|
| PUT | /books/{id}/return/{member_id} | return book | | 200(all went well) /  404(book or member not exists) / 409(the member is not borrowed this book) |

---

### Members Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
|POST| /members | create member | dict(NewMemberModel) | 201(all went well) / 409(email is already exists)| 
|GET|/members | see all members| | list(dict)|
|GET| /members/{id} | see specific member | | 200 (dict) / 404 (not exist)|
|PUT| /members/{id} | update member details | dict(UpdateMemberModel) | 200(all went well) / 404(member not exists) / 409(email is already exists for another user)|
| PUT | /members/{id}/deactivate | deactivate member | | 200(all went well) / 404(member not exists)|
|PUT |  /members/{id}/activate | activate a member | | 200(all went well) / 404(member not exists)|



### Reports Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET|  /reports/summary | get a summery report  |  | dict |
|GET | 	/reports/books-by-genre | get cnt of every genre | |dict |
| GET | /reports/top-member | get the best member (by borrows) | |dict| 404 |


---

## Error Handling

### users table management
|**Error Name**| **When does it Happen** | **What do we return to the user**|
|---|---|---|
|*`UserNotExists`*| we try to find or do an action on a user that does not exists| 404 user (id) not found|
|*`UserInactive`*| when we try to borrow book from inactive user| 400/409 user in active, can not barrow books|
|*`MailExist`*| we try to create or update a mail with a mail that exists | 400/409 {mail} is already exists|
|*`OverTheBarrowLimit`*|we try to barrow a book for a user but it has 3 books borrowed|400/409 you already got to the max borrowed books (3)


### book table management
|**Error Name**| **When does it Happen** | **What do we return to the user**|
|---|---|---|
|*`BookNotExists`*| when we try to found or do things about a book that does'not exists| 404 book not found
|*`BookIsBorrowed`* | when we try to borrow a book is already borrowed | 400/409 book is already borrowed|
|*`BookIsBorrowedToOtherUser`*| when we try to return a book for a user that borrowed to other user|400/409 book is borrowed to other user

---

## System Flow


1. **Server Startup:**
   - The server connects to MySQL
   - Creates tables if they don't exist
   - Starts the FastAPI server

2. **Creating a Member:**
   - User sends POST request to `/members` with name and email
   - System validates the email is unique
   - System creates member with `is_active=True` and `total_borrows=0`
   - Returns the created member

3. **Borrowing a Book:**
   - User sends PATCH request to `/books/{id}/borrow/{member_id}`
   - System checks if book exists
   - System checks if member exists and is active
   - System checks if book is available
   - System checks if member has less than 3 books
   - Updates book: `is_available=False`, `borrowed_by_member_id=member_id`
   - Increments member's `total_borrows` by 1
   - Returns success message


---



## Testing the API


### Test 1: Create a Member
```
POST /members
{
  "name": "Sara Cohen",
  "email": "sara@example.com"
}
```

### Test 2: Create a Book
```
POST /books
{
  "title": "The Hitchhiker's Guide to the Galaxy",
  "author": "Douglas Adams",
  "genre": "Fiction"
}
```

### Test 3: Borrow a Book
```
PATCH /books/1/borrow/1
```


---

