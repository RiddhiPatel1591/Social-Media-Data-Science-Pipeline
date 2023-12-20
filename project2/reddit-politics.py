import time
import requests
import psycopg2
from psycopg2 import extras
from datetime import datetime

# Define your Reddit API credentials
client_id = 'qOXnEvUHEITqLDVy1OINIQ'
client_secret = 'WE_gw3kiOU9wtl9heDktmhDvXLbaxQ'
user_agent = 'kirthikraj1104'

# Define your PostgreSQL database connection parameters
db_params = {
    "dbname": "reddit_data",  # Replace with your PostgreSQL database name
    "user": "kkamara1",       # Replace with your PostgreSQL username
    "password": "12345",      # Replace with your PostgreSQL password
    "host": "localhost",      # Change if your database is hosted elsewhere
    "port": "5432"            # Change if your PostgreSQL port is different
}

# Define a function to fetch comments for a given submission
def fetch_comments(submission_id):
    base_url = f'https://www.reddit.com/comments/{submission_id}.json'
    headers = {'User-Agent': user_agent}
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

    response = requests.get(base_url, headers=headers, auth=auth)

    comments = []

    if response.status_code == 200:
        submission_data = response.json()
        for comment in submission_data[1]['data']['children']:
            comment_data = comment['data']
            author = comment_data.get('author', None)
            comments.append({
                'author': author,
                'score': comment_data.get('score', None),
                'body': comment_data.get('body', None)
            })

    return comments

# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Create tables for Reddit posts and comments if they don't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS reddit_posts (
        id TEXT PRIMARY KEY,
        title TEXT,
        self_text TEXT,
        author TEXT,
        score INTEGER,
        num_comments INTEGER,
        upvote_ratio NUMERIC,
        created_utc TIMESTAMP
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS reddit_comments (
        comment_id SERIAL PRIMARY KEY,
        post_id TEXT REFERENCES reddit_posts(id),
        author TEXT,
        score INTEGER,
        body TEXT
    );
""")

# Define the Reddit API endpoint and parameters for r/politics
base_url = 'https://www.reddit.com/r/politics/top.json'
headers = {'User-Agent': user_agent}
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
params = {
    'limit': 100,
    'after': '',
    'before': '',
}

after = None

while True:
    if after:
        params['after'] = after

    response = requests.get(base_url, headers=headers, auth=auth, params=params)

    if response.status_code == 200:
        subreddit_data = response.json()
        for submission in subreddit_data['data']['children']:
            submission_data = submission['data']
            created_utc = datetime.utcfromtimestamp(submission_data['created_utc'])

            # Check if the post_id already exists in the reddit_posts table
            cur.execute("SELECT id FROM reddit_posts WHERE id = %s", (submission_data['id'],))
            existing_post = cur.fetchone()

            if not existing_post:
                # Insert post data into the database
                cur.execute("""
                    INSERT INTO reddit_posts (id, title, self_text, author, score, num_comments, upvote_ratio, created_utc)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    submission_data['id'], submission_data['title'], submission_data['selftext'],
                    submission_data['author'], submission_data['score'], submission_data['num_comments'],
                    submission_data['upvote_ratio'], created_utc
                ))

                # Fetch comments for this post and insert into the database
                comments = fetch_comments(submission_data['id'])
                for comment in comments:
                    # Check if the comment already exists in the reddit_comments table
                    cur.execute("SELECT post_id FROM reddit_comments WHERE post_id = %s AND body = %s", (submission_data['id'], comment['body'],))
                    existing_comment = cur.fetchone()

                    if not existing_comment:
                        cur.execute("""
                            INSERT INTO reddit_comments (post_id, author, score, body)
                            VALUES (%s, %s, %s, %s);
                        """, (
                            submission_data['id'], comment['author'], comment['score'], comment['body']
                        ))

        after = subreddit_data['data']['after']
        if not after:
            break
    else:
        print(f"Failed to fetch data. Error: {response.status_code}")
        break

# Commit changes and close the database connection
conn.commit()
cur.close()
conn.close()

