import time
from datetime import datetime, timedelta
import os
import csv
import pandas as pd
import threading
from twitter_scraper_1 import Tweet_info1 as fetch_tweets1
from twitter_scraper_2 import Tweet_info2 as fetch_tweets2
from twitter_scraper_3 import Tweet_info3 as fetch_tweets3
from twitter_scraper_1 import User_info1 as fetch_user1
from twitter_scraper_2 import User_info2 as fetch_user2
from twitter_scraper_3 import User_info3 as fetch_user3


#Storing data to main csv, dividing it to three parts, store them in respective csv's.
def consolidate_tweets():
    main_file = "C:/Users/Ibrahim/Desktop/Data_collection/tweets.csv"
    tweet_files = ["C:/Users/Ibrahim/Desktop/Data_collection/S1/tweets.csv" ,
                   "C:/Users/Ibrahim/Desktop/Data_collection/S2/tweets.csv",
                   "C:/Users/Ibrahim/Desktop/Data_collection/S3/tweets.csv" ]

    try:
        main_df = pd.read_csv(main_file)
        print('mili')
    except FileNotFoundError:
        main_df = pd.DataFrame()
    for tweet_file in tweet_files:
        try:
            tweet_df = pd.read_csv(tweet_file)
            print(tweet_df)
        except FileNotFoundError:
            continue

        main_df = pd.concat([main_df, tweet_df], ignore_index=True)

    main_df = main_df.drop_duplicates(subset='Tweet')
    main_df.to_csv(main_file, index=False)
    
    
    #Getting USer names
    today_date = datetime.today().strftime('%Y-%m-%d')
    
    usernames=set()
    with open(main_file, 'r', newline='',encoding='utf-8') as file:
        reader = csv.reader(file)
            
        next(reader)

        for row in reader:
            if row:  
                if row[0] == today_date:
                    value = row[3]
                    if value not in usernames:
                        usernames.add(value)

    # Divide Into Three parts
    file_paths = ["C:/Users/Ibrahim/Desktop/Data_collection/S1/usernames.csv" ,
                   "C:/Users/Ibrahim/Desktop/Data_collection/S2/usernames.csv",
                   "C:/Users/Ibrahim/Desktop/Data_collection/S3/usernames.csv" ]

    # Divide the usernames into three parts
    num_parts = 3
    chunk_size = (len(usernames) + num_parts - 1) // num_parts
    username_chunks = [list(usernames)[i:i + chunk_size] for i in range(0, len(usernames), chunk_size)]

    # Write each chunk to a separate CSV file
    for i, filepath in enumerate(file_paths):
        with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Username'])
            for username in username_chunks[i]:
                csv_writer.writerow([username])


def main():
    #Getting User tweets info
    start_time = time.time()
    thread1 = threading.Thread(target=fetch_tweets1)
    thread2 = threading.Thread(target=fetch_tweets2)
    thread3 = threading.Thread(target=fetch_tweets3)
    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()
    # Wait for all threads to finish
    thread1.join()
    thread2.join()
    thread3.join()       

    # Store data, divide usernames.
    consolidate_tweets()
    
    #Getting User User info
    thread4 = threading.Thread(target=fetch_user1)
    thread5 = threading.Thread(target=fetch_user2)
    thread6 = threading.Thread(target=fetch_user3)
    # Start the threads
    thread4.start()
    thread5.start()
    thread6.start()
    # Wait for all threads to finish
    thread4.join()
    thread5.join()
    thread6.join()
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    #Making a log file.
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"work_status_{current_date}.txt"
    work_done = "DONE...., In = " + str(elapsed_time/120) + " hour's."
    with open(file_name, 'w') as file:
        file.write(f"Date: {current_date}\nWork Done: {work_done}")
        file.close()
        
    #os.system("shutdown /s /t 1")
    
if __name__ == "__main__":
    main()
