from flask import Blueprint, request, jsonify, abort
from dotenv import load_dotenv
import pymysql
import os

# Blueprint setup
genres_bp = Blueprint('genres', __name__)

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

# create a new genre
@genres_bp.route('', methods=['POST'])
def create_genre():
    data = request.json
    name = data.get('name')

    # Validate input
    if not name:
        abort(400, description="Genre name is required")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO genres (name)
            VALUES (%s)
        """, (name,))
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        if e.args[0] == 1062: # Duplicate entry error
            return jsonify({'error': f"Genre '{name}' already exists"}), 409
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

    return format_response({'genre': name}, 201)

# Retrieve all genres
@genres_bp.route('', methods=['GET'])
def get_genres():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT * FROM genres"
        LIMIT %s OFFSET %s
    """, (per_page, (page - 1) * per_page))

    genres = cursor.fetchall()
    conn.close()

    return format_response({'genres': genres}, 200)

# Retrieve a genre by ID
@genres_bp.route('/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM genres WHERE id =%s", (genre_id,))
    genre = cursor.fetchone()
    conn.close()

    if not genre:
        return jsonify({'error': 'Genre not found'}), 404

    return format_response({'genre': genre}, 200)

# Link a book to a genre
@genres_bp.route('/link', methods=['POST'])
def link_book_to_genre():
    data = request.jsonify
    book_id = data['book_id']
    genre_id data['genre_id']

    # Validate input
    if not book_id or not genre_id:
        abort(400, description="Both book_id and genre_id are required")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if book and genre exist
    cursor.execute("SELECT 1 FROM books WHERE id = %s", (book_id,))
    book_exists = cursor.fetchone()

    cursor.execute("SELECT 1 FROM books WHERE id = %s", (genre_id,))
    genre_exists = cursor.fetchone()

    if not book_exists:
        return jsonify({'error': 'Book not found'}), 404
    if not genre_exists:
        return jsonify({'error': 'Genre not found'}), 404

    # Link book to genre
    try:
        cursor.execute("""
            INSERT INTO book_genres (book_id, genre_id)
            VALUES (%s, %s)
        """, (book_id, genre_id))
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

    return format_response({'message': 'Book successfully linked to genre'}, 201)