import pyshortcuts
import os


path = os.getcwd()
path = os.path.join(path,'run_app.py')
print(path)
pyshortcuts.make_shortcut(path,name='VOICE-CONTROL')
