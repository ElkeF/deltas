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

def is_legitimate(operators):
   "Determine whether the number of creation and annihilation operators match"
   n = len(operators)
   ncreate = 0
   nannihilate = 0
   for pos in range(0,n):
      operator_character = operators[pos][1]
      if operator_character == 'create':
         ncreate = ncreate + 1
      if operator_character == 'annihilate':
         nannihilate = nannihilate + 1
   
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
   


op_string = [('a', 'create'), ('i', 'annihilate'), ('b', 'create'), ('j', 'annihilate')]

a = is_normal_ordered(op_string)
#print a
#find_pos_to_change(op_string)
b = find_pos_to_change(op_string)
print b
