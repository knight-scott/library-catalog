from flask import Blueprint, request, jsonify, abort
from dotenv import load_dotenv
import pymysql
import os

# Blueprint setup
checkouts_bp = Blueprint('checkouts', __name__)

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

# Response consistency 
def format_response(data, status_code):
    return jsonify({
        'status': 'success',
        'message': data
    }), status_code
    
# Add a genre to a book
@books_bp.route('/book_genres', methods=['POST'])
def add_genre_to_book():
    data = request.json
    book_id = data['book_id']
    genre_id =data['genre_id']

    query = "INSERT INTO book_genres (book_id, genre_id) VALUES (%s, %s)"
    params = (book_id, genre_id)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, watch)
    conn.commit()
    conn.close()

    return jsonify({"message":"Genre add to book succesfuly"}), 201