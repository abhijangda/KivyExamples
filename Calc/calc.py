from kivy.uix.boxlayout import *
from kivy.uix.textinput import *
from kivy.app import App
from kivy.properties import *

class calcApp(App):

    def __init__(self):
        
        App.__init__(self)
        
    def build(self):
        
        main_window = MainWindow()
        return main_window

class MainWindow(BoxLayout):
    
    textInput = ObjectProperty()
    button_plus = ObjectProperty()
    button_minus = ObjectProperty()
    button_multiply = ObjectProperty()
    button_divide = ObjectProperty()
    button_equal_to = ObjectProperty()
    button_decimal = ObjectProperty()
    
    def __init__(self,**kwargs):
            
        super(MainWindow,self).__init__()
        self.num1 = None
        self.operation = None
        self.num2 = None        
        
    def on_button_press(self, *args):

        self.textInput.text += args[0]

    def divide(self, *args):

        try:
            if self.num1 != None:
                self.equal()
                
            self.num1 = float(self.textInput.text)
            self.operation = '/'
            self.textInput.text = ""
        except ValueError:
            pass
        
    def minus(self, *args):

        try:
            if self.num1 != None:
                self.equal()

            self.num1 = float(self.textInput.text)
            self.operation = '-'
            self.textInput.text = ""
        except ValueError:
            pass

    def multiply(self, *args):

        try:            
            if self.num1 != None:
                self.equal()

            self.num1 = float(self.textInput.text)
            self.operation = '*'
            self.textInput.text = ""
        except ValueError:
            pass
        
    def decimal(self, *args):

        if self.textInput.text.find('.')!=-1:
            self.textInput.text += '.'

    def plus(self, *args):

        try:
            if self.num1 != None:
                self.equal()

            self.num1 = float(self.textInput.text)
            self.operation = '+'
            self.textInput.text = ""
        except ValueError:
            pass

    def equal(self, *args):

        try:            
            self.num2 = float(self.textInput.text)
            if self.operation == '+':
                self.textInput.text = str(self.num2+self.num1)
                self.num1 = None
            elif self.operation == '*':
                self.textInput.text = str(self.num2*self.num1)
                self.num1 = None
            elif self.operation == '-':
                self.textInput.text = str(self.num2-self.num1)
                self.num1 = None
            elif self.operation == '/':
                self.textInput.text = str(self.num2/self.num1)
                self.num1 = None
        except ValueError:
            pass
    
if __name__ == '__main__':    
        
    calcApp().run()
