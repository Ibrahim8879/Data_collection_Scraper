from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge.options import Options as EdgeOptions
import csv
import pandas as pd
import time
from datetime import datetime
import os


def Tweet_info3():
    retry_count = 0
    while retry_count < 5:
        try:
            #countries list
            countries_list = [
            "Lebanon",
            "Oman",
            "Palestine",
            "Qatar",
            "Saudi Arabia",
            "Syria",
            "United Arab Emirates",
            "Yemen",
            ]
            
            username = "Testing5611013"
            password="M_ali123!@#"
            
            url="https://twitter.com/i/flow/login"
            edge_options = EdgeOptions()
            edge_options.add_argument("--disable-images")
            edge_options.add_argument("--disable-features=Video")
            driver = webdriver.Edge(options=edge_options)
            driver.get(url)
            
            time.sleep(8)
            username_input=driver.find_element(By.CLASS_NAME,'r-30o5oe')
            username_input.send_keys(username)
              
            next_button=driver.find_element(By.XPATH,'//*[@id="layers"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[6]/div[1]')    
            next_button.click()
            time.sleep(5)  
                
            password_input=driver.find_element(By.NAME,'password')
            password_input.send_keys(password)
                
            login_button=driver.find_element(By.XPATH,'//*[@id="layers"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]')
            login_button.click()
            time.sleep(6)
            explore_button=driver.find_element(By.CSS_SELECTOR,'a[href="/explore"]')
            explore_button.click()
            time.sleep(2)
            
            
            # get trends and save them is csv
            ProfileDataFile='C:/Data_collection/S3/ProfileData.csv'
            csv_filename="C:/Data_collection/S3/Trends.csv"
            tweetsFile="C:/Data_collection/S3/Tweets.csv"
            tmp_tweetsFile="C:/Data_collection/S3/tmpTweets.csv"
            username="C:/Data_collection/S3/usernames.csv"
        
             # Remove previous trends if present from trends.
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                 csv_writer = csv.writer(csvfile)
                 # Write the header row
                 csv_writer.writerow(['Country', 'Trend', 'Search URL'])
                 csvfile.close()
                 
             # Remove previous data from tweet.
            with open(tweetsFile, 'w', newline='', encoding='utf-8') as csvfile:
                 csv_writer = csv.writer(csvfile)
                 # Write the header row
                 csv_writer.writerow(["Date", "Country", "Trend", "Username", "Tweet","Language","Tweet_Time"])
                 csvfile.close()
             
             # Remove previous data from user profile.
            with open(ProfileDataFile, 'w', newline='', encoding='utf-8') as csvfile:
                 csv_writer = csv.writer(csvfile)
                 # Write the header row
                 csv_writer.writerow(['Username','Display Name','Birth Date','Description','Location','Followers','Following','Verified','Number of Posts','Date Joined'])
                 csvfile.close()
             
             # Remove previous data from tmo_tweet.
            with open(tmp_tweetsFile, 'w', newline='', encoding='utf-8') as csvfile:
                 csv_writer = csv.writer(csvfile)
                 csvfile.close()
                 
             # Remove previous data from usernames.
            with open(username, 'w', newline='', encoding='utf-8') as csvfile:
                 csv_writer = csv.writer(csvfile)
                 csvfile.close()
             
             # trends collection
            with open(csv_filename, 'a', newline='',encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                
                for country in countries_list:
                    retry_count = 0
                    time.sleep(5)
                    
                    while retry_count < 5:  # Retry for a total of 30 minutes (5 attempts x 6 minutes)
                        try:
                            # Navigate to the trends location settings page
                            driver.get('https://twitter.com/settings/trends/location')
                            time.sleep(4)
                        
                            # Set the input field "country"
                            location_input = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="locationSearchBox"]')
                            location_input.clear()
                            location_input.send_keys(country)
                        
                            time.sleep(2)
                        
                            # Save the changes
                            location_suggestion = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
                            location_suggestion.click()
                        
                            # Going back to trends
                            driver.get('https://twitter.com/i/trends')
                            
                            time.sleep(3)
                            # Get trends (hashtags) for the current country
                            trends = set()
                            
                            #FOR TRENDS ONLY WITH HASHTAGS
                            #trends = driver.find_elements(By.XPATH, '//*[starts-with(@id, "id")]/div[2]/span/span')
                            #FOR TOPICS AND TRENDS BOTH THINGS
                            trends=driver.find_elements(By.XPATH,'.//*[starts-with(@id,"id")]/div[2]/span') 
                            time.sleep(2)
                            trendsLength = len(trends)
                            print("Country:", country)
                            print("Number of trends:", trendsLength)
                        
                            for trend in trends:
                                trend_text = trend.text
                                trend_text_tmp = trend_text
                                if (trend_text[0]=='#'):
                                    trend_text_tmp = trend_text_tmp.lstrip("#")          
                                    trend_text_tmp = "%23" + trend_text_tmp          
                                search_url = f'https://twitter.com/search?q={trend_text_tmp}&src=trend_click&vertical=trends'      
                                csv_writer.writerow([country, trend_text, search_url])
                        
                            time.sleep(4)
                            break
                        except Exception as e:
                            print(f"Error fetching trends for {country}: {str(e)}")
                            retry_count += 1
                            print(f"Retrying in 6 minutes (Attempt {retry_count}/5)")
                            time.sleep(40)  # Wait for 6 minutes before retrying
                        
            # Open the CSV file for reading
            trends_url_list = []
            trends_list = []
            country_list = []
            
            with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
            
                for row in csv_reader:
                    if len(row) >= 3:
                        country = row[0]
                        trend = row[1]
                        trends_url = row[2]
                        country_list.append(country)
                        trends_list.append(trend)
                        trends_url_list.append(trends_url)
            
            # Print the list of trends
            today_date = datetime.today().strftime('%Y-%m-%d')
            
            for trend, country, trend_url in zip(trends_list, country_list, trends_url_list):
                retry_count = 0
                
                while retry_count < 5:  # Retry for a total of 30 minutes (5 attempts x 6 minutes)
                    try:
                        driver.get(trend_url)
                        time.sleep(7)
                        usernames_and_tweets = []
            
                        while len(usernames_and_tweets) < 2:
                            tweetElement = driver.find_elements(By.XPATH, '//*[@data-testid="tweet"]')
                            for tweet in tweetElement:
                                UN = tweet.find_element(By.XPATH, './/*[starts-with(@id,"id")]/div[2]/div/div[1]/a/div/span').text
                                tweets = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
                                lang=tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').get_attribute('lang')
                                #TimeElement=tweet.find_element(By.XPATH,'.//time')
                                time_element = driver.find_element(By.XPATH,'//time[@datetime]')
                                TimeValue=time_element.get_attribute('datetime')
                                usernames_and_tweets.append((today_date, country, trend, UN, tweets,lang,TimeValue))
                                
                                file_exists = os.path.exists(tmp_tweetsFile)
                                new_data_df = pd.DataFrame(usernames_and_tweets, columns=["Date", "Country", "Trend", "Username", "Tweet","Language","Tweet_Time"])
                                mode = 'a' if file_exists else 'w'
                                new_data_df.to_csv(tmp_tweetsFile, mode=mode, index=False, header=not file_exists)
                                
                            driver.execute_script('window.scrollBy(0,3000);')
                            time.sleep(5)
        
                        file_exists = os.path.exists(tweetsFile)
                        new_data_df = pd.DataFrame(usernames_and_tweets, columns=["Date", "Country", "Trend", "Username", "Tweet","Language","Tweet_Time"])
                        new_data_df = new_data_df.drop_duplicates(subset="Tweet", keep="first")
                        mode = 'a' if file_exists else 'w'
                        new_data_df.to_csv(tweetsFile, mode=mode, index=False, header=not file_exists)
                        break  # Break out of the retry loop if successful
                    except Exception as e:
                        print(f"Error fetching tweets for {trend}: {str(e)}")
                        retry_count += 1
                        print(f"Retrying in 6 minutes (Attempt {retry_count}/5)")
                        time.sleep(2)  # Wait for 6 minutes before retrying
                        driver.get('https://twitter.com/i/trends')
                        time.sleep(40)
            
            driver.quit()
            break
        except Exception as e:
            print(f"Error Logging in.. : {e}")
            retry_count += 1
            print(f"Retrying in 6 minutes (Attempt {retry_count}/5)")
            time.sleep(360)  # Wait for 6 minutes before retrying
    
