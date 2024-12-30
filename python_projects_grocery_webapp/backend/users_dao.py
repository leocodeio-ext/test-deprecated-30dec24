from werkzeug.security import generate_password_hash, check_password_hash

def register_user(connection, user_data):
    cursor = connection.cursor()
    
    # Check if username already exists
    cursor.execute('SELECT username FROM users WHERE username = ?', (user_data['username'],))
    if cursor.fetchone() is not None:
        return None, "Username already exists"
    
    # Hash the password
    hashed_password = generate_password_hash(user_data['password'])
    
    try:
        cursor.execute('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        ''', (user_data['username'], hashed_password, user_data['role']))
        connection.commit()
        return cursor.lastrowid, "Registration successful"
    except Exception as e:
        return None, str(e)

def login_user(connection, username, password):
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if user is None:
        return None, "Invalid username or password"
        
    if check_password_hash(user['password'], password):
        return {
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role']
        }, "Login successful"
    else:
        return None, "Invalid username or password"