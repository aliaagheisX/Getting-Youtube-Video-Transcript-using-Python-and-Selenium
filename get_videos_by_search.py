import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_video_transcript import get_video_transcript

def get_videos_by_search(search_query:str, videos_dict, chapters_dict, transcripts_dict, driver, wait):
    """
        :return : dataframes of videos, chapters, transcripts
        - search on youtube for search_query
        - get top videos transcripts
        
    """
    
    driver.get("https://www.youtube.com/")
    # write product name to search 
    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#search')))
    search_input.send_keys(search_query)
    # click on search button
    driver.find_element(By.ID, 'search-icon-legacy').click()
    # get videos list
    videos = driver.find_elements(By.TAG_NAME, 'ytd-video-renderer')
    # store index of unprocesed videos
    lst_processed_vid = len(videos_dict['title']) 

    # first loop on videos and collect metadata [title, url]
    for video in videos:
        video_data = video.find_element(By.ID,'video-title')
        video_link = video_data.get_attribute('href')

        videos_dict['title'].append(video_data.text)
        videos_dict['url'].append(video_link)

    # loop on unprocess videos and collect transcript
    for video_url in videos_dict['url'][lst_processed_vid:]:
        try: 
            video_txt = get_video_transcript(
                video_url, 
                lst_processed_vid, 
                chapters_dict, 
                transcripts_dict, 
                driver, 
                wait
            ) 
            # if  transcript found  add it else remove video from data
            if video_txt is not None: 
                videos_dict['txt'].append(video_txt)
                lst_processed_vid += 1
            else:
                videos_dict['title'].pop(lst_processed_vid)
                videos_dict['url'].pop(lst_processed_vid)
        except Exception as e:
            print("error: ", e)
            videos_dict['title'].pop(lst_processed_vid)
            videos_dict['url'].pop(lst_processed_vid)


if __name__ == '__main__':
    # where I put the chrome driver 
    os.environ['PATH'] += r"C:\seleniumDrivers"
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    wait = WebDriverWait(driver, 10)

    videos_dict = {
        'title': [],
        'url' : [],
        'txt': []
    }
    chapters_dict = {
        'headline': [], 
        'txt': [],
        'vid': [],
    }

    transcripts_dict = {
        'txt' : [],
        'timestamp': [],
        'cid' : [],
        'vid' : []
    }
    get_videos_by_search(
        "Coffee Machine Reviews",
        videos_dict,
        chapters_dict,
        transcripts_dict,
        driver, 
        wait
    )
    pd.DataFrame(videos_dict).to_csv('videos.csv', index=False)
    pd.DataFrame(chapters_dict).to_csv('chapters.csv', index=False)
    pd.DataFrame(transcripts_dict).to_csv('transcripts.csv', index=False)

