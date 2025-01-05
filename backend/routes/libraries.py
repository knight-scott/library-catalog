from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
import os
import pymysql

# Blueprint setup
libraries_bp = Blueprint('libraries', __name__)

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

# Add a new library
@libraries_bp.route('', methods=['POST'])
def add_library():
    data = request.json
    name = data.get('name')
    owner = data.get('owner')  # New owner field

    if not name or not owner:
        return jsonify({'error': 'Name and owner are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO libraries (name, owner)
        VALUES (%s, %s)
    """, (name, owner))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Library added successfully!'}), 201

# Retrieve all libraries
@libraries_bp.route('', methods=['GET'])
def get_libraries():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM libraries")
    libraries = cursor.fetchall()
    conn.close()

    return jsonify(libraries), 200

# Get details of a specific library by ID
@libraries_bp.route('/<int:library_id>', methods=['GET'])
def get_library(library_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM libraries WHERE id = %s", (library_id,))
    library = cursor.fetchone()
    conn.close()

    if not library:
        return jsonify({'error': 'Library not found'}), 404

    return jsonify(library), 200
