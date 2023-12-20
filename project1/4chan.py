import requests
import psycopg2
from psycopg2 import extras
import csv

API_BASE_URL = "https://a.4cdn.org"

db_params = {
    "dbname": "reddit_data",  # Replace with your PostgreSQL database name
    "user": "kkamara1",    # Replace with your PostgreSQL username
    "password": "12345",  # Replace with your PostgreSQL password
    "host": "localhost",        # Change if your database is hosted elsewhere
    "port": "5432"              # Change if your PostgreSQL port is different
}

def create_4chan_table_if_not_exists(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS four_chan_data (
            board TEXT,
            thread_id INTEGER,
            post_id INTEGER,
            username TEXT,
            p_comment TEXT,
            datetime TIMESTAMP
        );
    """)
    conn.commit()

def fetch_4chan_posts(board, thread_id):
    url = f"{API_BASE_URL}/{board}/thread/{thread_id}.json"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from 4chan API.")
        return None

def save_posts_to_postgresql(posts, board, thread_id):
    conn = psycopg2.connect(**db_params)
    create_4chan_table_if_not_exists(conn)

    cur = conn.cursor(cursor_factory=extras.DictCursor)

    for post in posts:
        post_data = {
            'board': board,
            'thread_id': thread_id,
            'post_id': post['no'],
            'username': post.get('name', ''),
            'p_comment': post.get('com', ''),
            'datetime': post['time']
        }
        try:
            cur.execute("""
                INSERT INTO four_chan_data (board, thread_id, post_id, username, p_comment, datetime)
                VALUES (%(board)s, %(thread_id)s, %(post_id)s, %(username)s, %(p_comment)s, to_timestamp(%(datetime)s));
                """, post_data)
        except Exception as e:
            print("Error inserting data:", e)
    conn.commit()

def export_4chan_data_to_csv(posts, board, thread_id):
    filename = f"four_chan_{board}_{thread_id}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['board', 'thread_id', 'post_id', 'username', 'p_comment', 'datetime']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for post in posts:
            post_data = {
                'board': board,
                'thread_id': thread_id,
                'post_id': post['no'],
                'username': post.get('name', ''),
                'p_comment': post.get('com', ''),
                'datetime': post['time']
            }
            writer.writerow(post_data)
    print(f"Data exported to {filename}")

if __name__ == "__main__":
    board = "k"
    thread_id = 60013532

    posts = fetch_4chan_posts(board, thread_id)

    if posts:
        save_posts_to_postgresql(posts['posts'], board, thread_id)
        export_4chan_data_to_csv(posts['posts'], board, thread_id)
        print(f"Successfully saved {len(posts['posts'])} posts to the database and exported to CSV.")