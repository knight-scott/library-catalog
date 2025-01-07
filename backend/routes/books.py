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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

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

    # add pagination
    offset = (page - 1) * per_page
    query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    books = cursor.fetchall()

    # Count total results for pagination metadata
    cursor.execute("SELECT COUNT(*) as total FROM books" + (" WHERE " + " AND ".join(filters) if filters else ""), params[:-2])
    total_books = cursor.fetchone()['total']

    conn.close()

    # Construct the response with pagination metadata
    response = {
        "books": books,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total_books, 
            "total_pages": (total_books + per_page - 1) // per_page # Calculate total pages
        }
    }

    return jsonify(books), 200

# Retrieve a book by ID
@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM Books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    conn.close()

    if not book:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify(book), 200

# Update a book
@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    fields = []
    values = []

    for field in ['title', 'author', 'isbn', 'publication_year', 'format', 'library_id']:
        if field in data:
            fields.append(f"{field} = %s")
            values.append(data[field])

    if not fields:
        return jsonify({'error': 'No fields to update provided'}), 400

    query = f"UPDATE Books SET {', '.join(fields)} WHERE id = %s"
    values.append(book_id)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify({'message': 'Book updated successfully'}), 200

# Delete a book
@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Books WHERE id = %s", (book_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify({'message': 'Book deleted successfully'}), 200