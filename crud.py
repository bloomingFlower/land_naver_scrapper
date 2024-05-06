import psycopg2

def connect_to_db():
    # Connect to your postgres DB
    conn = psycopg2.connect("dbname=test user=postgres password=secret host=localhost")

    cur = conn.cursor()

    # Execute a query
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles(
            id SERIAL PRIMARY KEY,
            title_area TEXT,
            price_area TEXT,
            information_area TEXT,
            tag_area TEXT,
            merit_area TEXT,
            full_url TEXT,
            article_number TEXT
        )
    """)
    # Commit the transaction
    conn.commit()
    return conn

def store_data(conn, title_area, price_area, information_area, tag_area, merit_area, full_url, article_number):
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("""
        INSERT INTO articles (title_area, price_area, information_area, tag_area, merit_area, full_url, article_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (article_number)
        DO UPDATE SET
            title_area = EXCLUDED.title_area,
            price_area = EXCLUDED.price_area,
            information_area = EXCLUDED.information_area,
            tag_area = EXCLUDED.tag_area,
            merit_area = EXCLUDED.merit_area,
            full_url = EXCLUDED.full_url
    """, (title_area, price_area, information_area, tag_area, merit_area, full_url, article_number))

    # Commit the transaction
    conn.commit()

    # Close the connection
    cur.close()