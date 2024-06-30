# TigerTaxi

Plan rideshares without listservs.

This repository is organized using Git [**branches**](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) and [**release tags**](https://git-scm.com/book/en/v2/Git-Basics-Tagging). In order to access and locally run a given version of the application, please follow the appropriate instructions below. For versions currently in development, read the corresponding section below **before** committing any code to the repository.

- [Command Line](#command-line)
- [Prototype](#prototype)
- [Alpha](#alpha)
- [Beta](#beta)
- [Final Release](#final-release)

## Command Line
<details>
  <summary>(Click to expand)</summary>

(**Note:** This version of TigerTaxi was a pre-prototype experiment meant to help flesh out our database design. As of now, only the user creation and ride search functionality is implemented.)

In order to begin using the command line version of the app, move to its tag using `git checkout command-line`. Then, run the database initialization script using `python3 dbinit.py`, making sure that you've activated the Python virtual environment. After this step, you should see a new file `tigertaxi.sqlite` in your repository directory. `dbinit.py` simply executes each of the SQL commands found in `setup.sql`, so if you'd like to add dummy data to the sqlite database, or alter any of its fields, you can do so by deleting `tigertaxi.sqlite`, editing `setup.sql`, and running `dbinit.py` again.

The command line application takes two arguments, `username` and `action`. To perform a given action, execute the command `python3 tigertaxi.py example_name example_action` and follow the prompts given by the program. If you don't already have a user in the database, you'll need to create one using `python3 tigertaxi.py example_name create_user` before performing any other action. You can use `python3 tigertaxi.py -h` to see each of the actions available in the program.
</details>

## Prototype
<details>
  <summary>(Click to expand)</summary>

### **Built With**

- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
  - [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/)
  - [Flask-DB](https://github.com/nickjj/flask-db#migrating-from-using-alembic-directly-or-flask-migrate)
  - [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [TailwindCSS](https://tailwindcss.com/)
- [PostgreSQL](https://www.postgresql.org/)
  - [psycopg2](https://www.psycopg.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)

### **Installation**
1. Install the Yarn package manager:
    ```sh
    npm install --global yarn
    ```

2. Install the Node dependencies (listed in `package.json`):
    ```sh
    yarn install
    ```

3. Initialize a virtual environment for the application and its dependencies:
    ```sh
    $ python3 -m venv .venv
    $ source .venv/bin/activate # activate the virtual environment
    ```

4. Install the required dependencies with pip:
    ```sh
    $ pip install -r requirements.txt
    ```

5. Install PostgreSQL (we use version 14). Set the superuser,
`postgres`, to have no password, and set the PostgreSQL
server to run on port `5432`. If you have an existing PostgreSQL
install that doesn't meet these specifications, you'll need to edit the
.flaskenv file to run the app.

6. Initialize a PostgreSQL database for the application:
    ```sh
    $ createdb -U postgres tigertaxi
    ```

7. Migrate your database to the latest revision:
    ```sh
    $ flask db migrate
    ```
8. Create a `.flaskenv` file:
```sh
$ touch .flaskenv
```

9. Copy the contents from `.flaskenv.sample` to your `.flaskenv` Follow the instructions to create your own secret key. **This is very important: The app will not run without a secret key!**
### **First Things First**
You want to make sure that your terminal environment has the necessary environment variables, otherwise the app will complain with some gnarly looking errors.

To load environment variables:
```sh
$ source .flaskenv
```

Always remember to do this at least once before doing anything below.

### **Slap the Database**

Flask-DB provides a simplified CLI for the Alembic database migration
tool. Visit the links above for more information on either library.

To seed the DB:
```sh
$ flask db seed
```
To drop, create, migrate, and seed the DB:
```sh
$ flask db reset
```
To automatically generate a migration after modifying a model:
```sh
$ flask db migrate revision --autogenerate -m "migration description"
```
The migration message is optional, but it would be very cool if you include it!

To upgrade your DB to the lastest migration:
```sh
$ flask db migrate
```

### **Go To Shell**
To test business logic on the models and other programmatic stuff:
```sh
$ flask shell
```

### **Serve the App-etizer**

To run the web app/server:
```sh
$ flask run
```
</details>

## Alpha
<details>
  <summary>(Click to expand)</summary>

### **Built With**
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
  - [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/)
  - [Flask-CAS-NG](https://github.com/MasterRoshan/flask-cas-ng)
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
  - [Flask-DB](https://github.com/nickjj/flask-db#migrating-from-using-alembic-directly-or-flask-migrate)
  - [Flask-Mail](https://pythonhosted.org/Flask-Mail/)


### **Installation**

1. Initialize a virtual environment for the application and its dependencies:
    ```sh
    $ python3 -m venv .venv
    $ source .venv/bin/activate # activate the virtual environment
    ```

2. Install the required dependencies with pip:
    ```sh
    $ pip install -r requirements.txt
    ```

3. Install PostgreSQL (we use version 14). Set the superuser,
`postgres`, to have no password, and set the PostgreSQL
server to run on port `5432`. If you have an existing PostgreSQL
install that doesn't meet these specifications, you'll need to edit the
.flaskenv file to reflect this.

4. Initialize a PostgreSQL database for the application:
    ```sh
    $ createdb -U postgres tigertaxi
    ```

5. Create your .flaskenv file from .flaskenv.sample. Copy the sample
   file over
    ```sh
    $ cp .flaskenv.sample .flaskenv
    ```
    Then follow the instructions given in the file.

6. Migrate your database to the latest revision:
    ```sh
    $ flask db migrate
    ```

7. Run the app!
    ```sh
    $ flask run
    ```

### **Database Usage**

We're currently still using Flask-DB, SQLAlchemy, and Alembic, so you should follow the same process as in the prototype to make any database changes.

</details>

## Beta

<details>
  <summary>(Click to expand)</summary>

### **Built With**
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
  - [Flask-CAS-NG](https://github.com/MasterRoshan/flask-cas-ng)
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
  - [Flask-DB](https://github.com/nickjj/flask-db#migrating-from-using-alembic-directly-or-flask-migrate)
  - [Flask-Mail](https://pythonhosted.org/Flask-Mail/)


### **Installation**

1. Initialize a virtual environment for the application and its dependencies:
    ```sh
    $ python3 -m venv .venv
    $ source .venv/bin/activate # activate the virtual environment
    ```

2. Install the required dependencies with pip:
    ```sh
    $ pip install -r requirements.txt
    ```

3. Install PostgreSQL (we use version 14). Set the superuser,
`postgres`, to have no password, and set the PostgreSQL
server to run on port `5432`. If you have an existing PostgreSQL
install that doesn't meet these specifications, you'll need to edit the
.flaskenv file to reflect this.

4. Initialize a PostgreSQL database for the application:
    ```sh
    $ createdb -U postgres tigertaxi
    ```

5. Create your .flaskenv file from .flaskenv.sample. Copy the sample
   file over
    ```sh
    $ cp .flaskenv.sample .flaskenv
    ```
    Then follow the instructions given in the file.

6. Migrate your database to the latest revision:
    ```sh
    $ flask db migrate
    ```

7. Run the app!
    ```sh
    $ flask run
    ```

### **Database Usage**

We're currently still using Flask-DB, SQLAlchemy, and Alembic, so you should follow the same process as in the prototype to make any database changes.

</details>

## Final Release

Any last minute bugfixes or tweaks can be committed straight to the `main`
branch. Great job this semester everyone!

### **Built With**
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
  - [Flask-CAS-NG](https://github.com/MasterRoshan/flask-cas-ng)
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
  - [Flask-DB](https://github.com/nickjj/flask-db#migrating-from-using-alembic-directly-or-flask-migrate)
  - [Flask-Mail](https://pythonhosted.org/Flask-Mail/)


### **Installation**

1. Initialize a virtual environment for the application and its dependencies:
    ```sh
    $ python3 -m venv .venv
    $ source .venv/bin/activate # activate the virtual environment
    ```

2. Install the required dependencies with pip:
    ```sh
    $ pip install -r requirements.txt
    ```

3. Install PostgreSQL (we use version 14). Set the superuser,
`postgres`, to have no password, and set the PostgreSQL
server to run on port `5432`. If you have an existing PostgreSQL
install that doesn't meet these specifications, you'll need to edit the
.flaskenv file to reflect this.

4. Initialize a PostgreSQL database for the application:
    ```sh
    $ createdb -U postgres tigertaxi
    ```

5. Create your .flaskenv file from .flaskenv.sample. Copy the sample
   file over
    ```sh
    $ cp .flaskenv.sample .flaskenv
    ```
    Then follow the instructions given in the file.

6. Migrate your database to the latest revision:
    ```sh
    $ flask db migrate
    ```

7. Run the app!
    ```sh
    $ flask run
    ```
