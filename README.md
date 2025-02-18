# Books Checker

Books Checker is a book management system where teachers can add and remove books, while students can view the available book catalog. The system also includes user authentication with login and registration functionalities.

## Description

Books Checker is a web application designed for managing books in a classroom environment. Teachers can register, log in, and manage the book list, while students can view the catalog of books available for borrowing. The application provides an easy-to-use interface and ensures secure authentication for users.

## Features

- **User Authentication**: Teachers can create accounts and log in. Students can register, but only after approval by a teacher.
- **Book Management**: Teachers can add, edit, and delete books.
- **Book Viewing**: Students can view the list of available books.
- **Responsive Interface**: The system is responsive, working seamlessly on both mobile and desktop devices.

## Technologies Used

- **Python**: The main programming language used to build the backend.
- **Flask**: The web framework used to develop the application.
- **MySQL**: The database used to store user and book data.
- **HTML/CSS**: Used for building the web pages and ensuring a responsive layout.

## Prerequisites

- Python 3.x
- MySQL
- pip (for installing dependencies)

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/books-checker.git
```

### 2. Create and activate a virtual environment:
# For Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# For Windows:
python -m venv venv
.\venv\Scripts\activate

### 3. Install the dependencies:
```bash
pip install -r requirements.txt
```
### 4. Set up the Database
Create a MySQL database named books_proj and configure the necessary tables. The schema can be found in database/schema.sql (if you have a database setup script).

### 5. Run the application

```bash
python app.py
```

### How to Use
Upon accessing the homepage, you will be redirected to the login page.
Teachers can register using a specific code and manage the list of books.
Students can register and view the book catalog.

### Contributing
Contributions are welcome! To contribute to this project, follow these steps:

Fork this repository.
Create a branch for your modification (git checkout -b my-feature).
Make your changes.
Submit a pull request to this repository.
