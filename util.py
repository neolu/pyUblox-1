#!/usr/bin/env python
'''common utility functions'''

import math

radius_of_earth = 6378137.0 # in meters
speedOfLight    = 299792458.0 # in m/s
gpsPi           = 3.1415926535898  # Definition of Pi used in the GPS coordinate system

def gps_distance(lat1, lon1, lat2, lon2):
	'''return distance between two points in meters,
	coordinates are in degrees
	thanks to http://www.movable-type.co.uk/scripts/latlong.html'''
	from math import radians, cos, sin, sqrt, atan2
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	dLat = lat2 - lat1
	dLon = lon2 - lon1
	
	a = sin(0.5*dLat)**2 + sin(0.5*dLon)**2 * cos(lat1) * cos(lat2)
	c = 2.0 * atan2(sqrt(a), sqrt(1.0-a))
	return radius_of_earth * c


def gps_bearing(lat1, lon1, lat2, lon2):
	'''return bearing between two points in degrees, in range 0-360
	thanks to http://www.movable-type.co.uk/scripts/latlong.html'''
	from math import sin, cos, atan2, radians, degrees
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	dLat = lat2 - lat1
	dLon = lon2 - lon1    
	y = sin(dLon) * cos(lat2)
	x = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dLon)
	bearing = degrees(atan2(y, x))
	if bearing < 0:
		bearing += 360.0
	return bearing

class PosLLH:
    '''a class for latitude/longitude/altitude'''
    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def __str__(self):
        return '(%f, %f, %f)' % (self.lat, self.lon, self.alt)

class PosVector:
    '''a X/Y/Z vector class, used for ECEF positions'''
    def __init__(self, X,Y,Z):
        self.X = X
        self.Y = Y
        self.Z = Z

    def __add__(self, v):
        return PosVector(self.X + v.X,
                         self.Y + v.Y,
                         self.Z + v.Z)

    def __mul__(self, v):
        return PosVector(self.X * v,
                         self.Y * v,
                         self.Z * v)

    def __div__(self, v):
        return PosVector(self.X / v,
                         self.Y / v,
                         self.Z / v)

    def distance(self, pos2):
        import math
        return math.sqrt((self.X-pos2.X)**2 + 
                         (self.Y-pos2.Y)**2 + 
                         (self.Z-pos2.Z)**2)

    def ToLLH(self):
        '''convert from ECEF to lat/lon/alt

        Thanks to Nicolas Hennion
        http://www.nicolargo.com/dev/xyz2lla/
        '''
        from math import sqrt, pow, cos, sin, pi, atan2

        a = radius_of_earth
        e = 8.1819190842622e-2

        b = sqrt(pow(a,2) * (1-pow(e,2)))
        ep = sqrt((pow(a,2)-pow(b,2))/pow(b,2))
        p = sqrt(pow(self.X,2)+pow(self.Y,2))
        th = atan2(a*self.Z, b*p)
        lon = atan2(self.Y, self.X)
        lat = atan2((self.Z+ep*ep*b*pow(sin(th),3)), (p-e*e*a*pow(cos(th),3)))
        n = a/sqrt(1-e*e*pow(sin(lat),2))
        alt = p/cos(lat)-n
        lat = (lat*180)/pi
        lon = (lon*180)/pi
        return PosLLH(lat, lon, alt)


def correctWeeklyTime(time):
    '''correct the time accounting for beginning or end of week crossover'''
    half_week       = 302400 # seconds
    corrTime        = time
    if time > half_week:
        corrTime    = time - 2*half_week
    elif time < -half_week:
        corrTime    = time + 2*half_week
    return corrTime