print("Data from r/politics (posts and comments) saved to the PostgreSQL database.")




# import time
# import requests
# import psycopg2
# from psycopg2 import extras
# from datetime import datetime

# # Define your Reddit API credentials
# client_id = 'qOXnEvUHEITqLDVy1OINIQ'
# client_secret = 'WE_gw3kiOU9wtl9heDktmhDvXLbaxQ'
# user_agent = 'kirthikraj1104'

# # Define your PostgreSQL database connection parameters
# db_params = {
#     "dbname": "reddit_data",  # Replace with your PostgreSQL database name
#     "user": "kkamara1",    # Replace with your PostgreSQL username
#     "password": "12345",  # Replace with your PostgreSQL password
#     "host": "localhost",        # Change if your database is hosted elsewhere
#     "port": "5432"              # Change if your PostgreSQL port is different
# }

# # Define a function to fetch comments for a given submission
# def fetch_comments(submission_id):
#     base_url = f'https://www.reddit.com/comments/{submission_id}.json'
#     headers = {'User-Agent': user_agent}
#     auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

#     response = requests.get(base_url, headers=headers, auth=auth)

#     comments = []

#     if response.status_code == 200:
#         submission_data = response.json()
#         for comment in submission_data[1]['data']['children']:
#             comment_data = comment['data']
#             # Check if 'author' key exists in the comment_data dictionary
#             author = comment_data.get('author', None)
#             comments.append({
#                 'author': author,
#                 'score': comment_data.get('score', None),
#                 'body': comment_data.get('body', None)
#             })

#     return comments

# # Connect to PostgreSQL
# conn = psycopg2.connect(**db_params)
# cur = conn.cursor()

# # Create tables for Reddit posts and comments if they don't exist
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS reddit_posts (
#         id TEXT PRIMARY KEY,
#         title TEXT,
#         self_text TEXT,
#         author TEXT,
#         score INTEGER,
#         num_comments INTEGER,
#         upvote_ratio NUMERIC,
#         created_utc TIMESTAMP
#     );
# """)

# cur.execute("""
#     CREATE TABLE IF NOT EXISTS reddit_comments (
#         post_id TEXT REFERENCES reddit_posts(id),
#         author TEXT,
#         score INTEGER,
#         body TEXT
#     );
# """)

# # Define the Reddit API endpoint and parameters for r/politics
# base_url = 'https://www.reddit.com/r/politics/top.json'
# headers = {'User-Agent': user_agent}
# auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
# params = {
#     'limit': 100,
#     'after': '',
#     'before': '',
# }

# after = None

# while True:
#     if after:
#         params['after'] = after

#     response = requests.get(base_url, headers=headers, auth=auth, params=params)

#     if response.status_code == 200:
#         subreddit_data = response.json()
#         for submission in subreddit_data['data']['children']:
#             submission_data = submission['data']
#             created_utc = datetime.utcfromtimestamp(submission_data['created_utc'])

#             # Insert post data into the database
#             cur.execute("""
#                 INSERT INTO reddit_posts (id, title, self_text, author, score, num_comments, upvote_ratio, created_utc)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                 ON CONFLICT DO NOTHING;
#             """, (
#                 submission_data['id'], submission_data['title'], submission_data['selftext'],
#                 submission_data['author'], submission_data['score'], submission_data['num_comments'],
#                 submission_data['upvote_ratio'], created_utc
#             ))

#             # Fetch comments for this post and insert into the database
#             comments = fetch_comments(submission_data['id'])
#             for comment in comments:
#                 cur.execute("""
#                     INSERT INTO reddit_comments (post_id, author, score, body)
#                     VALUES (%s, %s, %s, %s);
#                 """, (
#                     submission_data['id'], comment['author'], comment['score'], comment['body']
#                 ))

#         after = subreddit_data['data']['after']
#         if not after:
#             break
#     else:
#         print(f"Failed to fetch data. Error: {response.status_code}")
#         break

# # Commit changes and close the database connection
# conn.commit()
# cur.close()
# conn.close()

# print("Data from r/politics (posts and comments) saved to the PostgreSQL database.")
