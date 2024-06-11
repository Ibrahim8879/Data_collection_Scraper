import csv
import pandas as pd
import time
from datetime import datetime
import os


user_attr="C:/Users/ALI/OneDrive/Desktop/Twitter/user_attr.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Username', 'User location','User screen_name',
                             'User description','User followers_count',
                             'User friends_count','User time_zone','User geo_enabled',
                             'User verified','User created_at','User statuses_count'])
    csvfile.close()


tweets_file_path = "C:/Users/ALI/OneDrive/Desktop/Twitter/Tweets.csv"
tweets_df = pd.read_csv(tweets_file_path)

unique_usernames = tweets_df['Username'].unique()

user_attr_df = pd.DataFrame({'Username': unique_usernames})
user_attr_df.to_csv(user_attr, index=False)

for username in unique_usernames:
    retry_count = 0

    while retry_count < 5:  # Retry for a total of 30 minutes (5 attempts x 6 minutes)
        try:
            driver.get(f'https://twitter.com/{username}')
            # get all above mentioned user attributes.
        except Exception as e:
            print(f"Error fetching user data for {username}: {str(e)}")
            retry_count += 1
            print(f"Retrying in 6 minutes (Attempt {retry_count}/5)")
            time.sleep(360)  # Wait for 6 minutes before retrying
            