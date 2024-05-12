from psycopg2 import pool

# Database connection parameters
db_params = {
    'dbname': 'seode',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

# Create a connection pool
try:
    connection_pool = pool.SimpleConnectionPool(
        1,  # minconn
        10,  # maxconn
        **db_params
    )
except Exception as e:
    print(f"Error creating connection pool: {e}")
    connection_pool = None

# Function to get a connection from the pool
def get_connection():
    if connection_pool:
        try:
            return connection_pool.getconn()
        except Exception as e:
            print(f"Error getting connection from pool: {e}")
            return None

# Function to release connection back to the pool
def release_connection(conn):
    if connection_pool and conn:
        try:
            connection_pool.putconn(conn)
        except Exception as e:
            print(f"Error releasing connection back to pool: {e}")

# Export functions
__all__ = ["get_connection", "release_connection"]
