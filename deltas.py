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


def is_normal_ordered(operators):
   n = len(operators)
   ncreate = 0
   nannihilate = 0
   for pos in range(0,n):
      operator_character = operators[pos][1]
      if operator_character == 'create':
         ncreate = ncreate + 1
      if operator_character == 'annihilate':
         nannihilate = nannihilate + 1
      print operator_character

   print ncreate
   print nannihilate

op_string = [('a', 'create'), ('i', 'annihilate'), ('b', 'create'), ('j', 'annihilate')]

a = is_legitimate(op_string)
print a
