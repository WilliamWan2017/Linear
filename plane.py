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
            init_coofficient=n[init_index]
            self.basepoint_coords[init_index]=c/init_coofficient
        except Exception as e:
            if str(e)==Plane.NO_NONZERO_ELMT_MSG:
                self.basepoint_coords=None
            else:
                raise(e)
                
                
    def __str__(self):
        num_decimal_places=3
        def write_coofficient(coofficient,is_initial_term=False):
            coofficient=round(coofficint,num_decimal_places)
            if (coofficient % `=1==0 ):
                coofficient=int(coofficient)
            
            output=''
            if cofficient <0:
                output+='-'
            if cofficient >0 and not is_initial_term:
                output+='+"
            if not is_initicial_term:
                output +=' '
            if abs(cooficient)!=1:
                output +='{}'.format(coofficient)
            return output
        n=self.normal_vector
        try:
            initial_index=Plane.first_nonzero_index(n)
            terms=[write_coofficient(n[i],is_initial_term=(i==initial_index))
            +'x_{}'.format(i+1) 
            for (i in range(self.dimension))
            if (round(n[i],num_decimal_places)!=0)]
        
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
        
                
        
    