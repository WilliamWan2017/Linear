#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 14:15:03 2017

@author: zqzhan
"""
from decimal import Decimal,getcontext
from vector import Vector,MyDecimal
getcontext().prec=30

class Hyperplane(object): 
    NO_NONZERO_ELMT_FOUND_MSG="No Nonzero element was found"
    EITHER_DIMENSION_OR_NORMAL_VECTOR_MUST_BE_PROVIDED_MSG=" Either dimension or normal vector must be provided"
    
    def __init__(self,dimension,normal_vector,constant_term):
        if not dimension and not normal_vector:
            raise Exception(self.EITHER_DIMENSION_OR_NORMAL_VECTOR_MUST_BE_PROVIDED)
        if not normal_vector:
            self.dimension=dimension
            allZero=[0]* self.dimension
            normal_vector=Vector(allZero)
        else:
            self.dimension=normal_vector.dimension
        self.normal_vector=normal_vector
        if not constant_term:
            constant_term=Decimal(0)
        self.constant_term=Decimal(constant_term)
        self.set_basepoint()
        
    def set_basepoint(self):
        try:
            n=self.normal_vector
            c=self.constant_term
            basepoint_coordis=[0]*self.dimension
            initial_index=Hyperplane.first_nonzero_index(n)
            initial_coofficient=Decimal(n[initial_index])
            basepoint_coordis[initial_index]=c/initial_coofficient
            self.basepoint=Vector(basepoint_coordis)
        except Exception as e :
            if (e)==Hyperplane.NO_NONZERO_ELMT_FOUND_MSG:
                self.basepoint=None
            else:
                raise(e)
    
    def __str__(self):
        num_decimal_places=3
        def write_coofficient(coofficient,is_initial_term=False):
            coofficient=round(coofficient,num_decimal_places)
            if (coofficient % 1==0):
                coofficient=int(coofficient)
            output=''
            if (coofficient<0):
                output+='-'
            if (coofficient >0 and not is_initial_term):
                output+='+'
            
            if not is_initial_term:
                output +=' '
            
            if abs(coofficient)!=1:
                output +='{}'.format(abs(coofficient))
            
            return output
        n=self.normal_vector;
        try:
            initial_term=Hyperplace.first_nonzero_index(n)
            term=[write_coofficient(n[i],is_initial_term=i==initial_term)+'x_{}'.format(i+1) for i in range(self.dimension) if round(n[i],num_decimal_places)!=0]
            output=' '.join(term)
        except Exception as e:
            if str(e) == self.NO_NONZERO_ELMT_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output
    def is_parallel(self, plane2):
        return self.normal_vector.is_parallel_to(plane2.normal_vector)

    def __eq__(self, plane2):
        if self.normal_vector.is_zero():
            if not plane2.normal_vector.is_zero():
                return False

            diff = self.constant_term - plane2.constant_term
            return MyDecimal(diff).is_near_zero()

        elif plane2.normal_vector.is_zero():
            return False

        if not self.is_parallel(plane2):
            return False

        basepoint_difference = self.basepoint.minus(plane2.basepoint)
        return basepoint_difference.is_orthogonal(self.normal_vector)


    def __getitem__(self, i):
        return self.normal_vector[i]

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Hyperplane.NO_NONZERO_ELMT_FOUND_MSG)

            
            
            
    