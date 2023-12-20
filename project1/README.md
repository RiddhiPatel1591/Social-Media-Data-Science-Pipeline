<html>
<h2>Update</h2>
<h2>Updated Data Scheduling using "nohup" in linux</h2>
This repository contains scripts for fetching data from Reddit and 4chan and saving it to a database. Scheduling is implemented using nohup along with Python's schedule library to automate data retrieval.

<h3>Scheduler Configuration</h3>
<h4>nohup python3 scheduler.py &</h4>
scheduler.py orchestrates the execution of reddit.py and 4chan.py scripts.
The script reddit.py collects data from Reddit and 4chan.py fetches data from 4chan's boards.
Data collection occurs every day at midnight.

<h3>Limitations</h3>
The reddit.py script is configured to run twenty times each day and collects a maximum of 1000 records per day. After reaching the limit, it stops further executions.


[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/8auxQMoN)


<html>
<h2>ReadMe for Reddit and 4chan Data Collection and Storage</h2>
  This repository contains Python scripts for collecting data from Reddit and 4chan and storing it in a PostgreSQL database.
  Additionally, the collected data can be exported to CSV files for further analysis.

  <h4>Reddit Data Collection::</h4>
  In the reddit.py script, you can collect data from Reddit, specifically posts and comments from the subreddits "guns" and "firearms."
  The collected data is then stored in a PostgreSQL database and exported to a CSV file for further analysis.

  <h4>4chan Data Collection:</h4>
  In the 4chan.py script, you can collect data from 4chan, specifically posts from a specific board and thread.
  The collected data is stored in a PostgreSQL database and exported to a CSV file for further analysis
  
  <h2>Data Parameters</h2>
  db_params:
    "dbname": "reddit_data",  # Replace with your PostgreSQL database name   
    "user": "kkamara1",    # Replace with your PostgreSQL username
    "password": "12345",  # Replace with your PostgreSQL password
    "host": "localhost",        # Change if your database is hosted elsewhere
    "port": "5432"              # Change if your PostgreSQL port is different

  <\html>





  
  db_params:
    "dbname": "reddit_data",  # Replace with your PostgreSQL database name   
    "user": "kkamara1",    # Replace with your PostgreSQL username
    "password": "12345",  # Replace with your PostgreSQL password
    "host": "localhost",        # Change if your database is hosted elsewhere
    "port": "5432"              # Change if your PostgreSQL port is different
