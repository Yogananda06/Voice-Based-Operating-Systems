import os
import shutil as sh
import webbrowser
import time
from gtts import gTTS  
import playsound
import speech_recognition as fn_sr

def fn_talk(k):
    input=fn_sr.Recognizer()
    with fn_sr.Microphone() as source:

        if(k==""): d=1
        else: d=k
        input.adjust_for_ambient_noise(source,duration=d)

        audio=input.listen(source)
        data=""
        try:
            data=input.recognize_google(audio)
            print("Response is: " + data)

        except fn_sr.UnknownValueError:
            respond("Sorry I did not hear you, Please repeat again.")
            return fn_talk("").lower()
    return data

def fn_respond(output):
    num=0
    print(output)
    num += 1
    response=gTTS(text=output, lang='en')
    file = str(num)+".mp3"
    response.save(file)
    playsound.playsound(file, True)
    os.remove(file)

def create_folder(fname,path):
    path = os.path.join(path,fname)
    if os.path.exists(path):
        return 0
    os.mkdir(path)
    return 1

def delete_folder(fname,path):
    path = os.path.join(path,fname)
    if os.path.exists(path):
        sh.rmtree(path)
        return 1
    else:
        return 0

def create_file(fname,typ,path):
    fname=fname
    count = 1
    join_part= '_'+str(count)+'.'+typ
    path += '/'+fname +'.'+typ
    while 1:
        if not os.path.exists(path):
            open(path,'w')
            return 1
        else :
            path=os.path.join(os.getcwd(),fname+join_part)
            join_part= '_'+str(count)+'.'+typ
            count+=1


def delete_file(fname,path):
    path = os.path.join(path, fname)
    if os.path.exists(path):
        os.remove(path)
    else :
        return 0
    return 1

def rename_dir_file(src,dst):
    if os.path.exists(src):
        if not os.path.exists(dst):
            os.rename(src,dst)
        else:
            return 0
    else:
        return -1
    return 1

def open_application(a):
    count =0
    prev_path = os.getcwd()
    apps_path = '/usr/share/applications'
    os.chdir(apps_path)
    apps = os.listdir()
    if a+".desktop" in apps:
        os.system(a)
        os.chdir(prev_path)
        return 1
    else:
        for app in apps :
            if a in app:
                k = app
                count+=1
    if "office" in a:
            a = a[7:]
            os.system("libreoffice --"+a)
            os.chdir(prev_path)
            return 1
    if not os.system("gnome-"+a) :
        os.chdir(prev_path)
        return 1
    if "gnome-"+a+".desktop" in apps:
        os.system("gnome-"+a)
        os.chdir(prev_path)
        return 1
    else:
        if count==1:
            os.system(k)
            os.chdir(prev_path)
            return 1
        else :
            os.chdir(prev_path)
            return 0

def open_folder(path):
    if os.path.exists(path):
        os.system("nautilus "+path)
        return 1
    else:
        return 0

def open_file(path):
    if not os.path.exists(path):
        return 0
    name, extension = os.path.splitext(path)
    command = ''
    if extension in ['.txt','.cpp','.c','.py']:
        command = 'gedit'
    elif extension in ['.odt','.docx']:
        command = 'libreoffice --writer'
    elif extension=='.xlsx':
        command = 'libreoffice --calc'
    elif extension=='.odg':
        command = 'libreoffice --draw'
    else:
        return 0

    command = command + ' ' + path
    os.system(command)
    return 1



def run_file(path):
    name, extension = os.path.splitext(path)
    command = ""
    if extension==".cpp":
        command = "g++"
    elif extension==".c":
        command = "gcc"
    elif extension==".py":
        command = "python"
    else:
        return 0

    command = command + " " + path
    if extension==".c" or extension==".cpp":
        command = command + "\n ./a.out"
    os.system("gnome-terminal -e 'bash -c \""+command+";bash\"'")
    return 1

def fill_file(path):
    if os.path.exists(path):
        with open(path,'w') as writer:
            fn_respond('Tell the content')
            content = fn_talk(5)
            writer.write(content)
            return 1
    else:
        return 0

def change_dir(path,folder_name):
    path = os.path.join(path,folder_name)
    if os.path.exists(path):
        os.chdir(path)
        return 1
    return 0

def go_back(path):
    path = os.path.dirname(os.getcwd())
    if os.path.exists(path):
        os.chdir(path)
        return 1
    return 0

def web_search(query):
    query_set=['gmail','youtube','drive','twitter','facebook','instagram']
    if query=="" or query==" ":
        webbrowser.open("https://google.com")
        return 1
    elif query in query_set:
        webbrowser.open("https://www."+query+".com/")
    else:
        if (webbrowser.open("https://google.com/search?q="+query)):
            return 1
        else :
            return 0

def shutdown(t,message):
    command = "shutdown +"+str(t)+" \""+message+"\""
    os.system("gnome-terminal -e 'bash -c \""+command+";bash\"'")
    return 1

def restart():
    command = "sudo reboot"
    os.system("gnome-terminal -e 'bash -c \""+command+";bash\"'")

def stop_all():
    time.sleep(3)
    os.system("kill -1 -1")
