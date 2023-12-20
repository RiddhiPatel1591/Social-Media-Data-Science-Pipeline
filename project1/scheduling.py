import schedule
import time
import subprocess
import sys

# Counter to track the number of executions
execution_count = 0

def run_4chan():
    subprocess.run(["python3", "/home/kkamara1/reddit-folder/4chan.py"]) 

def run_reddit():
    global execution_count
    
    # Check if the script has already run twenty times
    if execution_count < 20:
        # Execute the script
        subprocess.run(["python3", "/home/kkamara1/reddit-folder/reddit.py"])
        # Increment the execution count
        execution_count += 1
        time.sleep(3600)
    else:
        # Stop further executions once the count reaches 20
        sys.exit()

# Schedule the job to run every day at midnight
schedule.every().day.at("00:00").do(run_reddit)
schedule.every().day.at("00:00").do(run_4chan)


while True:
    schedule.run_pending()
    time.sleep(10)
