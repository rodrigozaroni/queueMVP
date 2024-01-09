import sqlite3

def debug_restaurants_data():
    # Connect to the database
    conn = sqlite3.connect('queue_MVP.db')
    c = conn.cursor()

    # Fetch restaurant data
    c.execute("SELECT restaurant_code, restaurant_name FROM restaurants")
    restaurants = c.fetchall()

    # Close the database connection
    conn.close()

    # Print the fetched data for debugging
    print("Fetched Restaurants Data:", restaurants)

# Call the function for debugging
debug_restaurants_data()
