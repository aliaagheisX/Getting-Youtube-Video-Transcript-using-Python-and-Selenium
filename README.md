# Getting YouTube videos' transcripts using Python and Selenium


This project consists of two modules. \
Module one ```get_video_transcript.py``` takes a YouTube link and returns the transcript, Module two ```get_videos_by_search.py``` takes a search query and returns the transcript of the top videos. Both return values as text and as dataframes (videos - chapters - timestamps).


## To Use

1. check the version of chrome from chrome://version

2. download a suitable version of Chrome driver https://chromedriver.storage.googleapis.com/index.html

3. put the executable files in C:\seleniumDrivers

You will need to modify that code line if you move it to another directory

```

os.environ['PATH'] += r"C:\seleniumDrivers"

```