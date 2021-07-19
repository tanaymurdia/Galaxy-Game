# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 13:33:08 2021

@author: tanay
"""
def transform_perspective(self,x,y):
        lin_y=(y/self.height)*self.perspective_point_y
        if lin_y>self.perspective_point_y:
            lin_y=self.perspective_point_y
        diffx=x-self.perspective_point_x
        diffy=self.perspective_point_y-lin_y
        
        factory=diffy/self.perspective_point_y
        factory=pow(factory,4)

        tx=self.perspective_point_x+(factory*diffx)
        ty=self.perspective_point_y-(factory*self.perspective_point_y)
        return (int(tx),int(ty))