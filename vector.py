# -*- coding: utf-8 -*-
"""
Spyder Editor


This is a temporary script file.
"""
from decimal import Decimal, getcontext
import math


class MyDecimal(Decimal):
    def is_near_zero(self,eps=1e-10):
        if (abs(self)<eps):
            return True
        else:
            return False

getcontext().prec = 30 

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates=tuple(coordinates)
            self.dimension=len(coordinates)
        except ValueError:
            raise ValueError("The coordinates must be nonempty")
        except TypeError:
            raise TypeError("the coordinates must be an iterable.")
            
            
    def __str__(self):
        return "Vector:{}".format(self.coordinates)
    
    def __eq__(self,v):
        return self.coordinates==v.coordinates
    
    def is_zero(self):
        return set(self.coordinates)==set([Decimal(0)])
        
    def __getitem__(self, i):
        return self.coordinates[i]
    
    def plus(self,v):
        new_coordinates=[x+y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates)
    
    def minus(self,v):
        new_coordinates=[x-y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates)
    
    
    def times_scalar(self,c):
        c_decimal=Decimal(c)
        new_coordinates=[c_decimal*Decimal(x) for x in self.coordinates]
        return Vector(new_coordinates)
        
    def magnitude(self):
        new_coordinates=[Decimal(x)**2 for x in self.coordinates]
        return math.sqrt(sum(new_coordinates))
    
    def normalized(self):
        try:
            magnitude=self.magnitude()
            return self.times_scalar(1.0/magnitude)
        except ZeroDivisionError:
            raise Exception('Cannot not normalized the zero vector')
    
    def dot_product(self, other):
        return sum(x * y for x, y in zip(self.coordinates, other.coordinates))
        
    def get_anger_radio(self ,other):
        self_normalized=self.normalized();
        other_normalized=other.normalized();
        return Decimal(round(self_normalized.dot_product(other_normalized),3))
    
    def get_anger_degree(self,other):
        degrees_per_radio=Decimal(180.0/math.pi)
        
        return self.get_anger_radio(other)*degrees_per_radio;
    
    def is_parallel_to(self,other):
        if (self.is_zero()) or (other.is_zero()):
            return True;
        if (self.get_anger_radio(other) in [0,math.pi]):
            return True;
        return False
    
    def is_orthogonal(self,other):
        return (round(self.dot_product(other),3)==0)
    
    def get_project_vector(self,other):
        other_normalized=other.normalized()
        return other_normalized.times_scalar(self.dot_product(other_normalized))
      
    def get_orthogonal_vector(self,other):
        return self.minus(self.get_project_vector(other))
    
    def cross_product(self,other):
        [x1,y1,z1]=self.coordinates
        [x2,y2,z2]=other.coordinates
        x=y1*z2-y2*z1
        y=-(x1*z2-x2*z1)
        z=x1*y2-x2*y1
        return Vector([x,y,z])
    
    def area_parallelogram(self,other):
        return self.cross_product(other).magnitude()
    
    def area_triangle(self,other):
        return self.area_parallelogram(other)/2
    
        
    
my_vector1=Vector([2,3])
my_vector2=Vector([8,5])
print((my_vector1))
print(my_vector1.magnitude())
print(my_vector1.dot_product(my_vector2))
print (my_vector1.get_anger_radio(my_vector2))
print (my_vector1.get_anger_degree(my_vector2))
print(my_vector1.is_parallel_to(my_vector2))
print(my_vector1.is_orthogonal(my_vector2))
print(my_vector1.get_project_vector(my_vector2))
print(my_vector1.get_orthogonal_vector(my_vector2))
my_vector1=Vector([2,3,4])
my_vector2=Vector([4,5,6])
print(my_vector1.cross_product(my_vector2))
print(my_vector1.area_parallelogram(my_vector2))
print(my_vector1.area_triangle(my_vector2))
