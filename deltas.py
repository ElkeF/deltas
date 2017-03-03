#!/opt/local/bin/python

##################################################################
#                             Deltas                             #
##################################################################
# Purpose:                                                       #
#         this script will from commutators of operators create  #
#         1. a string of annihilation and creation operators     #
#         2. do the normal ordering of the operators             #
#         3. evaluate which ones are non-zero                    #
#         4. evaluate the delta functions                        #
##################################################################
# written by:  Elke Fasshauer February 2017                      #
##################################################################

import itertools
import os

def number_create(operators):
   n = len(operators)
   ncreate = 0
   for pos in range(0,n):
      operator_character = operators[pos][1]
      if operator_character == 'create':
         ncreate = ncreate + 1
   return ncreate

def number_annihilate(operators):
   n = len(operators)
   nannihilate = 0
   for pos in range(0,n):
      operator_character = operators[pos][1]
      if operator_character == 'annihilate':
         nannihilate = nannihilate + 1
   return nannihilate

def is_legitimate(operators):
   "Determine whether the number of creation and annihilation operators match"
   n = len(operators)
   ncreate = number_create(operators)
   nannihilate = number_annihilate(operators)
   if ncreate == nannihilate:
      legitimate = True
   else:
      legitimate = False

   return legitimate

def first_annihilate(operators):
   n = len(operators)
   for pos in range(n-1,-1,-1):
      operator_character = operators[pos][1]
      if operator_character == 'annihilate':
         first_annihilate = pos
   return first_annihilate

def is_normal_ordered(operators):
   n = len(operators)
   for pos in range(0,n):
      operator_character = operators[pos][1]
      if operator_character == 'create':
         last_create = pos
   pos_first_annihilate = first_annihilate(operators)

   if last_create > pos_first_annihilate:
      is_normal = False
   else:
      is_normal = True
   return is_normal

def find_next_create(op_string,pos_ann):
   n = len(op_string)
   for pos in range(pos_ann,n):
      operator_character = op_string[pos][1]
      if operator_character == 'create':
         pos_create = pos
         break
   return pos_create

def find_pos_to_change(operators):
   first_ann = first_annihilate(operators)
   pos_create = find_next_create(op_string=operators, pos_ann=first_ann)
   if (pos_create - first_ann) > 1:
      pos_ann = pos_create - 1
   else:
      pos_ann = first_ann
   return (pos_ann,pos_create)
   
def find_indices_to_change(operators,positions):
   (pos1,pos2) = positions
   i1 = operators[pos1][0]
   i2 = operators[pos2][0]
   return (i1,i2)

def diff_spaces(op_string,pos1,pos2):
   first = op_string[pos1][0]
   sec   = op_string[pos2][0]
   first_occ = (first in ['i','j','k','l','m','n'])
   first_virt = (first in ['a','b','c','d','e','f'])
   sec_occ = (sec in ['i','j','k','l','m','n'])
   sec_virt = (sec in ['a','b','c','d','e','f'])
   if ((first_occ and sec_virt) or (first_virt and sec_occ)):
      return True
   else:
      return False

def create_normal_order(op_strings):
   "operates on a list of operator strings"
   ncreate = number_create(op_strings[0])
   maxperm = ncreate**4
   for perm in range(0,maxperm):
      n_strings = len(op_strings)
      for i in range(n_strings-1,-1,-1):
         curr_string = op_strings[i]
         ac_ops = []
         deltas = []
         split_ops_from_deltas(curr_string,deltas,ac_ops)
         if (is_legitimate(curr_string) == False):
            print 'Non-legitimate string'
            break

         if (is_normal_ordered(curr_string) == False):
            positions = find_pos_to_change(ac_ops)
            indices = find_indices_to_change(ac_ops,positions)
            new_string = ac_ops[:] + deltas[:]
            (i1,i2) = indices
            (pos1,pos2) = positions
            del op_strings[i]
            if (diff_spaces(ac_ops,pos1,pos2) == True):
               new_string[pos1], new_string[pos2] = new_string[pos2], new_string[pos1]
            else:
               # Delta function
               del ac_ops[pos2]
               del ac_ops[pos1]
               new_delta = ac_ops[:] + deltas[:]
               new_delta.append(('Delta',i1,i2))
               op_strings.append(new_delta)
               # swap indices
               new_string[pos1], new_string[pos2] = new_string[pos2], new_string[pos1]
               new_string.append(('-','-'))
            op_strings.append(new_string)
   #print op_strings

def remove_zero_strings(op_strings):
   n = len(op_strings)
   for term in range(n-1,-1,-1):
      curr_string = op_strings[term]
      for i in range(0,len(curr_string)):
         index = curr_string[i][0]
         if index in ['a','b','c','d']:
            del op_strings[term]
            break

