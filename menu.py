# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 13:50:12 2021

@author: tanay
"""
from kivy import platform
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty,BooleanProperty, Clock,NumericProperty
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse, Quad, Triangle
from kivy.graphics.context_instructions import Color
from kivy.metrics import dp
from kivy.core.window import Window
import random
from kivy.uix.relativelayout import RelativeLayout

class MenuWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity ==0:
            return False
        return super(RelativeLayout,self).on_touch_down(touch)