import kivy
import time,math
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import *
from kivy.app import App

class ClockApp(App):

    def __init__(self):
        
        App.__init__(self)
        
    def build(self):
        main_window = MainWindow()
        return main_window
    
class MainWindow (FloatLayout):

    def __init__(self, **kwargs):

        super(MainWindow, self).__init__(**kwargs)

        Clock.schedule_interval(self.update_clock,0)
        self.bind(pos = self.update_rect)
        self.bind(size = self.update_rect)
        self.sec_line = None
        self.min_line = None
        self.hr_line = None
        self.update_rect()
                    
    def update_rect (self, *args):

        radius = self.height/2
        if self.width <= self.height:
            radius = self.width/2
        self.sec_radius = radius - 10
        self.min_radius = radius - 30
        self.hr_radius = radius - 50
        self.center_x = self.width/2
        self.center_y = self.height/2
        
    def update_clock (self, *args):

        self.canvas.clear()
        str_time = time.strftime("%H:%M:%S")
        sec_angle = math.radians(int(time.strftime("%S"))*6)
        min_angle = math.radians(int(time.strftime("%M"))*6)
        hr = int(time.strftime("%H"))        
        if hr > 12:
            hr = hr - 12
        
        hr_angle = math.radians(int(hr)*30)        
                
        with self.canvas:
            
            for i in range (0,60):
                i_radians = math.radians(i*6)
                if i%5 == 0:
                    Color(1,0,0)
                    Line(circle=(self.center_x + self.sec_radius*math.sin(i_radians),
                                 self.center_y + self.sec_radius*math.cos(i_radians),
                                 2,0,359),width = 2)
                else:
                    Color(0,1,0)
                    Line(circle=(self.center_x + self.sec_radius*math.sin(i_radians),
                                 self.center_y + self.sec_radius*math.cos(i_radians),
                                 1,0,359),width = 1.5)
            Color(0.7,0.5,0.4)
            self.sec_line = Line(points=[self.center_x,self.center_y,
                                         self.center_x + self.sec_radius*math.sin(sec_angle),
                                         self.center_y+ self.sec_radius*math.cos(sec_angle)],
                                 width = 1)
            self.min_line = Line(points=[self.center_x,self.center_y,
                                         self.center_x + self.min_radius*math.sin(min_angle),
                                         self.center_y+ self.min_radius*math.cos(min_angle)],
                                 width = 2)
            self.hr_line = Line(points=[self.center_x,self.center_y,
                                        self.center_x + self.hr_radius*math.sin(hr_angle),
                                        self.center_y+ self.hr_radius*math.cos(hr_angle)],
                                width = 3)        

if __name__ == '__main__':
    ClockApp().run()
