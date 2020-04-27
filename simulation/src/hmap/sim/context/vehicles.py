#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmap.interface.context.traits.orientation import X, Y, XVel, YVel




class OmniDirectionalVehicle(X, Y, XVel, YVel):
    def __init__(self, x=0.0, y=0.0, x_vel=0.0, y_vel=0.0):
        self.__x, self.__y = (x, y)
        self.__x_vel, self.__y_vel = (x_vel, y_vel)
    @property
    def x(self):
        return self.__x
    def set_x(self, x):
        self.__x = x
    @property
    def y(self):
        return self.__y
    def set_y(self, y):
        self.__y = y
    @property
    def x_vel(self):
        return self.__x_vel
    def set_x_vel(self, xv):
        self.__x_vel = xv
    @property
    def y_vel(self):
        return self.__y_vel
    def set_y_vel(self, yv):
        self.__y_vel = yv
