import os
import shutil
import subprocess
import tkinter.filedialog
import threading
from tkinter import *
import tkinter as tk
from tkinter import ttk
import time
from bs4 import BeautifulSoup as bs
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

s = requests.session()
fileopen = open(".config", 'r')
buxmail = fileopen.readline().split(" ")[0]
fileopen.close()


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        canvas.config(width=500, height=400)
        scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        canvas.bind_all("<MouseWheel>",
                        lambda event: canvas.yview_scroll(
                            int(-1*(event.delta/120)), "units")
                        )
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(self, event):
        self.yview_scroll(-1*(event.delta/120), "units")


def folderchange():
    ab = tkinter.filedialog.askdirectory()
    global folder
    folder = ab
    file9 = open('.config', 'a')
    file9.write("\n"+folder)
    return folder


def step(k):
    prg['value'] = k


def starting(sps, folder, topic, content):
    t = threading.Thread(target=Video, args=(sps, folder, topic, content))
    t.daemon = True
    t.start()


def replace(string):
    return string.replace(" ", "_").replace("&", "_and_").replace(
        "/", "_or_").replace("\\", "_or_").replace("(", "_").replace(
            ")", "_").replace("[", "_").replace("]", "_").replace("{", "_").replace(
                "}", "_").replace(".", "").replace(",", "and")


