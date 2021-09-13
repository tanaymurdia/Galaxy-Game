# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 14:23:41 2021

@author: - Tanay Murdia

comment for assignment
"""
from kivy.config import Config
Config.set('graphics','width','900')
Config.set('graphics','height','400')

from kivy import platform
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty,BooleanProperty, Clock,NumericProperty,ObjectProperty
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse, Quad, Triangle
from kivy.graphics.context_instructions import Color
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.core.window import Window
import random


Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from transforms import transform_perspective
    from useractions import keyboard_closed ,on_touch_down, on_touch_up, on_keyboard_down, on_keyboard_up
    
    menu_widget = ObjectProperty()
    perspective_point_x=NumericProperty(0)
    perspective_point_y=NumericProperty(0)
    V_NB_LINES=6
    V_LINE_SPACING=0.4
    vertical_lines=[]
    minx=float('inf')
    maxx=0
    
    SPEED=.1
    current_y_offset=0
    current_y_loop=0
    
    SPEEDX=3
    current_speed_x=0
    current_x_offset=0
    
    H_NB_LINES=15
    H_LINE_SPACING=0.1
    horizontal_lines=[]
    
    NB_TILES=10
    tiles = []
    tiles_coordinates =[]
    
    
    SHIP_WIDTH=.1
    SHIP_HEIGHT=0.035
    SHIP_BASE_Y =0.04
    ship=None
    ship_coordinates=[(0,0),(0,0),(0,0)]
    
    menu_title=StringProperty("G   A   L   A   X   Y")
    menu_button_title=StringProperty("START")
    
    state_game_over=False
    state_game_has_started=False
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.perspective_point_x=self.width/2
        self.perspective_point_y=self.height*(3/4)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.init_ship()
        
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed,self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        
        Clock.schedule_interval(self.update,1/60)
        
    def reset_game(self):

        self.current_y_loop=0
        self.current_y_offset=0
        
        self.current_x_offset=0
        self.current_speed_x=0
        
        self.tiles_coordinates =[]
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        
        self.state_game_over=False
        
    def is_desktop(self):
        print(platform)
        if platform in ('linux','win','macosx'):
            return True
        return False
        
    def init_ship(self):
        with self.canvas:
            Color(0,0,0)
            self.ship=Triangle()
            
    def update_ship(self):
        
        base=self.SHIP_BASE_Y*self.height
        shipwidth=self.SHIP_WIDTH*self.width/2
        shipheight=self.SHIP_HEIGHT*self.height
        
        x1=self.width/2-shipwidth+self.current_speed_x
        y1=base
        x2=self.width/2+self.current_speed_x
        y2=base+shipheight
        x3=self.width/2+shipwidth+self.current_speed_x
        y3=base
        
        self.ship_coordinates[0]=(x1,y1)
        self.ship_coordinates[1]=(x2,y2)
        self.ship_coordinates[2]=(x3,y3)
        
        
        tx1,ty1=self.transform_perspective(x1, y1)
        tx2,ty2=self.transform_perspective(x2, y2)
        tx3,ty3=self.transform_perspective(x3, y3)
        #print(tx1,ty1,tx2,ty2,tx3,ty3)
        self.ship.points=(tx1,ty1,tx2,ty2,tx3,ty3)

    def check_collison(self):
        for i in range(len(self.tiles_coordinates)):
            tx,ty=self.tiles_coordinates[i]
            if ty>self.current_y_loop+1:
                return False
            if self.check_collisonwith_tile(tx, ty)==True:
                return True
        return False
                
                
            

    def check_collisonwith_tile(self,tx,ty):
        xmin,ymin=self.get_tile_coordinates(tx, ty)
        xmax,ymax=self.get_tile_coordinates(tx+1, ty+1)
        for i in range(len(self.ship_coordinates)):
            x,y=self.ship_coordinates[i]
            if xmin<= x<=xmax and ymin<=y<=ymax:
                return True
        return False 

    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.V_NB_LINES):
                self.vertical_lines.append(Line())
                
    
    def get_line_x_from_index(self,index):
        central_line=self.perspective_point_x
        spacing=self.V_LINE_SPACING*self.width
        offset=index-0.5
        #print(central_line,spacing,offset)
        line_x=central_line+(offset*spacing) + self.current_x_offset
        return line_x
        
    
    def update_vertical_lines(self):
        index=-int(self.V_NB_LINES/2)
        for i in range(self.V_NB_LINES):
            index+=1
            line_x=self.get_line_x_from_index(index)
            x1,y1=self.transform_perspective(line_x,0)
            x2,y2=self.transform_perspective(line_x,self.height)
            line=self.vertical_lines[i]
            line.points=(x1,y1,x2,y2)
            
    def init_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.H_NB_LINES):
                self.horizontal_lines.append(Line())
                
    def get_line_y_from_index(self,index):
        spacing=self.H_LINE_SPACING*self.height
        #print(central_line,spacing,offset)
        line_y=index*spacing + self.current_y_offset
        return line_y
    
    
    def update_horizontal_lines(self):
        start_index=-int(self.V_NB_LINES/2)+1
        xmin=self.get_line_x_from_index(start_index)
        xmax=self.get_line_x_from_index(start_index+self.V_NB_LINES-1)
        #print(xmin,xmax)
        
        for i in range(self.H_NB_LINES):
            line_y=self.get_line_y_from_index(i)
            x1,y1=self.transform_perspective(xmin,line_y)
            x2,y2=self.transform_perspective(xmax,line_y)
            line=self.horizontal_lines[i]
            line.points=(x1,y1,x2,y2)
            #line.points=(0,line_y,self.width,line_y)
    
    def get_tile_coordinates(self,tx,ty):
        ty=ty-self.current_y_loop
        x=self.get_line_x_from_index(tx)
        y=self.get_line_y_from_index(ty)
        return x,y    
            
    def init_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.NB_TILES):
                self.tiles.append(Quad())
                
    def pre_fill_tiles_coordinates(self):
        for i in range(10):
            self.tiles_coordinates.append((0,i))
    
    def generate_tiles_coordinates(self):
        
        last_y=0
        last_x=0
        
        start_index=-int(self.V_NB_LINES/2)+1
        end_index=start_index+self.V_NB_LINES-1
        
        
        for i in range(len(self.tiles_coordinates)-1,-1,-1):
            tix,tiy=self.tiles_coordinates[i]
            if (self.current_y_loop-1>tiy):
                del self.tiles_coordinates[i]
                
        if len(self.tiles_coordinates)>0:
            last_y=self.tiles_coordinates[-1][1]+1
            last_x=self.tiles_coordinates[-1][0]
                
        for i in range(len(self.tiles_coordinates),self.NB_TILES):
            r =random.randint(0, 2)
            
            if(last_x<=start_index):
                r=1
            if(last_x>=end_index-1):
                r=2
            
            self.tiles_coordinates.append((last_x,last_y))
            if r==1:
                last_x+=1
                self.tiles_coordinates.append((last_x,last_y))
                last_y+=1
                self.tiles_coordinates.append((last_x,last_y))
                
            if r==2:
                last_x-=1
                self.tiles_coordinates.append((last_x,last_y))
                last_y+=1
                self.tiles_coordinates.append((last_x,last_y))
                
            
            last_y+=1

    
    def update_tiles(self):
        for i in range(self.NB_TILES):
            ti_x,ti_y=self.tiles_coordinates[i]
            xmin,ymin=self.get_tile_coordinates(ti_x, ti_y)
            xmax,ymax=self.get_tile_coordinates(ti_x+1, ti_y+1)
            x1,y1=self.transform_perspective(xmin, ymin)
            x2,y2=self.transform_perspective(xmin, ymax)
            x3,y3=self.transform_perspective(xmax, ymax)
            x4,y4=self.transform_perspective(xmax, ymin)
            self.tiles[i].points=(x1,y1,x2,y2,x3,y3,x4,y4)
        
        
        
    def update(self,dt):
        self.perspective_point_x=self.width/2
        self.perspective_point_y=self.height*(3/4)
        dist=self.H_LINE_SPACING*self.height
        timefactor=dt*60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()
        
        if not self.state_game_over and self.state_game_has_started:
            speed_y=self.SPEED *self.height/100

            if self.current_y_offset<=0:
                self.current_y_offset=dist
                self.current_y_loop+=1
                self.generate_tiles_coordinates()
            else:
            #self.current_y_offset-=((dist/60)+self.SPEED)
                self.current_y_offset-=(speed_y*timefactor)
            
            speed_x=self.current_speed_x*self.width/100
            self.current_x_offset+=(speed_x*timefactor)
        

        if not self.check_collison() and not self.state_game_over:
            self.menu_title="G  A  M  E    O  V  E  R"
            self.menu_button_title="RESTART"
            self.state_game_over=True
            self.menu_widget.opacity=1
            print('Game Over')
        
    def on_menu_button(self):
        print("Start")
        self.reset_game()
        self.state_game_has_started= True
        self.menu_widget.opacity=0
    
        

class GalaxyApp(App):
    pass

GalaxyApp().run()
    
