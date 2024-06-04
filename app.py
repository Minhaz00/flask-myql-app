from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="db",  
        port=3306,  
        user="root",
        password="root",
        database="test_db"
    )


@app.route('/')
def index():
    connection = get_db_connection()
    if connection.is_connected():
        return jsonify(message="Connected to MySQL database")
    else:
        return jsonify(message="Failed to connect to MySQL database"), 500

# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# Endpoint to get a user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

# Endpoint to add a new user
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (new_user['name'], new_user['email']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User added successfully!'}), 201

# Endpoint to update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    update_data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (update_data['name'], update_data['email'], user_id))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'User updated successfully!'})

# Endpoint to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'User deleted successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
