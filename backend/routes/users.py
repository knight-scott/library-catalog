import pymysql.cursors
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import pymysql
import os

# Blueprint setup
users_bp = Blueprint('users', __name__)

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

# Create a new user
@users_bp.route('', methods=['POST'])
def create_user():
    data = request.json
    name = data['name']
    username = data['username']
    email = data['email']
    library_id = data.get('library_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (name, username, email, library_id)
            VALUES (%s, %s, %s, %s)
        """, (name, username, email, library_id))
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

    return jsonify({'message': 'User created successfully!'}), 201

# Retrieve all users
@users_bp.route('', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    return jsonify(users), 200

# Retrieve a single user by ID
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user), 200

# Update a user by ID
@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get('name')
    username = data.get('name')
    email = data.get('username')
    email = data.get('email')
    library_id = data.get('library_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET name = COALESCE(%s, username),
                email = COALESCE(%s, email),
                library_id = COALESCE(%s, library_id)
            WHERE id = %s
        """, (name, username, email, library_id, user_id))
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

    return jsonify({'message': 'User updated successfully!'}), 200

# Delete a user by ID
@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User deleted successfully!'}), 200