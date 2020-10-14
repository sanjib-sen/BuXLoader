# BuXLoader

### Description:
This is an automated software which will download Lecture Videos from BuX. BuX is an online platform for academic activites of BRAC University. Teachers upload their lecture contents and take examinations,assignments and quizzes from here, just like edX. This software will look for video lectures in a particular course and download them automatically. 

## Images
![Main](/Screenshots/show.png)

### Features:
1. Resume downloading videos in case of Crash/Hang or network failure.
2. Only download new Lecture Videos which are not downloaded. 
3. Will show deadline of upcoming Assignments/Quizzes or exams. 
4. Support for file and folder indexing for better organization.
5. Autamically download subtitles for Videos.

### Alpha Version Notes:
1. As of now, the software only supports <b> Microsft Edge (Latest Version 86, Chromium) </b>. It is because, selenium is experiencing a chromedriver issue which hasn't been fixed by Chrome Developers yet. I will update and release the software for chrome if they fixes it. Check the problem yourself by running the software with chrome webdriver.
2. I am also thinking of removing the File/Folder indexing feature. Sometimes it looks a little bit messy, doesn't it? What do you think? Also it will be more stable. Whatever. 
3. Needs a lot of changes. But I also need to sleep now. 


### Installation:
1. Download and Extract [BuXLoader_Edge_.v01](https://github.com/sanjib-sen/BuXLoader/releases/download/v0.1/BuXLoader_Edge_.v01.zip)
2. Run **BuXLoader.exe**

### Modules Used:
1. selenium
2. beautifuslou4
3. requests
4. tkinter

### Instruction for Developers:
1. Download Python 3.9
2. Install [pip](https://pip.pypa.io/en/stable/installing/)
3. Install beautifulsoup4, selenium, requests through pip. 
4. Git Clone: https://github.com/sanjib-sen/BuXLoader
5. Open BuXLoader.pyw with your IDE/Editor.
