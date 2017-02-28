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

def create_normal_order(op_strings):
   "operates on a list of operator strings"
   ncreate = number_create(op_strings[0])
   maxperm = ncreate**4
   for perm in range(0,maxperm):
      n_strings = len(op_strings)
      for i in range(0,n_strings):
         curr_string = op_strings[i]
         if (is_legitimate(curr_string) == False):
            print 'Non-legitimate string'
            break

         if (is_normal_ordered(curr_string) == False):
            positions = find_pos_to_change(curr_string)
            indices = find_indices_to_change(curr_string,positions)
            new_string = curr_string[:]
            (i1,i2) = indices
            (pos1,pos2) = positions
            # Delta function
            del curr_string[pos2]
            del curr_string[pos1]
            curr_string.append(('Delta',i1,i2))
            #curr_string.append((i1,i2))
            # swap indices
            new_string[pos1], new_string[pos2] = new_string[pos2], new_string[pos1]
            new_string.append(('-','-'))
            op_strings.append(new_string)
   print op_strings

all_strings = []
op_string = [('a', 'create'), ('i', 'annihilate'), ('b', 'create'), ('j', 'annihilate')]
all_strings.append(op_string)

create_normal_order(all_strings)
      
#print all_strings
   

#a = is_normal_ordered(op_string)
##print a
##find_pos_to_change(op_string)
#positions = find_pos_to_change(op_string)
#indices = find_indices_to_change(op_string,positions)
#print positions
#print indices
