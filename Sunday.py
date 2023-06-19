import wikipedia,webbrowser,os,random,requests,pyautogui,playsound,subprocess,time
import urllib.request,bs4 as bs,sys,threading
import Annex,wolframalpha
from ttkthemes import themed_tk
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk,Image
import sqlite3,pyjokes,pywhatkit
from functools import partial
import getpass,calendar
from pytz import timezone
import datetime
import subprocess


fmt="%Y-%m-%d %H:%M:%S "

try:
    app=wolframalpha.Client("JPK4EE-L7KR3XWP9A")  #API key for wolframalpha
except Exception as e:
    pass

#setting chrome path
chrome_path="C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

def there_exists(terms,query):
    for term in terms:
        if term in query:
            return True

def CommandsList():
    '''show the command to which voice assistant is registered with'''
    os.startfile('Commands List.txt')

def clearScreen():
    ''' clear the scrollable text box'''
    SR.scrollable_text_clearing()


def greet():

    conn = sqlite3.connect('Sunday.db')
    mycursor=conn.cursor()
    hour=int(datetime.datetime.now().hour)
    if hour>=4 and hour<12:
        mycursor.execute('select sentences from goodmorning')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=12 and hour<18:
        mycursor.execute('select sentences from goodafternoon')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=18 and hour<21:
        mycursor.execute('select sentences from goodevening')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    else:
        mycursor.execute('select sentences from night')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    conn.commit()
    conn.close()
    SR.speak("\nMyself Sunday, Sir How may I help you?")
    SR.speak("\n(Please add your login through login portal, ignore if already added)")

