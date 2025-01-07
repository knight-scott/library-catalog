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

# New checkout record
@books_bp.route('/checkouts', methods=['POST'])
def checkout_book():
    data = request.json
    user_id = data['user_id']
    book_id = data['book_id']
    checkout_date = data['checkout_data']

    query = "INSERT INTO checkouts (user_id, book_id, checkout_date) VALUES (%s, %s, %s)"
    params - (user_id, book_id, checkout_date)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

    return jsonify({"message": "Book checked out successfully"})