def User_info3():
    retry_count = 0
    while retry_count < 5:
        try:
            #Log in
            username = "Testing5611013"
            password="M_ali123!@#"
            
            url="https://twitter.com/i/flow/login"
            edge_options = EdgeOptions()
            edge_options.add_argument("--disable-images")
            edge_options.add_argument("--disable-features=Video")
            driver = webdriver.Edge(options=edge_options)
            driver.get(url)
            
            time.sleep(8)
            username_input=driver.find_element(By.CLASS_NAME,'r-30o5oe')
            username_input.send_keys(username)
              
            next_button=driver.find_element(By.XPATH,'//*[@id="layers"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[6]/div[1]')    
            next_button.click()
            time.sleep(5)  
                
            password_input=driver.find_element(By.NAME,'password')
            password_input.send_keys(password)
                
            login_button=driver.find_element(By.XPATH,'//*[@id="layers"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]')
            login_button.click()
            time.sleep(6)
            explore_button=driver.find_element(By.CSS_SELECTOR,'a[href="/explore"]')
            explore_button.click()
            time.sleep(2)
            
            # get trends and save them is csv
            ProfileDataFile='C:/Data_collection/S3/ProfileData.csv'
            username="C:/Data_collection/S3/usernames.csv"
        
            usernames=set()
            with open(username, 'r', newline='',encoding='utf-8') as file:
                # Create a CSV reader
                reader = csv.reader(file)
                # Skip the header row
                next(reader)
                for row in reader:
                    if row:  # Check if the row is not empty
                        value = row[0]
                        if value not in usernames:
                            usernames.add(value)
        
            print(usernames)
        
            url_prefix = 'https://twitter.com/'
            wait = WebDriverWait(driver, timeout=2)
            element_locator=(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div')
        
            for uname in usernames:   
                ProfileData=[]
                user_birthdate=''
                user_description=''
                user_location=''
                user_following=''
                user_followers=''
                num_of_posts=''
                verified=''
                profile_URL=f'{url_prefix}{uname}'
                driver.get(profile_URL)
                try :
                    empty_state_element = driver.find_element(By.XPATH, '//*[@data-testid="empty_state_header_text"]')
                    print(empty_state_element.is_displayed())
                    if empty_state_element.is_displayed():
                        pass
                except NoSuchElementException:
                    continue
        
                try:
                    
                    wait.until(EC.presence_of_element_located(element_locator))
                    
                    display_name=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]').text
                    date_joined=driver.find_element(By.XPATH,'.//*[@data-testid="UserJoinDate"]').text
                    try:
                        user_description=driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[1]/div[3]/div/div').text
                    except NoSuchElementException:
                        user_description='N/A'
                    try:
                        user_birthdate=driver.find_element(By.XPATH,'.//*[@data-testid="UserBirthdate"]').text
                    except NoSuchElementException:
                        user_birthdate='N/A'
                    try:
                        user_location=driver.find_element(By.XPATH,'.//*[@data-testid="UserLocation"]').text
                    except NoSuchElementException:
                        user_location='N/A'
                        
                    try:
                        user_following=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span').text
                    except:
                        user_following='N/A'
                    try:
                        user_followers=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span').text
                    except:
                        user_followers='N/A'
                    try:
                        num_of_posts=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div').text
                        num_of_posts = num_of_posts.split(' ')[0]
                    except:
                        num_of_posts='N/A'    
                    try: 
                        isVerified=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[2]/span/span/div/div')
                        verified='Yes'
                    except:
                        verified='No'
                
                    ProfileData.append((uname,display_name,user_birthdate,user_description,user_location,user_followers,user_following,verified,num_of_posts,date_joined))
                    new_data_df = pd.DataFrame(ProfileData, columns=['Username','Display Name','Birth Date','Description','Location','Followers','Following','Verified','Number of Posts','Date Joined'])
        
                    file_exists = os.path.exists(ProfileDataFile)
                    mode = 'a' if file_exists else 'w'
                    new_data_df.to_csv(ProfileDataFile, mode=mode, index=False, header=not file_exists)            
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error processing profile for {uname}: {str(e)}")
                    time.sleep(2)
                    continue
            driver.quit()
            break
        except Exception as e:
            print(f"Error Logging in.. : {e}")
            retry_count += 1
            print(f"Retrying in 6 minutes (Attempt {retry_count}/5)")
            time.sleep(360)  # Wait for 6 minutes before retrying