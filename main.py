from flask import Flask, render_template, request, redirect, url_for, g, jsonify
import sqlite3

app = Flask(__name__)

# Function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('restaurant_queue.db')
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# Moved database initialization inside a function
def init_db():
    conn = sqlite3.connect('restaurant_queue.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  queue_position INTEGER DEFAULT 0,
                  name TEXT,
                  email TEXT UNIQUE,
                  phone TEXT)''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customer_form', methods=['GET', 'POST'])
def customer_form():
    db = get_db()  # Get the database connection within the same thread
    c = db.cursor()  # Create a cursor
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Check if the customer already exists based on email or phone
        c.execute("SELECT id, name FROM customers WHERE email=? OR phone=?", (email, phone))
        customer_data = c.fetchone()

        if customer_data:
            customer_id, customer_name = customer_data
            # Simulate queue position change (you can implement this based on your logic)
            new_queue_position = 5  # Replace with your queue management logic
            # Redirect the customer to the customer queue route with their customer_id
            return redirect(url_for('customer_queue', customer_id=customer_id))

        # If the customer is new, insert their data into the database (you can adapt this to your database setup)
        c.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
        db.commit()

        # Simulate queue position change for new customers
        new_queue_position = 1  # Replace with your queue management logic
        # Redirect the customer to the customer queue route with their customer_id
        return redirect(url_for('customer_queue', customer_id=c.lastrowid))

    return render_template('customer_form.html')

@app.route('/customerqueue/<int:customer_id>')
def customer_queue(customer_id):
    db = get_db()  # Get the database connection within the same thread
    c = db.cursor()  # Create a cursor

    # Fetch the customer's queue position based on customer_id (you can implement this based on your logic)
    c.execute("SELECT queue_position FROM customers WHERE id=?", (customer_id,))
    queue_position = c.fetchone()

    if queue_position:
        return render_template('customer_queue.html', queue_position=queue_position[0])
    else:
        return jsonify({"error": "Customer not found"})

if __name__ == '__main__':
    app.run(debug=True)
