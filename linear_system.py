#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 14:42:24 2017

@author: zqzhan
"""

from copy import deepcopy
from decimal import Decimal,getcontext
from vector import Vector,MyDecimal
from plane import Plane
from hyperplane import Hyperplane
getcontext().prec=30
def _get_new_plane(coofficient,plane):
    new_vector_normal=plane.normal_vector.times_scalar(coofficient)
    return Hyperplane(dimension=new_vector_normal.dimension, normal_vector=new_vector_normal,constant_term=plane.constant_term*coofficient)


class LinearSystem(object):
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
            raise(LinearSystem.ALL_PANELS_MUST_BE_IN_SAME_DIM_MSG)  
    
    def __len__(self):
        return len(self.planes)
    
    def __getitem__(self,i):
        return self.planes[i]
    
    def __setitem__(self,i,plane):
        try:
            assert plane.dimension==self.dimension
            self.planes[i]=plane
        except AssertionError:
            raise(LinearSystem.ALL_PANELS_MUST_BE_IN_SAME_DIM_MSG)
            
    def __str__(self):
        ret="Linear System:\n"
        temp=["equation {}:{}]".format(i,p) for i,p in enumerate(self.planes)]
        ret +='\n'.join(temp)
        return ret
    
    def swap_rows(self,row1,row2):
        self.planes[row1],self.planes[row2]=self.planes[row2],self.planes[row1]
        
    def multify_coofficient_and_row(self,coofficient,row):
        self[row]=_get_new_plane(coofficient,self[row])
        
    def add_multiple_times_row_to_row(self,coofficient,row_to_add ,row_to_be_add_to):
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
    
        
    def compute_triangular_form(self):
        system = deepcopy(self)

        num_equations = len(system)
        num_variables = system.dimension

        col = 0
        for row in range(num_equations):
            while col < num_variables:
                c = MyDecimal(system[row].normal_vector[col])
                if c.is_near_zero():
                    swap_succeeded = system.did_swap_with_row_below(row, col)
                    if not swap_succeeded:
                        col += 1
                        continue

                system.clear_coefficients_bellow(row, col)
                col += 1
                break

        return system

    def did_swap_with_row_below(self, row, col):
        num_equations = len(self)

        for k in range(row + 1, num_equations):
            coefficient = MyDecimal(self[k].normal_vector[col])
            if not coefficient.is_near_zero():
                self.swap_rows(row, k)
                return True

        return False

    def clear_coefficients_bellow(self, row, col):
        num_equations = len(self)
        beta = MyDecimal(self[row].normal_vector[col])

        for row_to_be_added_to in range(row + 1, num_equations):
            n = self[row_to_be_added_to].normal_vector
            gamma = n[col]
            alpha = -gamma / beta
            self.add_multiple_times_row_to_row(alpha, row, row_to_be_added_to)

    def clear_coefficients_above(self, row, col):
        for row_to_be_added_to in range(row)[::-1]:
            n = self[row_to_be_added_to].normal_vector
            alpha = -(n[col])
            self.add_multiple_times_row_to_row(alpha, row, row_to_be_added_to)

    def compute_rref(self):
        tf = self.compute_triangular_form()

        num_equations = len(tf)
        pivot_indices = tf.indices_of_first_nonzero_terms_in_each_row()

        for row in range(num_equations)[::-1]:
            pivot_var = pivot_indices[row]
            if pivot_var < 0:
                continue
            tf.scale_row_to_make_coefficient_equal_one(row, pivot_var)
            tf.clear_coefficients_above(row, pivot_var)

        return tf

    def scale_row_to_make_coefficient_equal_one(self, row, col):
        n = self[row].normal_vector
        beta = Decimal('1.0') / n[col]
        self.multiply_coefficient_and_row(beta, row)
        
    def do_guassian_elimination(self):
        rref=self.compute_rref()
        try:
            self.raise_execption_if_contradictory_equation()
            self.raise_exception_if_too_few_pivots()
        except Exception as e:
            return e.message
        num_variables=rref.dimension
        solution_coordinates=[rref.planes[i].contant_term for i in range(num_variables)]
        return Vector(solution_coordinates)
    
    def raise_execption_if_contradictory_equation(self):
        for plane in self.planes:
            try:
                plane.first_nonzero_index()
            except Exception as e:
                if str(e)==Plane.NO_NONZERO_ELMT_FOUND_MSG:
                    tmp_contant=MyDecimal(plane.constant_term)
                    if not tmp_contant.is_near_zero():
                        raise Exception(self.NO_SOLUTION_MSG)
                else:
                    raise(e)
    def raise_exception_if_too_few_pivots(self):
        pivot_indices=self.indices_of_first_nonzero_terms_each_row()
        num_pivots=sum([1 if  index >=0 else 0 for index in pivot_indices])
        #num_variables＝self.dimension
        num_variables=self.planes.dimension
        if (num_pivots<num_variables):
            raise Exception(self.INF_SOLUTIONS_MSG)
        
    def compute_solution(self):
        try:
            return self.do_gaussian_elimination_and_parametrization();
        except Exception as e:
            if str(e)==self.NO_SOLUTION_MSG:
                return str(e)
            else:
                raise e
    def do_gaussian_elimination_and_parametrization(self):
        rref=self.compute_rref()
        rref.raise_execption_if_contradictory_equation()
        direction_vector=self.extract_direction_vector_for_parametrization()
        basepoint_vector=self.extract_basepoint_vecotr_for_parametrization()
        return Parametrization(basepoint_vector,direction_vector)
    
    def extract_direction_vector_for_parametrization(self):
        num_variables=self.dimension
        povit_indices=self.indices_of_first_nonzero_terms_each_row()
        freedom_variables_indices=set(range(num_variables))-set(povit_indices)
        director_vector=[]
        for free_var in range(freedom_variables_indices):
            vector_coordinates=[0]*num_variables
            vector_coordinates[free_var]=1
            for index,plane in enumerate(self.planes):
                pivot_var = pivot_indices[index]
                if pivot_var < 0:
                    break
                vector_coords[pivot_var] = -plane.normal_vector[free_var]

            direction_vectors.append(Vector(vector_coords))

        return direction_vectors
        
    def extract_basepoint_vector_for_parametrization(self):
        num_variables = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()

        basepoint_coords = [0] * num_variables

        for index, plane in enumerate(self.planes):
            pivot_var = pivot_indices[index]
            if pivot_var < 0:
                break
            basepoint_coords[pivot_var] = plane.constant_term

        return Vector(basepoint_coords)
        
        
    
p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')

s = LinearSystem([p0, p1, p2, p3])
# Print initial system
# print s

p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')

s = LinearSystem([p0, p1, p2, p3])
s.swap_rows(0, 1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print ('test case 1 failed')

s.swap_rows(1, 3)
if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
    print ('test case 2 failed')

s.swap_rows(3, 1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print ('test case 3 failed')

s.multify_coofficient_and_row(1, 0)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print ('test case 4 failed')

s.multify_coofficient_and_row(-1, 2)
new_s2 = Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3')
if not (s[0] == p1 and
        s[1] == p0 and
        s[2] == new_s2 and
        s[3] == p3):
    print ('test case 5 failed')

s.multify_coofficient_and_row(10, 1)
new_s1 = Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10')
if not (s[0] == p1 and
        s[1] == new_s1 and
        s[2] == new_s2 and
        s[3] == p3):
    print ('test case 6 failed')

s.add_multiple_times_row_to_row(0, 0, 1)
if not (s[0] == p1 and
        s[1] == new_s1 and
        s[2] == new_s2 and
        s[3] == p3):
    print ('test case 7 failed')

s.add_multiple_times_row_to_row(1, 0, 1)
added_s1 = Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12')
if not (s[0] == p1 and
        s[1] == added_s1 and
        s[2] == new_s2 and
        s[3] == p3):
    print ('test case 8 failed')

s.add_multiple_times_row_to_row(-1, 1, 0)
new_s0 = Plane(normal_vector=Vector(['-10', '-10', '-10']),
               constant_term='-10')
if not (s[0] == new_s0 and
        s[1] == added_s1 and
        s[2] == new_s2 and
        s[3] == p3):
    print ('test case 9 failed')

p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
s = LinearSystem([p1, p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2):
    print ('test case 1 failed')

p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
s = LinearSystem([p1, p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == Plane(constant_term='1')):
    print ('test case 2 failed')

p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
s = LinearSystem([p1, p2, p3, p4])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2 and
        t[2] == Plane(normal_vector=Vector(['0', '0', '-2']),
                      constant_term='2') and
        t[3] == Plane()):
    print ('test case 3 failed')

p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
s = LinearSystem([p1, p2, p3])
t = s.compute_triangular_form()
if not (t[0] == Plane(normal_vector=Vector(['1', '-1', '1']),
                      constant_term='2') and
        t[1] == Plane(normal_vector=Vector(['0', '1', '1']),
                      constant_term='1') and
        t[2] == Plane(normal_vector=Vector(['0', '0', '-9']),
                      constant_term='-2')):
    print ('test case 4 failed')


# ***************

p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
s = LinearSystem([p1, p2])
r = s.compute_rref()
if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']),
                      constant_term='-1') and
        r[1] == p2):
    print ('test case 1 failed')

p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
s = LinearSystem([p1, p2])
r = s.compute_rref()
if not (r[0] == p1 and
        r[1] == Plane(constant_term='1')):
    print ('test case 2 failed')

p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
s = LinearSystem([p1, p2, p3, p4])
r = s.compute_rref()
if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']),
                      constant_term='0') and
        r[1] == p2 and
        r[2] == Plane(normal_vector=Vector(['0', '0', '-2']),
                      constant_term='2') and
        r[3] == Plane()):
    print ('test case 3 failed')

p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
s = LinearSystem([p1, p2, p3])
r = s.compute_rref()
if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']),
                      constant_term=Decimal('23') / Decimal('9')) and
        r[1] == Plane(normal_vector=Vector(['0', '1', '0']),
                      constant_term=Decimal('7') / Decimal('9')) and
        r[2] == Plane(normal_vector=Vector(['0', '0', '1']),
                      constant_term=Decimal('2') / Decimal('9'))):
    print ('test case 4 failed')


# first system
p1 = Plane(Vector([5.862, 1.178, -10.366]), -8.15)
p2 = Plane(Vector([-2.931, -0.589, 5.183]), -4.075)
system1 = LinearSystem([p1, p2])
print ('first system: {}'.format(system1.do_gaussian_elimination()))


# # second system
p1 = Plane(Vector([8.631, 5.112, -1.816]), -5.113)
p2 = Plane(Vector([4.315, 11.132, -5.27]), -6.775)
p3 = Plane(Vector([-2.158, 3.01, -1.727]), -0.831)
system2 = LinearSystem([p1, p2, p3])
print ('second system: {}'.format(system2.do_gaussian_elimination()))


# third system
p1 = Plane(Vector([5.262, 2.739, -9.878]), -3.441)
p2 = Plane(Vector([5.111, 6.358, 7.638]), -2.152)
p3 = Plane(Vector([2.016, -9.924, -1.367]), -9.278)
p4 = Plane(Vector([2.167, -13.543, -18.883]), -10.567)
system3 = LinearSystem([p1, p2, p3, p4])
print ('thrid system: {} '.format(system3.do_gaussian_elimination()))


class Parametrization(object):

    BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM = (
        'The basepoint and direction vectors should all live in the same '
        'dimension')

    def __init__(self, basepoint, direction_vectors):

        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension

        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension

        except AssertionError:
            raise Exception(self.BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM)

    def __str__(self):

        output = ''
        for coord in range(self.dimension):
            output += 'x_{} = {} '.format(coord + 1,
                                          round(self.basepoint[coord], 3))
            for free_var, vector in enumerate(self.direction_vectors):
                output += '+ {} t_{}'.format(round(vector[coord], 3),
                                             free_var + 1)
            output += '\n'
        return output


p1 = Plane(normal_vector=Vector([0.786, 0.786, 0.588]), constant_term=-0.714)
p2 = Plane(normal_vector=Vector([-0.131, -0.131, 0.244]), constant_term=0.319)

system = LinearSystem([p1, p2])
print (system.compute_solution())


p1 = Plane(Vector([8.631, 5.112, -1.816]), -5.113)
p2 = Plane(Vector([4.315, 11.132, -5.27]), -6.775)
p3 = Plane(Vector([-2.158, 3.01, -1.727]), -0.831)

system = LinearSystem([p1, p2, p3])
print (system.compute_solution())

p1 = Plane(Vector([0.935, 1.76, -9.365]), -9.955)
p2 = Plane(Vector([0.187, 0.352, -1.873]), -1.991)
p3 = Plane(Vector([0.374, 0.704, -3.746]), -3.982)
p4 = Plane(Vector([-0.561, -1.056, 5.619]), 5.973)

print (system.compute_solution())


# The systems bellow are just to test hyperplanes

p1 = Hyperplane(normal_vector=Vector([0.786, 0.786]), constant_term=0.786)
p2 = Hyperplane(normal_vector=Vector([-0.131, -0.131]), constant_term=-0.131)

system = LinearSystem([p1, p2])
print (system.compute_solution())


p1 = Hyperplane(normal_vector=Vector([2.102, 7.489, -0.786]),
                constant_term=-5.113)
p2 = Hyperplane(normal_vector=Vector([-1.131, 8.318, -1.209]),
                constant_term=-6.775)
p3 = Hyperplane(normal_vector=Vector([9.015, 5.873, -1.105]),
                constant_term=-0.831)

system = LinearSystem([p1, p2, p3])
print (system.compute_solution())

p1 = Hyperplane(normal_vector=Vector([0.786, 0.786, 8.123, 1.111, -8.363]),
                constant_term=-9.955)
p2 = Hyperplane(normal_vector=Vector([0.131, -0.131, 7.05, -2.813, 1.19]),
                constant_term=-1.991)
p3 = Hyperplane(normal_vector=Vector([9.015, -5.873, -1.105, 2.013, -2.802]),
                constant_term=-3.982)

system = LinearSystem([p1, p2, p3])
print (system.compute_solution())
        
        