# modified from
# http://code.activestate.com/recipes/579051-get-the-inversion-number-of-a-permutation/ under MIT license
def inversion_compared_to_reference(permList,reference):
    """
    Description - This function returns the number of inversions in a
                  permutation compared to a given order.
    Preconditions - The parameter permList is a list of unique positve numbers.

    Postconditions - The number of inversions in permList has been returned.

    Input - permList : list, reference list
    Output - numInversions : int
    """
    n = len(permList)

    if len(permList)==1:
        return 0
    else:
        numInversion=len(permList)-permList.index(reference[n-1])-1
        permList.remove(reference[n-1])
        return numInversion+inversion_compared_to_reference(permList,reference)

def permutations_list(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield list(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield list(pool[i] for i in indices[:r])
                break
        else:
            return

def split_ops_from_deltas(op_string,deltas,ac_ops):
   n = len(op_string)
   for op in range(0,n):
      if (op_string[op][1] == 'create' or op_string[op][1] == 'annihilate'):
         ac_ops.append(op_string[op])
      else:
         deltas.append(op_string[op])

def remove_redundant_perms(perms,reference):
   n = len(perms)
   for i in range(n-1,-1,-1):
      perm = perms[i]
      n_create = number_create(perm)
      for j in range(0,n_create*2):
         ref_pos = j
         curr_pos = perm.index(reference[j])
         if (reference[j][1] == 'create'):
            if not (2*ref_pos == curr_pos):
               del perms[i]
               break
      
def perm_to_deltas(permutations,delta_list):
   n = len(permutations)
   for i in range(n-1,-1,-2):
      first = permutations[i][0]
      second = permutations[i-1][0]
      delta_list.append(('Delta',first,second))
      #print delta_list

def resolve_deltas(op_strings):
   n_strings = len(op_strings)
   for string in range(n_strings-1,-1,-1):
      curr_string = list(op_strings[string])
      del op_strings[string]
      n = len(curr_string)
      deltas = []
      ac_ops = []
      split_ops_from_deltas(curr_string,deltas,ac_ops)
      #print 'Deltas', deltas, '\n'
      #print 'ac_ops', ac_ops, '\n'
      perms = list(permutations_list(ac_ops))
      remove_redundant_perms(perms,ac_ops)
      for i in range(0,len(perms)):
         all_deltas = deltas[:]
         perm = list(perms[i])
         n_inv = inversion_compared_to_reference(permList=perm,reference=ac_ops)
         if (n_inv%2 != 0): #odd
            all_deltas.append(('-','-'))
      # we now have the signs correct and add the missing Delta functions
         perm = list(perms[i])
         perm_to_deltas(perm,all_deltas)
         op_strings.append(all_deltas)
            
def latex_from_deltas(deltas,lines):
   n_deltas = len(deltas)
   minus_signs = deltas.count(('-','-'))
   if (minus_signs%2 == 0): #even
      sign = '+'
   else:
      sign = '-'
   deltas.append(sign)
 
   for i in range(n_deltas-1,-1,-1):
      curr = deltas[i]
      if (curr == ('-','-')):
         del deltas[i]
      else:
         first = deltas[i][1]
         sec   = deltas[i][2]
         del deltas[i]
         delta = r'\delta_{' + first + sec + '}'
         deltas.append(delta)
   string = ' & ' + ' '.join(deltas) + r'\\'
   lines.append(string)


def make_outfile(all_strings,filename):
   header_list = [r'\documentclass{scrartcl}',r'\usepackage[utf8]{inputenc}',r'\usepackage{amsmath}',r'\allowdisplaybreaks','\n',r'\begin{document}','\n','\section*{'+name+'}','\n',r'\begin{align}']
   outfile = open(filename, mode="w")
   header = '\n'.join(header_list)
   outfile.write(header)
   outfile.write('\n')

   n = len(all_strings)
   outlines = []
   for i in range(0,n):
      curr = all_strings[i]
      latex_from_deltas(deltas=curr,lines=outlines)

   res_lines = '\n'.join(outlines)
   outfile.write(res_lines)

   if (n == 0):
     outfile.write('0')

   outfile.write('\n')

   bottom_list = [r'\end{align}','\n',r'\end{document}']
   bottom = '\n'.join(bottom_list)
   outfile.write(bottom)

   outfile.close
   
def make_deltas(op_strings,name):
   create_normal_order(op_strings)
   remove_zero_strings(op_strings)
   resolve_deltas(op_strings)
   make_outfile(op_strings,name)


##################################################################
#                   all functions above this line                #
##################################################################

exc_ia = [('a', 'create'), ('i', 'annihilate')]
exc_jb = [('b', 'create'), ('j', 'annihilate')]
deexc_ia = [('i', 'annihilate'),('a', 'create')]
deexc_jb = [('j', 'annihilate'),('b', 'create')]
MP1_ket = [('d', 'create'), ('l', 'annihilate'), ('c', 'create'), ('k', 'annihilate')]
MP1_bra = [('k', 'create'), ('c', 'annihilate'), ('l', 'create'), ('d', 'annihilate')]
MP1_bra_p = [('i', 'create'), ('a', 'annihilate'), ('j', 'create'), ('b', 'annihilate')]
F = [('p', 'create'), ('q', 'annihilate')]
V1 = [('p', 'create'), ('r', 'create'), ('s', 'annihilate'), ('q', 'annihilate')]
V2 = [('p', 'create'), ('q', 'annihilate')]

all_strings = []

#MP_norm = MP1_bra_p + MP1_ket
#name = 'norm-MP1.tex'
#all_strings.append(MP_norm)


###################################################################
# B - Matrix
###################################################################

##<SCF| F |SCF>
#comm1 = exc_ia + F + exc_jb
#comm2 = F + exc_ia + exc_jb
#comm2.append(('-','-'))
#comm3 = exc_jb + exc_ia + V1
#comm3.append(('-','-'))
#comm4 = exc_jb + F + exc_ia
#name = 'SCF-F-SCF.tex'

##<SCF| V2 |SCF>
#comm1 = exc_ia + V2 + exc_jb
#comm2 = V2 + exc_ia + exc_jb
#comm2.append(('-','-'))
#comm3 = exc_jb + exc_ia + V2
#comm3.append(('-','-'))
#comm4 = exc_jb + V2 + exc_ia
#name = 'SCF-V2-SCF.tex'

##<SCF| V1 |SCF>
#comm1 = exc_ia + V1 + exc_jb
#comm2 = V1 + exc_ia + exc_jb
#comm2.append(('-','-'))
#comm3 = exc_jb + exc_ia + V1
#comm3.append(('-','-'))
#comm4 = exc_jb + V1 + exc_ia
#name = 'MP1-V1-SCF.tex'
#-------------------------------------------------------

##<MP1| F |SCF>
#comm1 = MP1_bra + exc_ia + F + exc_jb
#comm2 = MP1_bra + F + exc_ia + exc_jb
#comm2.append(('-','-'))
#comm3 = MP1_bra + exc_jb + exc_ia + V1
#comm3.append(('-','-'))
#comm4 = MP1_bra + exc_jb + F + exc_ia
#name = 'MP1-F-SCF.tex'

##<MP1| V2 |SCF>
#comm1 = MP1_bra + exc_ia + V2 + exc_jb
#comm2 = MP1_bra + V2 + exc_ia + exc_jb
#comm2.append(('-','-'))
#comm3 = MP1_bra + exc_jb + exc_ia + V2
#comm3.append(('-','-'))
#comm4 = MP1_bra + exc_jb + V2 + exc_ia
#name = 'MP1-V2-SCF.tex'

##<MP1| V1 |SCF>
#comm1 = MP1_bra + exc_ia + V1 + exc_jb
#comm2 = MP1_bra + V1 + exc_ia + exc_jb
#comm2.append(('-','-'))
#comm3 = MP1_bra + exc_jb + exc_ia + V1
#comm3.append(('-','-'))
#comm4 = MP1_bra + exc_jb + V1 + exc_ia
#name = 'MP1-V1-SCF.tex'
#-------------------------------------------------------

##<SCF| F |MP1>
#comm1 = exc_ia + F + exc_jb + MP1_ket
#comm2 = F + exc_ia + exc_jb + MP1_ket
#comm2.append(('-','-'))
#comm3 = exc_jb + exc_ia + V1 + MP1_ket
#comm3.append(('-','-'))
#comm4 = exc_jb + F + exc_ia + MP1_ket
#name = 'SCF-F-MP1.tex'

##<SCF| V2 |MP1>
#comm1 = exc_ia + V2 + exc_jb + MP1_ket
#comm2 = V2 + exc_ia + exc_jb + MP1_ket
#comm2.append(('-','-'))
#comm3 = exc_jb + exc_ia + V2 + MP1_ket
#comm3.append(('-','-'))
#comm4 = exc_jb + V2 + exc_ia + MP1_ket
#name = 'SCF-V2-MP1.tex'

#<SCF| V1 |MP1>
comm1 = exc_ia + V1 + exc_jb + MP1_ket
comm2 = V1 + exc_ia + exc_jb + MP1_ket
comm2.append(('-','-'))
comm3 = exc_jb + exc_ia + V1 + MP1_ket
comm3.append(('-','-'))
comm4 = exc_jb + V1 + exc_ia + MP1_ket
name = 'SCF-V1-MP1.tex'

all_strings.append(comm1)
all_strings.append(comm2)
all_strings.append(comm3)
all_strings.append(comm4)
#print all_strings

make_deltas(all_strings,name)



#ref = [('a', 'create'), ('i', 'annihilate'), ('b', 'create'), ('j', 'annihilate')]
#ex1 = [('b', 'create'), ('j', 'annihilate'), ('a', 'create'), ('i', 'annihilate')]
#
all_strings = []
op_string = [('a', 'create'), ('i', 'annihilate'), ('Delta','p','q'), ('b', 'create'), ('j', 'annihilate')]
op2_string = [('p', 'create'), ('r', 'annihilate'), ('q', 'create'), ('s', 'annihilate')]


#all_strings.append(op_string)
#all_strings.append(op2_string)

#print all_strings, '\n'
#create_normal_order(all_strings)
#print all_strings


