from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
import os
import pymysql

# Blueprint setup
books_bp = Blueprint('books', __name__)

# Load environment variables
load_dotenv()

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host='db',
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

# Add a book
@books_bp.route('', methods=['POST'])
def add_book():
    data = request.json
    title = data['title']
    author = data['author']
    isbn = data['isbn']
    publication_year = data['publication_year']
    format = data['format']
    library_id = data['library_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, isbn, publication_year, format, library_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, author, isbn, publication_year, format, library_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Book added successfully!'}), 201

# Search for a book by title, author, or library_id
@books_bp.route('', methods=['GET'])
def get_books(title, author, library_id):
    title = request.args.get('title')
    author = request.args.get('author')
    library_id = request.args.get('library_id')

    query = "SELECT * FROM books"
    filters = []
    params = []

    # Dynamically build the WHERE clause based on the filters provided
    if title:
        filters.append("title LIKE %s")
        params.append(f"%{title}%")
    if author:
        filters.append("author LIKE %s")
        params.append(f"%{author}%")
    if library_id:
        filters.append("library_id = %s")
        params.append(library_id)

    # Add filters to the query if any exist
    if filters:
        query += " WHERE " + " AND ".join(filters)

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    books = cursor.fetchall()
    conn.close()

    return jsonify(books), 200

