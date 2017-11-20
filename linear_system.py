#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 14:42:24 2017

@author: zqzhan
"""

from copy import deepcopy
from decimal import Decimal,getcontext
from vector import Vector,MyDecimal
from panel import Panel
from hyperpanel import Hyperpanel

getcontext().prec=30
def _get_new_place(coofficient,plane):
    new_vector_normal=plane.vector_normal.scale_time(coofficient)
    return Hyperplane(vector_noral=new_vector_normal,constant_term=plane.constant_term*coofficient)


class linear_system(object):
    ALL_PANELS_MUST_BE_IN_SAME_DIM_MSG=(" All Panels in the solution should be in the same dimension")
    NO_SOLUTIONS_MSG="No Solutions"
    INF_SOLUTIONS_MSG="Infinitely solutions"
    def __init__(self,planes):
        try:
            d=planes[0].dimension
            for p in planes:
                assert p.dimension==d
            self.dimension=d
            self.planes=planes
        except AssertionError:
            raise(linear_system.ALL_PANELS_MUST_BE_IN_SAME_DIM_MSG)  
    
    def __len__(self):
        return len(self.planes)
    
    def __getitem__(self,i):
        return self.planes[i]
    
    def __setitem(self,plane,i):
        try:
            assert plane.dimension==self.dimension
            self.planes[i]=plane
        except AssertionError:
            raise(linear_system.ALL_PANELS_MUST_BE_IN_SAME_DIM_MSG)
            
    def __str__(self):
        ret="Linear System:\n"
        temp=["equation {}:{}]".format(i,p) for i,p in enumerate(self.planes)]
        ret +='\n'.join(temp)
        return ret
    
    def swap(self,row1,row2):
        self.planes[row1],self.planes[row2]=self.planes[row2],self.planes[row1]
        
    def multify_coofficient_and_row(self,coofficient,row):
        self[row]=_get_new_plane(coofficient,self[row])
        
    def add_multify_time_row_to_row(self,coofficient,row_to_add ,row_to_be_add_to):
        receipt_row=self[row_to_be_add_to]
        new_plane=self.multify_coofficient_and_row(coofficient,row_to_add)
        new_vector_normal=receipt_row.vector_normal.plus(new_plane.vector_normal)
        new_contant_term=receipt_row.contant_term+new_plane.contant_term
        self[row_to_be_add_to]=Hyperplane(vector_normal=new_vector_normal,contant_term=new_contant_term)
    
    def indices_of_first_nonzero_terms_each_row(self):
        num_equation=len(self)
        indices=[-1]*num_equation
        for i,p in enumerate(self.planes):
            try:
                p.first_nonzero_term(p.vector_normal)
                indices[i]=p.first_nonzero_term(p.vector_normal)
            except Exception as e:
                if str(e)==Plane.NO_NONZERO_ELMT_MSG:
                    continue;
                else:
                    raise (e)
        return indices
    
        
    
        
        