def mainframe():
    """Logic for execution task based on query"""
    SR.scrollable_text_clearing()
    greet()
    query_for_future=None
    try:
        while(True):
            query=SR.takeCommand().lower()          #converted the command in lower case of ease of matching

            #wikipedia search
            if there_exists(['search wikipedia for','from wikipedia'],query):
                SR.speak("Searching wikipedia...")
                if 'search wikipedia for' in query:
                    query=query.replace('search wikipedia for','')
                    results=wikipedia.summary(query,sentences=2)
                    SR.speak("According to wikipedia:\n")
                    SR.speak(results)
                elif 'from wikipedia' in query:
                    query=query.replace('from wikipedia','')
                    results=wikipedia.summary(query,sentences=2)
                    SR.speak("According to wikipedia:\n")
                    SR.speak(results)
            elif there_exists(['wikipedia'],query):
                SR.speak("Searching wikipedia....")
                query=query.replace("wikipedia","")
                results=wikipedia.summary(query,sentences=2)
                SR.speak("According to wikipedia:\n")
                SR.speak(results)

            #jokes
            elif there_exists(['tell me joke','tell me a joke','tell me some jokes','i would like to hear some jokes',"i'd like to hear some jokes",
                            'can you please tell me some jokes','i want to hear a joke','i want to hear some jokes','please tell me some jokes',
                            'would like to hear some jokes','tell me more jokes'],query):
                SR.speak(pyjokes.get_joke(language="en", category="all"))
                query_for_future=query
            elif there_exists(['one more','one more please','tell me more','i would like to hear more of them','once more','once again','more','again'],query) and (query_for_future is not None):
                SR.speak(pyjokes.get_joke(language="en", category="all"))

            #asking for name
            elif there_exists(["what is your name","what's your name","tell me your name",'who are you'],query):
                SR.speak("My name is Sunday and I'm here for you.")
            #How are you
            elif there_exists(['how are you'],query):
                conn = sqlite3.connect('Sunday.db')
                mycursor=conn.cursor()
                mycursor.execute('select sentences from howareyou')
                result=mycursor.fetchall()
                temporary_data=random.choice(result)[0]
                SR.updating_ST_No_newline(temporary_data+'😃\n')
                SR.nonPrintSpeak(temporary_data)
                conn.close()
            #what is my name
            elif there_exists(['what is my name','tell me my name',"i don't remember my name"],query):
                SR.speak("Your name is Ishan Saraswat from 9 E")
                

            #my lovely frnds
            elif there_exists(['my lovely friends','my friends', 'tell me about my friends'],query):
                SR.speak("Sure, Here is a small summary about your social friends-: \n") 
                SR.speak("The Homies Category: \n")
                SR.speak("(1) Aman - Your childhood friend, the closest one of all. \n")
                SR.speak("(2) Arihant - Your brother-from-another-mother, your life-teacher. \n")
                SR.speak("(3) Atharva Naman - Your also brother-from-another-mother, your technical friend. \n")
                SR.speak("The Girl category: \n")
                SR.speak("(1) Ushika - Your female best friend, the closest one in girls. \n")
                SR.speak("(2) Kastury - Your also female best friend, your close sister. \n")
                SR.speak("(3) Rayna - Your also female best friend, the one who understand you the most. \n")
                SR.speak("The Anonymous - Your second-half, the one who took your sleep and the one am named after...., the most important of all(except the homies)\n")
                
            #calendar
            elif there_exists(['show me calendar','display calendar'],query):
                SR.updating_ST(calendar.calendar(2023))

            #google, youtube and location
            #playing on youtube
            elif there_exists(['open youtube and play','on youtube'],query):
                if 'on youtube' in query:
                    SR.speak("Opening youtube")
                    pywhatkit.playonyt(query.replace('on youtube',''))
                else:
                    SR.speak("Opening youtube")
                    pywhatkit.playonyt(query.replace('open youtube and play ',''))
                
            elif there_exists(['play some songs on youtube','i would like to listen some music','i would like to listen some songs','play songs on youtube'],query):
                SR.speak("Opening youtube")
                pywhatkit.playonyt('play random songs')
                
            elif there_exists(['open youtube','access youtube'],query):
                SR.speak("Opening youtube")
                webbrowser.get(chrome_path).open("https://www.youtube.com")
                
            elif there_exists(['open google and search','google and search'],query):
                url='https://google.com/search?q='+query[query.find('for')+4:]
                webbrowser.get(chrome_path).open(url)
                
            elif there_exists(['open my profile website','open my website', 'portfolio', 'open my personal website'],query):
                url='https://ishansaraswat28.github.io/Ishan-Saraswat---Profile.github.io/'+query[query.find('for')+4:]
                webbrowser.get(chrome_path).open(url)
                
            elif there_exists(['open my github','open my github account', 'github web',],query):
                url='https://github.com/IshanSaraswat28'+query[query.find('for')+4:]
                webbrowser.get(chrome_path).open(url)
                
            #image search
            elif there_exists(['show me images of','images of','display images'],query):
                url="https://www.google.com/search?tbm=isch&q="+query[query.find('of')+3:]
                webbrowser.get(chrome_path).open(url)
                
            elif there_exists(['search for','do a little searching for','show me results for','show me result for','start searching for'],query):
                SR.speak("Searching.....")
                if 'search for' in query:
                    SR.speak(f"Showing results for {query.replace('search for','')}")
                    pywhatkit.search(query.replace('search for',''))
                elif 'do a little searching for' in query:
                    SR.speak(f"Showing results for {query.replace('do a little searching for','')}")
                    pywhatkit.search(query.replace('do a little searching for',''))
                elif 'show me results for' in query:
                    SR.speak(f"Showing results for {query.replace('show me results for','')}")
                    pywhatkit(query.replace('show me results for',''))
                elif 'start searching for' in query:
                    SR.speak(f"Showing results for {query.replace('start searching for','')}")
                    pywhatkit(query.replace('start searching for',''))
                

            elif there_exists(['open google'],query):
                SR.speak("Opening google")
                webbrowser.get(chrome_path).open("https://www.google.com")
                
            elif there_exists(['find location of','show location of','find location for','show location for'],query):
                if 'of' in query:
                    url='https://google.nl/maps/place/'+query[query.find('of')+3:]+'/&amp'
                    webbrowser.get(chrome_path).open(url)
                    
                elif 'for' in query:
                    url='https://google.nl/maps/place/'+query[query.find('for')+4:]+'/&amp'
                    webbrowser.get(chrome_path).open(url)
                    
            elif there_exists(["what is my exact location","what is my location","my current location","exact current location"],query):
                url = "https://www.google.com/maps/search/Where+am+I+?/"
                webbrowser.get().open(url)
                SR.speak("Showing your current location on google maps...")
                
            elif there_exists(["where am i"],query):
                Ip_info = requests.get('https://api.ipdata.co?api-key=test').json()
                loc = Ip_info['region']
                SR.speak(f"You must be somewhere in {loc}")

            elif there_exists(["open canva","turn on canva","access canva"],query):
                url="https://www.canva.com/"
                webbrowser.get().open(url)
                SR.speak("Opening canva")

            elif there_exists(["open school app", "open school portal", "open portal", "open school website", "open edulakshya"],query):
                url="https://sajsvg.edulakshya.in/parent_dashboard"
                webbrowser.get().open(url)
                SR.speak("Opening school portal")

            elif there_exists(["open zoro.to", "open zoro dot to", "i want to watch anime", "play anime", "watch some anime", "watch anime", "anime"],query):
                SR.speak("Sure, which anime would you like to watch?")
                while(True):
                    query=SR.takeCommand().lower()
                    if('one piece' in query) or ('goat piece' in query):
                        url="https://sanji.to/one-piece-100?ref=search"
                        webbrowser.get().open(url)
                        SR.speak("Playing One Piece")
                    elif('naruto' in query) or ('ninja anime' in query):
                        url="https://sanji.to/naruto-677?ref=search"
                        webbrowser.get().open(url)
                        SR.speak("Playing Naruto")
                    elif('tokyo revengers' in query) or ('tokyo gangsters' in query):
                        url="https://sanji.to/tokyo-revengers-15585?ref=search"
                        webbrowser.get().open(url)
                        SR.speak("Playing Tokyo Revengers")
                    else:
                        SR.speak("Sorry please repeat the anime you want to see")
                        break
            #who is searcing mode
            elif there_exists(['who is','who the heck is','who the hell is','who is this'],query):
                query=query.replace("wikipedia","")
                results=wikipedia.summary(query,sentences=1)
                SR.speak("According to wikipdedia:  ")
                SR.speak(results)

            #play music
            elif there_exists(['play music','play some music for me','like to listen some music'],query):
                SR.speak("Playing musics")
                music_dir='C:\\Users\\Rahul\\Music'
                songs=os.listdir(music_dir)
                # print(songs)
                indx=random.randint(0,50)
                os.startfile(os.path.join(music_dir,songs[indx]))
            
            # top 5 news
            elif there_exists(['top 5 news','top five news','listen some news','news of today'],query):
                news=Annex.News(scrollable_text)
                news.show()

            #whatsapp message
            elif there_exists(['open whatsapp messeaging','send a whatsapp message','send whatsapp message','please send a whatsapp message'],query):
                whatsapp=Annex.WhatsApp(scrollable_text)
                whatsapp.send()
                del whatsapp
            #what is meant by
            elif there_exists(['what is meant by','what is mean by'],query):
                results=wikipedia.summary(query,sentences=2)
                SR.speak("According to wikipedia:\n")
                SR.speak(results)

            #taking photo
            elif there_exists(['take a photo','take a selfie','take my photo','take photo','take selfie','one photo please','click a photo'],query):
                takephoto=Annex.camera()
                Location=takephoto.takePhoto()
                os.startfile(Location)
                del takephoto
                SR.speak("Captured picture is stored in Camera folder.")

            #bluetooth file sharing
            elif there_exists(['send some files through bluetooth','send file through bluetooth','bluetooth sharing','bluetooth file sharing','open bluetooth'],query):
                SR.speak("Opening bluetooth...")
                os.startfile(r"C:\Windows\System32\fsquirt.exe")
                

            #play game
            elif there_exists(['would like to play some games','play some games','would like to play some game','want to play some games','want to play game','want to play games','play games','open games','play game','open game'],query):
                SR.speak("We have 2 games right now.\n")
                SR.updating_ST_No_newline('1.')
                SR.speak("Stone Paper Scissor")
                SR.updating_ST_No_newline('2.')
                SR.speak("Snake")
                SR.speak("\nTell us your choice:")
                while(True):
                    query=SR.takeCommand().lower()
                    if ('stone' in query) or ('paper' in query):
                        SR.speak("Opening stone paper scissor...")
                        sps=Annex.StonePaperScissor()
                        sps.start(scrollable_text)
                        
                    elif ('snake' in query):
                        SR.speak("Opening snake game...")
                        import Snake
                        Snake.start()
                        
                    else:
                        SR.speak("It did not match the option that we have. \nPlease say it again.")
                        break
            #makig note
            elif there_exists(['make a note','take note','take a note','note it down','make note','remember this as note','open notepad and write'],query):
                SR.speak("What would you like to write down?")
                data=SR.takeCommand()
                n=Annex.note()
                n.Note(data)
                SR.speak("I have a made a note of that.")
                
            elif there_exists(["toss a coin","flip a coin","toss"],query):
                moves=["head", "tails"]
                cmove=random.choice(moves)
                playsound.playsound('quarter-spin-flac.mp3')
                SR.speak("It's " + cmove)
            #time and date
            elif there_exists(['the time'],query):
                strTime =datetime.datetime.now().strftime("%H:%M:%S")
                SR.speak(f"Sir, the time is {strTime}")
            elif there_exists(['the date'],query):
                strDay=datetime.date.today().strftime("%B %d, %Y")
                SR.speak(f"Today is {strDay}")
            elif there_exists(['what day it is','what day is today','which day is today',"today's day name please"],query):
                SR.speak(f"Today is {datetime.datetime.now().strftime('%A')}")

            #opening software applications
            elif there_exists(['open chrome'],query):
                SR.speak("Opening chrome")
                os.startfile(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
                

            elif there_exists(['open notepad','start notepad'],query):
                SR.speak('Opening notepad')
                os.startfile(r'%windir%\system32\notepad.exe')
                
            elif there_exists(['open ms paint','open mspaint','open microsoft paint','start microsoft paint','start ms paint'],query):
                SR.speak("Opening Microsoft paint....")
                os.startfile('%windir%\system32\mspaint.exe')
                
            elif there_exists(['show me performance of my system','open performance monitor','performance monitor','performance of my computer','performance of this computer'],query):
                SR.speak("Opening performence monitoring...")
                os.startfile(r"%windir%\system32\taskmgr.exe")
                
            elif there_exists(['open snipping tool','snipping tool','start snipping tool'],query):
                SR.speak("Opening snipping tool....")
                os.startfile("C:\Windows\System32\SnippingTool.exe")
                
            elif there_exists(['open my directory','open my file ','open my files', 'open my code', 'open vs code'],query):
                SR.speak("Opeining vs code")
                codepath = r"C:\Users\Rahul\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                os.startfile(codepath)
                
            elif there_exists(['open file manager','file manager','open my computer','my computer','open file explorer','file explorer','open this pc','this pc'],query):
                SR.speak("Opening File Explorer")
                os.startfile("C:\Windows\explorer.exe")
                
            elif there_exists(['powershell'],query):
                SR.speak("Opening powershell")
                os.startfile(r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe')
                
            elif there_exists(['cmd','command prompt','command prom','commandpromt',],query):
                SR.speak("Opening command prompt")
                os.startfile(r'C:\Windows\System32\cmd.exe')
                
            elif there_exists(['open whatsapp'],query):
                SR.speak("Opening whatsApp")
                os.startfile(r'C:\Users\Vishal\AppData\Local\WhatsApp\WhatsApp.exe')
                
            elif there_exists(['open settings','open control panel','open this computer setting Window','open computer setting Window'   ,'open computer settings','open setting','show me settings','open my computer settings'],query):
                SR.speak("Opening settings...")
                os.startfile('C:\Windows\System32\control.exe')
                
            elif there_exists(['open your setting','open your settings','open settiing window','show me setting window','open voice assistant settings'],query):
                SR.speak("Opening my Setting window..")
                sett_wind=Annex.SettingWindow()
                sett_wind.settingWindow(root)
                
            elif there_exists(['open vlc','vlc media player','vlc player'],query):
                SR.speak("Opening VLC media player")
                os.startfile(r"C:\Program Files\VideoLAN\VLC\vlc.exe")
                

            #password generator
            elif there_exists(['suggest me a password','password suggestion','i want a password'],query):
                m3=Annex.PasswordGenerator()
                m3.givePSWD(scrollable_text)
                del m3
            #screeshot
            elif there_exists(['take screenshot','take a screenshot','screenshot please','capture my screen'],query):
                SR.speak("Taking screenshot")
                SS=Annex.screenshot()
                SS.takeSS()
                SR.speak('Captured screenshot is saved in Screenshots folder.')
                del SS

            #voice recorder
            elif there_exists(['record my voice','start voice recorder','voice recorder'],query):
                VR=Annex.VoiceRecorer()
                VR.Record(scrollable_text)
                del VR

            #text to speech conversion
            elif there_exists(['text to speech','convert my notes to voice'],query):
                SR.speak("Opening Text to Speech mode")
                TS=Annex.TextSpeech()
                del TS

            #weather report
            elif there_exists(['weather report of delhi','weather report of Delhi','temperature of delhi', 'temprature od Delhi'],query):
                
                while(True):
                    query=SR.takeCommand().lower()
                    if('Delhi' in query) or ('delhi' in query) or ("New delhi" in query) or ("new delhi" in query) or ("delhi" in query):
                        Weather=Annex.WeatherDelhi()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")
            elif there_exists(['weather report of pune', 'weather report of Pune', 'temprature of pune', 'temprature of Pune'],query):
                
                while(True):
                    if('Pune' in query) or ('pune' in query):
                        Weather=Annex.WeatherPune()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")
            elif there_exists(['weather report of kolkata', 'weather report of Kolkata', 'temprature of kolkata', 'temprature of Kolkata'],query):
                
                while(True):
                    if('Kolkata' in query) or ('kolkata' in query):
                        Weather=Annex.WeatherKolkata()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of mumbai', 'weather report of Mumbai', 'temprature of mumbai', 'temprature of Mumbai'],query):
                
                while(True):
                    if('Mumbai' in query) or ('mumbai' in query):
                        Weather=Annex.WeatherMumbai()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of goa', 'weather report of Goa', 'temprature of goa', 'temprature of Goa'],query):
                
                while(True):
                    if('Goa' in query) or ('goa' in query):
                        Weather=Annex.WeatherGoa()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of kerala', 'weather report of Kerala', 'temprature of kerala', 'temprature of Kerala'],query):
                
                while(True):
                    if('Kerala' in query) or ('kerala' in query):
                        Weather=Annex.WeatherKerala()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of chandigarh', 'weather report of Chandigarh', 'temprature of chandigarh', 'temprature of Chandigarh'],query):
                
                while(True):
                    if('Chandigarh' in query) or ('chandigarh' in query):
                        Weather=Annex.WeatherChandigarh()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of punjab', 'weather report of Punjab', 'temprature of punjab', 'temprature of Punjab'],query):
                
                while(True):
                    if('Punjab' in query) or ('punjab' in query):
                        Weather=Annex.WeatherPunjab()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of maharashtra', 'weather report of Maharashtra', 'temprature of maharashtra', 'temprature of Maharashtra'],query):
                
                while(True):
                    if('Maharashtra' in query) or ('maharashtra' in query):
                        Weather=Annex.WeatherMaharashtra()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of indore', 'weather report of Indore', 'temprature of indore', 'temprature of Indore'],query):
                
                while(True):
                    if('Indore' in query) or ('indore' in query):
                        Weather=Annex.WeatherIndore()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of jammu', 'weather report of Jammu', 'temprature of jammu', 'temprature of Jammu'],query):
                
                while(True):
                    if('Jammu' in query) or ('jammu' in query):
                        Weather=Annex.WeatherJammu()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of kanpur', 'weather report of Kanpur', 'temprature of kanpur', 'temprature of Kanpur'],query):
                
                while(True):
                    if('Kanpur' in query) or ('kanpur' in query):
                        Weather=Annex.WeatherKanpur()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of chennai', 'weather report of Chennai', 'temprature of chennai', 'temprature of Chennai'],query):
                
                while(True):
                    if('Chennai' in query) or ('chennai' in query):
                        Weather=Annex.WeatherChennai()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of uttrakhand', 'weather report of Uttrakhand', 'temprature of uttrakhand', 'temprature of Uttrakhand'],query):
                
                while(True):
                    if('Uttrakhand' in query) or ('uttrakhand' in query):
                        Weather=Annex.WeatherUttrakhand()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of lucknow', 'weather report of Lucknow', 'temprature of lucknow', 'temprature of Lucknow'],query):
                
                while(True):
                    if('Lucknow' in query) or ('lucknow' in query):
                        Weather=Annex.WeatherLucknow()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of patna', 'weather report of Patna', 'temprature of patna', 'temprature of Patna'],query):
                
                while(True):
                    if('Patna' in query) or ('patna' in query):
                        Weather=Annex.WeatherPatna()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of hyderabad', 'weather report of Hyderabad', 'temprature of hyderabad', 'temprature of Hyderabad'],query):
                
                while(True):
                    if('Hyderabad' in query) or ('hyderabad' in query):
                        Weather=Annex.WeatherHyderabad()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of bengaluru', 'weather report Bengaluru', 'temprature of bengaluru', 'temprature of Bengaluru'],query):
                
                while(True):
                    if('Bengaluru' in query) or ('bengaluru' in query):
                        Weather=Annex.WeatherBengaluru()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of ahmedabad', 'weather report of Ahmedabad', 'temprature of ahmedabad', 'temprature of Ahmedabad'],query):
                
                while(True):
                    if('Ahmedabad' in query) or ('ahmedabad' in query):
                        Weather=Annex.WeatherAhmedabad()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of jaipur', 'weather report Jaipur', 'temprature of jaipur', 'temprature of Jaipur'],query):
                
                while(True):
                    if('Jaipur' in query) or ('jaipur' in query):
                        Weather=Annex.WeatherJaipur()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of shillong', 'weather report of Shillong', 'temprature of shillong', 'temprature of Shillong'],query):
                
                while(True):
                    if('Shillong' in query) or ('shillong' in query):
                        Weather=Annex.WeatherShilong()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of imphal', 'weather report of Imphal', 'temprature of imphal', 'temprature of Imphal'],query):
                
                while(True):
                    if('Imphal' in query) or ('imphal' in query):
                        Weather=Annex.WeatherImphal()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of bhubaneswar', 'weather report of Bhubaneswar', 'temprature of bhubaneswar', 'temprature of Bhubaneswar'],query):
                
                while(True):
                    if('Bhubaneswar' in query) or ('bhubaneswar' in query):
                        Weather=Annex.WeatherBhubaneswar()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of srinagar', 'weather report of Srinagar', 'temprature of srinagar', 'temprature of Srinagar'],query):
                
                while(True):
                    if('Srinagar' in query) or ('srinagar' in query):
                        Weather=Annex.WeatherSrinagar()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of nagpur', 'weather report of Nagpur', 'temprature of nagpur', 'temprature of Nagpur'],query):
                
                while(True):
                    if('Nagpur' in query) or ('nagpur' in query):
                        Weather=Annex.WeatherNagpur()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of surat', 'weather report of Surat', 'temprature of surat', 'temprature of Surat'],query):
                
                while(True):
                    if('Surat' in query) or ('surat' in query):
                        Weather=Annex.WeatherSurat()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of visakhapatnam', 'weather report of Visakhapatnam', 'temprature of visakhapatnam', 'temprature of Visakhapatnam'],query):
                
                while(True):
                    if('Visakhapatnam' in query) or ('visakhapatnam' in query):
                        Weather=Annex.WeatherVisakhapatnam()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of madurai', 'weather report of Madurai', 'temprature of madurai', 'temprature of Madurai'],query):
                
                while(True):
                    if('Madurai' in query) or ('madurai' in query):
                        Weather=Annex.WeatherMadurai()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of jodhpur', 'weather report of Jodhpur', 'temprature of jodhpur', 'temprature of Jodhpur'],query):
                
                while(True):
                    if('Jodhpur' in query) or ('jodhpur' in query):
                        Weather=Annex.WeatherJodhpur()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of nashik', 'weather report of Nashik', 'temprature of nashik', 'temprature of Nashik'],query):
                
                while(True):
                    if('Nashik' in query) or ('nashik' in query):
                        Weather=Annex.WeatherNashik()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of )adodara', 'weather report of Vadodara', 'temprature of Vadodara', 'temprature of vadodara'],query):
                
                while(True):
                    if('Vadodara' in query) or ('Vadodara' in query):
                        Weather=Annex.WeatherVadodara()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of varanasi', 'weather report of Varanasi', 'temprature of varanasi', 'temprature of Varanasi'],query):
                
                while(True):
                    if('Varanasi' in query) or ('varanasi' in query):
                        Weather=Annex.WeatherVaranasi()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of amritsar', 'weather report of Amritsar', 'temprature of amritsar', 'temprature of Amritsar'],query):
                
                while(True):
                    if('Amritsar' in query) or ('amritsar' in query):
                        Weather=Annex.WeatherAmritsar()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of agra', 'weather report of Agra', 'temprature of agra', 'temprature of Agra'],query):
                
                while(True):
                    if('Agra' in query) or ('agra' in query):
                        Weather=Annex.WeatherAgra()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of ranchi', 'weather report of Ranchi', 'temprature of ranchi', 'temprature of Ranchi'],query):
                
                while(True):
                    if('Ranchi' in query) or ('ranchi' in query):
                        Weather=Annex.WeatherRanchi()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of rajkot', 'weather report of Rajkot', 'temprature of rajkot', 'temprature of Rajkot'],query):
                
                while(True):
                    if('Rajkot' in query) or ('rajkot' in query):
                        Weather=Annex.WeatherRajkot()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of faridabad', 'weather report of Faridabad', 'temprature of faridabad', 'temprature of Faridabad'],query):
                
                while(True):
                    if('Faridabad' in query) or ('faridabad' in query):
                        Weather=Annex.WeatherFaridabad()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of jamshedpur', 'weather report of Jamshedpur', 'temprature of jamshedpur', 'temprature of Jamshedpur'],query):
                
                while(True):
                    if('Jamshedpur' in query) or ('jamshedpur' in query):
                        Weather=Annex.WeatherJamshedpur()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of ludhiana', 'weather report of Ludhiana', 'temprature of ludhiana', 'temprature of Ludhiana'],query):
                
                while(True):
                    if('Ludhiana' in query) or ('ludhiana' in query):
                        Weather=Annex.WeatherLudhiana()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of raipur', 'weather report of Raipur', 'temprature of raipur', 'temprature of Raipur'],query):
                
                while(True):
                    if('Raipur' in query) or ('raipur' in query):
                        Weather=Annex.WeatherRaipur()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of meerut', 'weather report of Meerut', 'temprature of meerut', 'temprature of Meerut'],query):
                
                while(True):
                    if('Meerut' in query) or ('meerut' in query):
                        Weather=Annex.WeatherMeerut()
                        Weather.show(scrollable_text)
                        print(Weather)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of aurangabad', 'weather report of Aurangabad', 'temprature of aurangabad', 'temprature of Aurangabad'],query):
                
                while(True):
                    if('Aurangabad' in query) or ('aurangabad' in query):
                        Weather=Annex.WeatherAurangabad()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of jabalpur', 'weather report of Jabalpur', 'temprature of jabalpur', 'temprature of Jabalpur'],query):
                
                while(True):
                    if('Jabalpur' in query) or ('jabalpur' in query):
                        Weather=Annex.WeatherJabalpur()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of gwalior', 'weather report of Gwalior', 'temprature of gwalior', 'temprature of Gwalior'],query):
                
                while(True):
                    if('Gwalior' in query) or ('gwalior' in query):
                        Weather=Annex.WeatherGwalior()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of bhopal', 'weather report of Bhopal', 'temprature of bhopal', 'temprature of Bhopal'],query):
                
                while(True):
                    if('Bhopal' in query) or ('bhopal' in query):
                        Weather=Annex.WeatherBhopal()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of coimbatore', 'weather report of Coimbatore', 'temprature of coimbatore', 'temprature of Coimbatore'],query):
                
                while(True):
                    if('Coimbatore' in query) or ('coimbatore' in query):
                        Weather=Annex.WeatherCoimbatore()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of ghaziabad', 'weather report of Ghaziabad', 'temprature of ghaziabad', 'temprature of Ghaziabad'],query):
                
                while(True):
                    if('Ghaziabad' in query) or ('ghaziabad' in query):
                        Weather=Annex.WeatherGhaziabad()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of guwahati', 'weather report of Guwahati', 'temprature of guwahati', 'temprature of Guwahati'],query):
                
                while(True):
                    if('Guwahati' in query) or ('guwahati' in query):
                        Weather=Annex.WeatherGuwahati()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of kochi', 'weather report of Kochi', 'temprature of kochi', 'temprature of Kochi'],query):
                
                while(True):
                    if('Kochi' in query) or ('kochi' in query):
                        Weather=Annex.WeatherKochi()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("Please give a valid city name")

            elif there_exists(['weather report of udaipur', 'weather report of Udaipur', 'temprature of udaipur', 'temprature of Udaipur'],query):
                
                while(True):
                    if('Udaipur' in query) or ('udaipur' in query):
                        Weather=Annex.WeatherUdaipur()
                        Weather.show(scrollable_text)
                        break
                    else:
                        SR.speak("I am sorry, my API can not inform about the place you mentioned")

            #shutting down system
            elif there_exists(['exit','quit', 'die', 'kill'],query):
                SR.speak("shutting down all systems")
                sys.exit()
                break

            elif there_exists(['none'],query):
                pass
            elif there_exists(['stop the flow','stop the execution','halt','halt the process','stop the process','stop listening','stop the listening'],query):
                SR.speak("Listening halted.")
            
            #it will give online results for the query
            elif there_exists(['search something for me','to do a little search','search mode','i want to search something'],query):
                SR.speak('What you want me to search for?')
                query=SR.takeCommand()
                SR.speak(f"Showing results for {query}")
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, but there is a little problem while fetching the result.")

            #what is the capital
            elif there_exists(['what is the capital of','capital of','capital city of'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, but there is a little problem while fetching the result.")

            elif there_exists(['temperature'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Internet Connection Error")
            elif there_exists(['+','-','*','x','/','plus','add','minus','subtract','divide','multiply','divided','multiplied'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Internet Connection Error")

            elif there_exists(['What is the time in UTC', 'Universal time', 'universal time','tell me utc', 'tell me universal time', 'tell me the universal time'],query):
                universaltime=Annex.UTCTimezone()
                universaltime.show(scrollable_text)
                SR.speak(universaltime)

            elif there_exists(['open login details', 'open login form', 'open login portal'],query):
                SR.speak("opening portal")
                login_portal="http://127.0.0.1:5000/"
                webbrowser.get().open(login_portal)

            elif there_exists(['shutdown', 'shutdown device', 'shutdown pc', 'shutdown systems'],query):
                SR.speak('Initiating shutdown')
                time.sleep(3)
                SR.speak('Shutting down, bye')
                subprocess.call(["shutdown", "/s", "/t", "0"])
            
            elif there_exists(['restart', 'restart device', 'restart pc', 'restart systems'],query):
                SR.speak('Initiating restart')
                time.sleep(3)
                SR.speak('restarting, see you soon')
                subprocess.call(["shutdown", "/r", "/t", "0"])

            elif there_exists(['mood detection', 'emotion', 'how is my mood', 'how are my emotions'],query):
                SR.speak('Starting detection')
                subprocess.Popen(["python", "main.py"])

            else:
                SR.speak("Sorry it did not match with any commands that i'm registered with. Please say it again.")
    except Exception as e:
        pass

def gen(n):
    for i in range(n):
        yield i

class MainframeThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        mainframe()

def Launching_thread():
    Thread_ID=gen(1000)
    global MainframeThread_object
    MainframeThread_object=MainframeThread(Thread_ID.__next__(),"Mainframe")
    MainframeThread_object.start()

if __name__=="__main__":
        #tkinter code
        root=themed_tk.ThemedTk()
        root.set_theme("winnative")
        root.geometry("{}x{}+{}+{}".format(745,360,int(root.winfo_screenwidth()/2 - 745/2),int(root.winfo_screenheight()/2 - 360/2)))
        root.resizable(0,0)
        root.iconbitmap('Ishan-Image.ico')
        root.title("Sunday - All Systems Power Established and Working")
        root.configure(bg='#2c4557')
        scrollable_text=scrolledtext.ScrolledText(root,state='disabled',height=15,width=87,relief='sunken',bd=5,wrap=tk.WORD,bg='#95e657',fg='#800000')
        scrollable_text.place(x=10,y=10)
        mic_img=Image.open("Mic.png")
        mic_img=mic_img.resize((55,55),Image.LANCZOS)
        mic_img=ImageTk.PhotoImage(mic_img)
        Speak_label=tk.Label(root,text="Start- ",fg="#95e657",font='"Times New Roman" 17 ',borderwidth=0,bg='#2c4557')
        Speak_label.place(x=270,y=295)
        """Setting up objects"""
        SR=Annex.SpeakRecog(scrollable_text)    #Speak and Recognition class instance
        Listen_Button=tk.Button(root,image=mic_img,borderwidth=0,activebackground='#2c4557',bg='#2c4557',command=Launching_thread)
        Listen_Button.place(x=330,y=280)
        myMenu=tk.Menu(root)
        m1=tk.Menu(myMenu,tearoff=0) #tearoff=0 means the submenu can't be teared of from the window
        m1.add_command(label='Commands List',command=CommandsList)
        myMenu.add_cascade(label="Help",menu=m1)
        stng_win=Annex.SettingWindow()
        myMenu.add_cascade(label="Settings",command=partial(stng_win.settingWindow,root))
        myMenu.add_cascade(label="Clear Screen",command=clearScreen)
        root.config(menu=myMenu)
        root.mainloop()
