import sip,sys,os,pty,time
from kivy.uix.floatlayout import *
from kivy.uix.textinput import *
from kivy.clock import *
from kivy.app import App
from kivy.uix.textinput import TextInput
import select,fcntl,termios
from kivy.properties import *

class shellApp(App):

    def __init__(self,return_val,fd):
        
        App.__init__(self)
        self.return_val = return_val
        self.fd = fd
        
    def build(self):
        main_window = MainWindow(self.return_val,self.fd)
        return main_window

class ShellTextInput(TextInput):

    def __init__(self, **kwargs):

        super(ShellTextInput, self).__init__(**kwargs)
        
    def insert_text(self,substring,from_undo=False):
        
        if substring == "\n":
            row = self.cursor[0]-1
            full_text = self.text
            last_row_index = full_text.rfind("\n")
            if last_row_index == -1:
                last_row_index = 0
                
            last_line_text = full_text[last_row_index:]
            text_to_write = last_line_text[last_line_text.find("]$")+2:].strip()
            os.write(self.win_parent.fd,text_to_write+'\n')
        TextInput.insert_text(self,substring,from_undo)
        
class MainWindow(FloatLayout):

    textInput = ObjectProperty()
    
    def __init__(self,return_val,fd,**kwargs):
            
        super(MainWindow,self).__init__()

        self.fd = fd
        self.textInput.win_parent = self        
        Clock.schedule_interval(self.readOutput,0)
        
    def readOutput(self,dt):
        
        r,w,e = select.select([self.fd],[],[],0)
        s=''
        d='1'
        try:                
            while d != '' and r!=[]:                
                d = os.read(r[0],1)
                s+=d
        except OSError:
            pass        

        if s!="":
            s = unicode(s,'utf-8',errors='replace')
            self.textInput.text += s           
            self.textInput.min_pos = self.textInput.cursor            

if __name__ == '__main__':
    
    return_val = pty.fork()      

    if return_val[0] == 0:           
        os.execv("/usr/bin/bash",["/usr/bin/bash"])
    
    state = 0
    fd = return_val[1]
    tc_attr = termios.tcgetattr(fd)
    tc_attr[3] = tc_attr[3] & ~termios.ECHO
    termios.tcsetattr(fd,termios.TCSANOW,tc_attr)
    fl = fcntl.fcntl(fd,fcntl.F_GETFL)
    fcntl.fcntl(fd,fcntl.F_SETFL,fl|os.O_NONBLOCK)
    
    shellApp(return_val,fd).run()
