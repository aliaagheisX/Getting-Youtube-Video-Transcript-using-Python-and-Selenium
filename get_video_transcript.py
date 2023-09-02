import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

""" 
1. check the version of chrome from chrome://version
2. download suitable version of chrome driver https://chromedriver.storage.googleapis.com/index.html
3. put the executable files in C:\seleniumDrivers
"""

def get_video_transcript(url: str,video_id: int, chapters_dict, transcripts_dict, driver, wait):
    """ 
        return the video transcripts as DataFrames 
        :return : chapters_df, transcripts_df
        if not exist return None, None
    """

    # 1. go to url
    driver.get(url)

    # 2. click on show more button
    show_more_button = wait.until(EC.element_to_be_clickable( driver.find_element(By.CSS_SELECTOR, "#button-shape button")))
    show_more_button.click()

    # 3. click on transcript button [and check if it exist]
    try: 
        transcript_button = wait.until(EC.element_to_be_clickable( driver.find_element(By.XPATH, "//yt-formatted-string[text()='Show transcript']")))
        transcript_button.click()
    except NoSuchElementException:
        print("No Transcript Exist")
        return None


    # 4. extract data
    
    curr_cid = -1
    video_txt = ""
    # 4.1 loop on transcripts 
    transcripts = driver.find_elements(By.XPATH, "//div[@id='segments-container']/*")

    for transcript in transcripts:
        if 'header' in transcript.tag_name:
            curr_cid = len(chapters_dict['headline'])
            chapters_dict['headline'].append(transcript.text)
            chapters_dict['txt'].append("")
            chapters_dict['vid'].append(video_id)
        else:
            data = transcript.text.splitlines() # [timestamp, txt]
            video_txt += " " + data[1]
            transcripts_dict['cid'].append(curr_cid)
            transcripts_dict['timestamp'].append(data[0])
            transcripts_dict['txt'].append(data[1])
            transcripts_dict['vid'].append(video_id)
            if curr_cid != -1: 
                chapters_dict['txt'][curr_cid] += " " + data[1]

    return video_txt

if __name__ == '__main__':
    # here were I put the web driver
    os.environ['PATH'] += r"C:\seleniumDrivers"
    driver = webdriver.Chrome(executable_path=r"C:\seleniumDrivers\\chromedriver.exe")
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 10)

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



    txt = get_video_transcript(
        "https://www.youtube.com/watch?v=olU_Qm6DJtA",
        0,
        chapters_dict, 
        transcripts_dict, 
        driver, 
        wait
    )
    print(txt)
    # pd.DataFrame(chapters_dict).to_csv('chapters.csv', index=False)
    # pd.DataFrame(transcripts_dict).to_csv('transcripts.csv', index=False)
    # with open("output.txt", "w") as file:
    #     file.write(txt)
