#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 13:51:32 2017

@author: zqzhan
"""

from decimal import Decimal,getcontext
from vector import Vector,MyDecimal

getcontext().prec = 30
class Plane(object):
    
    NO_NONZERO_ELMT_FOUND_MSG="No nonzero element was found"
    def __init__(self,normal_vector=None,constant_term=None):
        self.dimension=3
        if not normal_vector:
            AllZero=[0]*self.dimension
            normal_vector=AllZero
        self.normal_vector=normal_vector
        
        if not constant_term:
            constant_term=Demical(0)
        self.constant_term=constant_term
        self.set_basepoint()
        
    def set_basepoint(self):
        try:
            
            n=self.normal_vector
            c=self.constant_term
            self.basepoint_coords=[0]*self.dimension
        
            init_index=Plane.first_nonzero_index(n)
            init_coofficient=n.coordinates[init_index]
            self.basepoint_coords[init_index]=c/init_coofficient
        except Exception as e:
            if str(e)==Plane.NO_NONZERO_ELMT_FOUND_MSG:
                self.basepoint_coords=None
            else:
                raise(e)
                
                
    def __str__(self):
        num_decimal_places=3
        def write_coofficient(coofficient,is_initicial_term=False):
            coofficient=round(coofficient,num_decimal_places)
            if (coofficient % 1==0 ):
                coofficient=int(coofficient)
            
            output=''
            if coofficient <0:
                output+='-'
            if coofficient >0 and not is_initicial_term:
                output+='+'
            if not is_initicial_term:
                output +=' '
            if abs(coofficient)!=1:
                output +='{}'.format(coofficient)
            return output
        n=self.normal_vector
        try:
            initial_index=Plane.first_nonzero_index(n)
            terms=[write_coofficient(n[i],is_initicial_term=(i==initial_index))+'x_{}'.format(i+1) for i in range(self.dimension) if round(n[i],num_decimal_places)!=0]
          
            output=' '.join(terms);
        except Exception as e:
            if (str(e)==Plane.NO_NONZERO_ELMT_FOUND_MSG):
                output='0'
            else:
                raise e
        constant=round(self.constant_term,num_decimal_places)
        if (constant %1 ==0):
            constant=int(constant)
        output +=' = {}'.format(constant)
        return output
    
        
            
            
                
                
                
                
    def first_nonzero_index(iterable):
        for k,item in enumerate(iterable):
            if MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_EMLT_FOUND_MSG)
        
                
        
    def is_parallel(self,Plane2):
        return self.normal_vector.is_parallel_to(Plane2.normal_vector)
    
    def __eq__(self,Plane2):
        if (self.normal_vector.is_zero()):
            if (not Plane2.normal_vector.is_zero()):
                return False
            else:
                return self.constant_term==Plane2.constant_term
        if (Plane2.normal_vector.is_zero()):
            return False
        if not self.normal_vector.is_parallel_to(Plane2.normal_vector):
            return False
        base_diff=self.basepoint_coords.minus(Plane2.basepooint_coords)
        return base_diff.is_orthogonal(self.normal_vector)
    
    @staticmethod
    def first_nonzero_index(Vector_iterable):
        iterable=Vector_iterable.coordinates
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)

if __name__ == '__main__':
    # first system of planes:
    # -0.412x + 3.806y + 0.728z = -3.46
    # 1.03x - 9.515y - 1.82z = 8.65

    plane1 = Plane(Vector([-0.412, 3.806, 0.728]), -3.46)
    plane2 = Plane(Vector([1.03, -9.515, -1.82]), 8.65)
    print(str(plane1))
    print ('1 is parallel: {}'.format(plane1.is_parallel(plane2)))
    print ('1 is equal: {}'.format(plane1 == plane2))

    # second system of planes:
    # 2.611x + 5.528y + 0.283z = 4.6
    # 7.715x + 8.306y + 5.342z = 3.76

    plane3 = Plane(Vector([2.611, 5.528, 0.283]), 4.6)
    plane4 = Plane(Vector([7.715, 8.306, 5.342]), 3.76)

    print ('2 is parallel: {}'.format(plane3.is_parallel(plane4)))
    print ('2 is equal: {}'.format(plane3 == plane4))

    # third system of planes:
    # -7.926x + 8.625y - 7.212z = -7.952
    # -2.642x + 2.875y - 2.404z = -2.443

    plane5 = Plane(Vector([-7.926, 8.625, -7.212]), -7.952)
    plane6 = Plane(Vector([-2.642, 2.875, -2.404]), -2.443)

    print ('3 is parallel: {}'.format(plane5.is_parallel(plane6)))
    print ('3 is equal: {}'.format(plane5 == plane6))
