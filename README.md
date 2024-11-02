# File Management System

This Flask-based file management system supports nested folders and file operations with a relational database backend.

## Features

- Folder creation, renaming, deletion (recursive)
- File creation, renaming, deletion
- Listing folder contents (files and subfolders)

## Endpoints

1. **Create Folder** - `POST /folders`
2. **Rename Folder** - `PUT /folders/<folder_id>`
3. **Delete Folder** - `DELETE /folders/<folder_id>`
4. **List Folder Contents** - `GET /folders/<folder_id>/contents`
5. **Create File** - `POST /files`
6. **Rename File** - `PUT /files/<file_id>`
7. **Delete File** - `DELETE /files/<file_id>`

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize the database: `flask db upgrade`
4. Run the app: `python app.py`

## Database

Using SQLite or PostgreSQL to store hierarchical folder and file structures.
