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
        INSERT INTO Books (title, author, isbn, publication_year, format, library_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, author, isbn, publication_year, format, library_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Book added successfully!'}), 201