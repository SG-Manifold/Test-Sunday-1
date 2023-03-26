from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# create a connection to the Postgres database
conn = psycopg2.connect(
    host="localhost",
    database="sunday1",
    user="postgres",
    password="12345"
)

# create a cursor object to interact with the database
cur = conn.cursor()

@app.route('/w', methods=['GET'])
def welcome():
    return jsonify({'message': 'Welcome to Manifold!'}), 200

@app.route('/register', methods=['GET','POST'])
def register():
    # get request data
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    # hash the password
    password_hash = generate_password_hash(password)

    # insert new user into database
    cur.execute('''
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id;
    ''', (username, email, password_hash))
    user_id = cur.fetchone()[0]
    conn.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201

@app.route('/login', methods=['POST'])
def login():
    # get request data
    username = request.json.get('rusername')
    password = request.json.get('rpassword')

    # retrieve user from database by username
    cur.execute('''
        SELECT id, password_hash, is_superuser, is_active
        FROM users
        WHERE username = %s;
    ''', (username,))
    user = cur.fetchone()

    # check if user exists and password is correct
    if user and check_password_hash(user[1], password):
        # check if user is active
        if user[3]:
            return jsonify({
                'message': 'User authenticated successfully',
                'user_id': user[0],
                'is_superuser': user[2],
            }), 200
        else:
            return jsonify({'message': 'User is inactive'}), 401
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/tenant', methods=['POST'])
def create_tenant():
    # get request data
    name = request.json.get('name')
    domain_name = request.json.get('domain_name')
    api_key = request.json.get('api_key')

    # insert new tenant into database
    cur.execute('''
        INSERT INTO tenant (name, domain_name, api_key)
        VALUES (%s, %s, %s)
        RETURNING id;
    ''', (name, domain_name, api_key))
    tenant_id = cur.fetchone()[0]
    conn.commit()

    return jsonify({'message': 'Tenant created successfully', 'tenant_id': tenant_id}), 201

@app.route('/tenant/<int:tenant_id>', methods=['PUT'])
def update_tenant(tenant_id):
    # get request data
    name = request.json.get('name')
    domain_name = request.json.get('domain_name')
    api_key = request.json.get('api_key')

    # update tenant in database
    cur.execute('''
        UPDATE tenant
        SET name = %s, domain_name = %s, api_key = %s, updated_at = %s
        WHERE id = %s;
    ''', (name, domain_name, api_key, datetime.now(), tenant_id))
    conn.commit()

    return jsonify({'message': 'Tenant updated successfully', 'tenant_id': tenant_id}), 200

@app.route('/tenant/<int:tenant_id>', methods=['DELETE'])
def delete_tenant(tenant_id):
    # delete tenant from database
    cur.execute('''
        DELETE FROM tenant
        WHERE id = %s;
    ''', (tenant_id,))
    conn.commit()

    return jsonify({'message': 'Tenant deleted successfully', 'tenant_id': tenant_id}), 200

@app.route('/tenant/<int:tenant_id>', methods=['GET'])
def get_tenant(tenant_id):
    # retrieve tenant from database by id
    cur.execute('''
        SELECT id, name, domain_name, api_key, created_at, updated_at
        FROM tenant
        WHERE id = %s;
    ''', (tenant_id,))
    tenant = cur.fetchone()

    # check if tenant exists
    if tenant:
        return jsonify({
            'id': tenant[0],
            'name': tenant[1],
            'domain_name': tenant[2],
            'api_key': tenant[3],
            'created_at': tenant[4].strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': tenant[5].strftime('%Y-%m-%d %H:%M:%S'),
        }), 200
    else:
        return jsonify({'message': 'Tenant not found'}), 404

@app.route('/tenant', methods=['GET'])
def list_tenants():
    # retrieve all tenants from database
    cur.execute('''
        SELECT id, name, domain_name, api_key, created_at, updated_at
        FROM tenant;
    ''')
    tenants = cur.fetchall()

    # format the response as a list of dictionaries
    response = []
    for tenant in tenants:
        response.append({
            'id': tenant[0],
            'name': tenant[1],
            'domain_name': tenant[2],
            'api_key': tenant[3],
            'created_at': tenant[4].strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': tenant[5].strftime('%Y-%m-%d %H:%M:%S'),
        })

    return jsonify(response), 200

# add more endpoints for CRUD operations on users, roles, modules, submodules, and microservices as needed

# run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
