#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:22:56 2017

@author: zqzhan
"""

from decimal import Decimal,getcontext
from vector import vector
class Line(object):
    NO_NONZERO_ELMT_FOUND_MSG="No Nonzero elements was found "
    def __init__(self,normal_vector=None,constant_term=None):
        self.Dimension=2;
        if not normal_vector:
            allzero=[0]*self.Dimension
            normal_vector=Vector(allzero)
        self.normal_vector=normal_vector
        if not constant_term:
            constant_term=Decimal(0)
        self.constant_term=Decimal(constant_term)
        self.set_basepoint()
        
    def set_basepoint(self):
        try:
            n=self.normal_vector
            c=self.constant_term
            basepoint_coords=[0]*self.dimension
            initial_index=Line.first_nonzero_index(n)
            initial_coefficient=n[initial_index]
            basepoint_coords[initial_index]=c/initial_coefficient
            self.basepoint=basepoint_coords
        
        except Exception as e:
            if str(e)==Line.NO_NONZERO_ELMT_FOUND_MSG:
                self.basepoint=None
            
            else:
                raise(e)
            

    def __str__(self):
        num_decimal_places=3
        def write_coefficient(coefficient,is_initial_term=False):
            coefficient=round(coefficient,num_decimal_places)
            if coefficient % 1 ==0:
                coefficient=int(coefficient)
            output=' '
            if (coefficient <0):
                output+='-'
            if (coefficient >0) and (not is_initial_term):
                output += '+'
            
            if (not is_initial_term):
                output += ' '
            if (abs(coefficient)!=1):
                output += '{}'.format(abs(coefficient))
            return output
        
            
        
    
        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i],
                                       is_initial_term=(i == initial_index)) +
                     'x_{}'.format(i + 1)
                     for i in range(self.dimension)
                     if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output