def Video(sps, folder, topic, content, tono, vino):
    print("topic:", topic, "tono:", tono, "vino:", vino)
    ab = '%SYSTEMROOT%\System32\WindowsPowerShell\\v1.0\powershell.exe -Command ' + \
        "md "+folder+"/"+str(tono)+"."+replace(topic)
    print(ab)
    process = subprocess.Popen(
        ab, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("folder in Video:", folder)
    topic_lbl.config(text="Topic: ")
    content_lbl.config(text="Content: ")
    topicx_lbl.config(text=topic)
    contentx_lbl.config(text=content)
    status.config(text="Donloading...")
    folder += "/"+str(tono)+"."+replace(topic)+"/"+str(vino) + "-"
    print("Folder in 2nd video: ", folder)
    hq = './main '+sps+" --write-auto-sub --write-srt --sub-lang en --convert-subs=srt -f 'bestvideo+bestaudio/bestvideo+bestaudio'  --merge-output-format mp4 --newline -o "
    hq += folder + "'%(title)s.%(ext)s'"
    ab = '%SYSTEMROOT%\System32\WindowsPowerShell\\v1.0\powershell.exe -Command ' + hq
    print(hq)
    process = subprocess.Popen(
        ab, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    Done = True
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            line = str(output.strip().decode('ansi'))
            print(line)
            if(len(line.split()) > 7):
                if (line.split()[0] == "[download]"):
                    if(line.split()[1] == '100'):
                        ml = Message(
                            root, text="Already Downloaded", width=400).pack()
                        continue

                    pbar = line.split()[1][:-3]
                    try:
                        int(pbar)
                    except:
                        continue
                    spd = line.split()[5]
                    lbl.config(text="Speed "+spd)
                    prc = line.split()[1]
                    prclbl.config(text=prc+" Done")
                    eta = line.split()[7]
                    etalbl.config(text="ETA " + eta)
                    step(int(pbar))
                    # root.update_idletasks()
                    # time.sleep(.1)
                    print(int(pbar))
                    if (int(pbar) == 100):
                        lbl.config(text=spd)
                        status.config(text="Converting...")
        if(process.poll() == 0):
            return


def signin():
    nwindow = Tk()
    nwindow.geometry('250x200')
    nwindow.resizable(False, False)
    nwindow.title('Login')
    tops = Label(nwindow, text="        ").grid(row=0)
    mlps = Label(nwindow, text="buX Email  ").grid(row=1, column=1)
    em = Entry(nwindow, width=20)
    em.grid(row=1, column=2)
    brk1s = Label(nwindow, text="").grid(row=2)
    sltp = Label(nwindow, text="Password ").grid(row=3, column=1)
    ep = Entry(nwindow, width=20, show="*")
    ep.grid(row=3, column=2)
    brk4s = Label(nwindow, text="").grid(row=4)
    myButton = Button(nwindow, text="Login", anchor='center', command=lambda: get_Courses(
        em.get(), ep.get(), nwindow)).grid(row=5, column=2)
    nwindow.mainloop()


def check(url):
    soup = bs(s.get(url).text, 'html.parser')
    for a in soup.findAll("li", {"class": "outline-item section"}):
        for b in a.findAll("li", {"class": "subsection accordion"}):
            c = b.find("h4", {"class": "subsection-title"})
            d = b.find("ol", {"class": "outline-item accordion-panel"})
            content = c.text.rstrip().lstrip()
            print(content)
            for e in b.findAll("li", {"class": "vertical outline-item focusable"}):
                f = e.find("a", {"class": "outline-item focusable"}, "href")
                g = f.find("div", {"class": "vertical-title"})
                address = g.text.rstrip().lstrip(), f['href']
                print(address)


def get_Courses(a, b, nwindow):
    filehand = open('.config', 'w')
    wr = a + " " + b
    filehand.write(wr)
    filehand.close()
    nwindow.destroy()
    root.update_idletasks()
    root.deiconify()
    top.config(text=a)
    return


def main_page():
    root.mainloop()


def start():
    global folder
    link = e.get()
    status.configure(text="Opening Browser. Please Wait...")
    print("Folder: ", folder)
    if("https://youtu.be" in link or "youtube" in link):
        folder = tkinter.filedialog.askdirectory()
        thr = threading.Thread(target=Video, args=(
            link, folder, "", "", "", ""))
        thr.daemon = True
        thr.start()
        return
    if "bux" not in link:
        status.config(text="Invalid Link. Please Try Again.")
        return

    if("courseware" in link):
        folder = tkinter.filedialog.askdirectory()
        thr = threading.Thread(target=single_lecture, args=(link, folder))
        thr.daemon = True
        thr.start()
        return
    print(folder)
    if(folder == " " or folder == "" or folder == None or folder == "  "):
        folder = folderchange()
    thr = threading.Thread(target=session, args=(link, folder))
    thr.daemon = True
    thr.start()


def single_lecture(link, folder):
    status.config(text="Collecting Links, Please Wait..")

    driver = webdriver.Edge(".\edge.exe")
    driver.get("https://bux.bracu.ac.bd/login?next=%2F")
    tick = driver.find_element_by_id("remember-yes")
    tick.click()
    filehand = open('.config', 'r')
    read = filehand.readline()
    filehand.close()
    mail = read.split()[0]
    passwd = read.split()[1]
    smail = driver.find_element_by_id("email")
    smail.send_keys(mail)
    passw = driver.find_element_by_id("password")
    passw.send_keys(passwd)
    passw.send_keys(Keys.RETURN)
    topic = ""
    content = ""
    tono = ""
    vino = ""
    time.sleep(1)
    string = browser(driver, link, folder,
                     topic, content, tono, vino)


def session(link, folder):
    fileopens = open(".courses", "r")
    checkall = fileopens.readlines()
    fileopens.close()
    exists = False
    for checkone in checkall:
        if link in checkone:
            exists = True
    print(exists)
    if(exists == False):
        filewrite = open(".courses", "a")
        filewrite.write(link+"\n")
        print("Written")
        filewrite.close()
    course_name.config(text=link.split("+")[1])
    filehand = open('.config', 'r')
    ab = '%SYSTEMROOT%\System32\WindowsPowerShell\\v1.0\powershell.exe -Command ' + \
        'md '+folder+"/"+link.split("+")[1]
    folder += "/"+replace(link.split("+")[1])
    process = subprocess.Popen(
        ab, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    read = filehand.readline()
    filehand.close()
    mail = read.split()[0]
    passwd = read.split()[1]
    print(mail, passwd)
    URL = 'https://bux.bracu.ac.bd/'

    LOGIN_ROUTE = 'login_ajax'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
               'origin': URL, 'referer': URL + LOGIN_ROUTE}
    s = requests.session()
    csrf_token = s.get(URL).cookies['csrftoken']
    login_payload = {
        'email': mail,
        'password': passwd,
        'remember': 'true',
        'csrfmiddlewaretoken': csrf_token
    }
    login_req = s.post(URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)
    print(login_req.status_code)
    cookies = login_req.cookies
    url = link
    soup = bs(s.get(url).text, 'html.parser')
    print(link)
    status.config(text="Collecting Links, Please Wait..")
    driver = webdriver.Edge(".\edge.exe")
    # driver.maximize_window()
    driver.get("https://bux.bracu.ac.bd/login?next=%2F")
    tick = driver.find_element_by_id("remember-yes")
    tick.click()
    smail = driver.find_element_by_id("email")
    smail.send_keys(mail)
    passw = driver.find_element_by_id("password")
    passw.send_keys(passwd)
    passw.send_keys(Keys.RETURN)
    tono = 1
    vino = 1
    tonochange = False
    for a in soup.findAll("li", {"class": "outline-item section"}):
        for b in a.findAll("li", {"class": "subsection accordion"}):
            c = b.find("h4", {"class": "subsection-title"})
            d = b.find("ol", {"class": "outline-item accordion-panel"})
            topic = c.text.rstrip().lstrip()
            print(topic)
            time.sleep(2)
            for e in b.findAll("li", {"class": "vertical outline-item focusable"}):
                f = e.find(
                    "a", {"class": "outline-item focusable"}, "href")
                g = f.find("div", {"class": "vertical-title"})
                content = g.text.rstrip().lstrip()
                address = f['href']
                filelinks = open('.links', "r")
                readlinks = filelinks.readlines()
                filelinks.close()
                ShouldPass = True
                for line in readlinks:
                    if address in line:
                        ShouldPass = False
                if(ShouldPass):
                    string = browser(driver, address, folder,
                                     topic, content, tono, vino)
                    print("string:", string)
                    if(string != None):
                        vino = string
                        tonochange = True
                    filelinks = open('.links', "a")
                    filelinks.write(address+"\n")
                    filelinks.close()
            if tonochange:
                tono += 1
                tonochange = False
    driver.close()
    status.config(text="All Done for this course.")


def browser(driver, address, folder, topic, content, tono, vino):
    driver.get(address)
    print(address)
    time.sleep(5)
    try:
        selects = driver.find_elements_by_xpath(
            '//iframe[starts-with(@src, "https://www.youtube.com/embed")]')
        for select in selects:
            source_url = select.get_attribute('src')
            vid_url = "https://youtu.be" + \
                source_url.split("?controls")[0].split("/embed")[1]
            print(folder, topic, content, tono, vino)
            if(vid_url != -1 and vid_url is not None):
                print("this", vid_url)
                Video(vid_url, folder, topic, content, tono, vino)
                vino += 1
        print(selects[0])
        return vino
    except:
        print("Video Not Available")
        return None


def logout(wind):
    file3 = open('.config', 'w')
    file3.write("")
    file3.close()
    wind.withdraw()
    signin()


def multiple():
    global folder
    status.configure(text="Opening Browser. Please Wait...")
    coursfile = open('.courses', "r")
    readcours = coursfile.readlines()
    coursfile.close()
    print(readcours)
    lst = e.get()
    print(lst)
    for ls in lst.split(","):
        if ls not in readcours and "bux" in ls:
            coursfile = open('.courses', "a")
            coursfile.write(ls+"\n")
            coursfile.close()

    coursfile = open('.courses', "r")
    readcours = coursfile.readlines()
    coursfile.close()
    print(readcours)
    if(readcours == "" or readcours == ","):
        status.config(text="Invalid Link, Try Again.")
        return
    if folder == "" or folder == " " or folder == None or folder == "\n" or folder == "  ":
        folder = folderchange()
    print(folder)
    for link in readcours:
        session(link, folder)
    course_name.config(text="Download Completed for All Courses.")


def multiple_threads():
    thr = threading.Thread(target=multiple)
    thr.daemon = True
    thr.start()


def allDatecheck():
    file4 = open('.courses', 'r')
    listcourses = file4.readlines()
    file4.close()
    notes = ""
    filehand = open('.config', 'r')
    read = filehand.readline()
    filehand.close()
    mail = read.split()[0]
    passwd = read.split()[1]
    for course in listcourses:
        URL = 'https://bux.bracu.ac.bd/'

        LOGIN_ROUTE = 'login_ajax'
        HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                   'origin': URL, 'referer': URL + LOGIN_ROUTE}
        s = requests.session()
        csrf_token = s.get(URL).cookies['csrftoken']
        login_payload = {
            'email': mail,
            'password': passwd,
            'remember': 'true',
            'csrfmiddlewaretoken': csrf_token
        }
        login_req = s.post(URL + LOGIN_ROUTE,
                           headers=HEADERS, data=login_payload)
        print(login_req.status_code)
        cookies = login_req.cookies
        url = course
        soup = bs(s.get(url).text, 'html.parser')
        notes += "\n\n Showing Tasks for Course : " + \
            course.split("+")[1] + "\n\n"
        for a in soup.findAll("li", {"class": "subsection accordion"}):
            b = a.find(
                "span", {"class": "localized-datetime subtitle-name"}, "data-datetime")
            month = {'01': 'January',
                     '02': 'February',
                     '03': 'March',
                     '04': 'April',
                     '05': 'May',
                     '06': 'June',
                     '07': 'July',
                     '08': 'August',
                     '09': 'September',
                     '10': 'October',
                     '11': 'November',
                     '12': 'December'}
            if b != None and len(b['data-datetime']) > 10:
                c = a.find("h4", {"class": "subsection-title"})
                count = b['data-datetime'][5:7]
                intcount = int(b['data-datetime'][5:7])
                time = int(b['data-datetime'][11:13])
                time += 6
                strdate = b['data-datetime'][8:10]
                date = int(strdate)
                mins = b['data-datetime'][14:16]
                if (time == 24):
                    time = 11
                    mins = '59'
                    if (date == 0):
                        intcount -= 1
                        if (count[0] == '0'):
                            count += '0' + str(intcount)
                        else:
                            count += str(intcount)
                        if (intcount == 4 or intcount == 6 or intcount == 9 or intcount == 11):
                            date = 30
                        else:
                            date = 31
                notes += "    " + month[count] + "  " + str(date) + " at " + str(
                    time) + ":" + mins + " :    " + c.text.rstrip().lstrip() + "\n"
    view(notes)


def cleardata():
    print("Here")
    filelist = open(".links", "w")
    filelist.write("")
    filelist.close()
    filelist = open(".courses", "w")
    filelist.write("")
    filelist.close()
    status.config(text="Cleared all data.")
    return


def view(text):
    window2 = Tk()
    window2.title('Tasks')
    window2.resizable(False, False)
    frame = ScrollableFrame(window2)
    ttk.Label(frame.scrollable_frame, text=text).pack()
    frame.pack()
    window2.mainloop()


def showAllDates():

    t = threading.Thread(target=allDatecheck())
    t.daemon = True
    t.start()


file8 = open('.config', 'r')
infos = file8.readlines()
folder = ""
try:
    info = infos[0]
except:
    info = ""
file8.close()
try:
    folder = infos[1].lstrip().rstrip()
except:
    folder = None


root = Tk()
root.geometry('800x350')
root.resizable(False, False)
root.title('Download Process')
lef = Label(root, text="    ").grid(row=0, column=0, sticky=E)
top = Label(root, text="    "+buxmail)
top.grid(row=1, column=1, sticky=E)
top2 = Label(root, text="            ").grid(row=0)
mlp = Label(root, text="    Enter URL").grid(row=2, column=1, sticky=E)
e = Entry(root, width=20)
e.grid(row=2, column=2)
brk0 = Label(root, text="").grid(row=3)

frame = Frame(root)
frame.grid(row=14, column=1, columnspan=5, sticky=W)
frame2 = Frame(root)
frame2.grid(row=15, column=1, columnspan=5, sticky=W)
#brk3 = Label(root, text="Download Status:", font=44).grid(row=6, columnspan=4)
topic_lbl = Label(frame, text="")
topic_lbl.grid(row=0, column=0, sticky=E)
topicx_lbl = Label(frame, text=" ")
topicx_lbl.grid(row=0, column=1, sticky=W)
content_lbl = Label(frame2, text="")
content_lbl.grid(row=1, column=0, sticky=E)
contentx_lbl = Label(frame2, text=" ")
contentx_lbl.grid(row=1, column=1, sticky=W)
#brk1 = Label(root, text="").grid(row=9)
status = Label(
    root, text="Enter your course/video link to start downloading")
status.grid(row=10, columnspan=5)
prg = ttk.Progressbar(root, orient=HORIZONTAL, length=700, mode='determinate')
prg.grid(row=12, columnspan=5, column=1)
course_name = Label(root)
course_name.grid(row=11, columnspan=5)
prclbl = Label(root)
prclbl.grid(row=13, column=1)
etalbl = Label(root)
etalbl.grid(row=13, column=5)
lbl = Label(root)
lbl.grid(row=13, column=3)

alldates = Button(root, text="See All Tasks", anchor='center',
                  command=showAllDates).grid(row=2, column=5)

signout = Button(root, text="Sign Out", anchor='center',
                 command=lambda: logout(root)).grid(row=17, column=5)
clear = Button(root, text="Clear Data", anchor='center',
               command=cleardata).grid(row=17, column=4)

dld_btn = Button(root, text="Single Download", anchor='center',
                 command=start).grid(row=2, column=3)
dld_btn = Button(root, text="Multiple Download", anchor='center',
                 command=multiple_threads).grid(row=2, column=4)

topic = ""
content = ""
address = ""
link = ""
if (info == " " or info == ""):
    root.withdraw()
    signin()
else:
    main_page()
