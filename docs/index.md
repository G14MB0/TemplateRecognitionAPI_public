# Welcome to SimpleApp_Backend

This simple Python application is a small backend applciation build with fastAPI.
It implements a uvicorn-fastAPI server that serve few RESTful APIs to interact with and use them as an example for a bigger work.

## Structure

The app is divided in two folders, app and lib.
- The app part is where the fastAPI application and all the endpoints and CRUD operations are defined.
- The lib part is where the sqlite database is initialized and some simple methods are written.

There is also a docs folder, where the markdown used by mkdocs are present.

The main.py in the root directory is used to start the application using uvicorn and also some basic routine are defined.

Below the project layout!


## Project Layout

The project is structured as follows:

- `main.py`: The main entry file of the project.
- `app/`: This directory contains the core of the FastAPI application.
    - `routers/`: Contains the router modules.
        - `database.py`: Endpoints for database operations.
    - `main.py`: Main FastAPI file with root endpoints.
    - `schemas.py`: Definitions of Pydantic schemas for data validation and serialization.
- `lib/`: This directory contains libraries and helpers.
    - `database/`: Related to database operations.
        - `main.py`: Main database file, handles initialization, connection, and potentially initial database creation.
    - `tkinter/`: Related to windows dialog operations.
        - `main.py`: Simple methods to opend windows file/folder selection dialogs
- `docs/`: Contains the MkDocs documentation.
    - `index.md`: The homepage of the documentation.
    - `...`: Other markdown pages for various documentation aspects.

