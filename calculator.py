### Parth Doshi. Fiddler Lab Coding Round. ###
### cat spreadsheet.txt | python calculator.py ###
import numpy as np
import sys

def calculate_rpn(tokens, strings, recur1, recur2, index_1, index_2):
    stack = []
    recur =[]
    for t in tokens:
        t = unicode(t,'utf-8')
        #print(t)
        if t not in ["+", "-", "*", "/"]:
            if t.isnumeric():
                stack.append(float(t))
            elif t[0] == "-":                                                                               ###Negative Values###
                if t[1].isnumeric():
                    stack.append(float(t[1:])*-1)
                else:
                    if t[1:] in recur1:                                                                     ### Cycle Detection###
                        recur.append(recur1)
                        recur.append(recur2)
                        for i in range(len(recur1)):
                            print("There exists a edge from " + recur2[i] +" to "+ recur1[i])
                        separate = ", "

                        print("There exists a cyclic dependency between "+ separate.join(recur2))
                        sys.exit(recur)
                    else:
                        recur1.append(t[1:].encode('ascii','ignore'))
                        recur2.append(str(chr(index_1+65)+str(index_2+1)))
                        index = ord(t[1])-65
                        index2 = int(t[2:])-1
                        stack.append(calculate_rpn(strings[index][index2].split(), strings, recur1, recur2, index, index2)*-1)
                        recur1.remove(t[1:].encode('ascii','ignore'))
                        recur2.remove(str(chr(index_1+65)+str(index_2+1)))
            else:                                                                                          #### Cell Reference Recursion####
                if t in recur1:                                                                            #### Cycle Detection####
                    recur.append(recur1)
                    recur.append(recur2)
                    for i in range(len(recur1)):
                        print("There exists a edge from " + recur2[i] +" to "+ recur1[i])
                    separate = ", "

                    print("There exists a cyclic dependency between "+ separate.join(recur2))
                        
                    sys.exit(recur)
                else:
                    recur1.append(t.encode('ascii','ignore'))
                    recur2.append(str(chr(index_1+65)+str(index_2+1)))
                    index = ord(t[0])-65
                    index2 = int(t[1:])-1
                    stack.append(calculate_rpn(strings[index][index2].split(), strings, recur1, recur2, index, index2))
                    recur1.remove(t.encode('ascii','ignore'))
                    recur2.remove(str(chr(index_1+65)+str(index_2+1)))
        else:                                                                                              #### Operator Evaluation
            r, l = stack.pop(), stack.pop()
            if t == "+":
                stack.append(l+r)
            elif t == "-":
                stack.append(l-r)
            elif t == "*":
                stack.append(l*r)
            else:
                stack.append(l/r)
    return stack.pop()  
lines = sys.stdin.readlines()                                                               ###Input File
arr=[]
for line in lines:
    lin =line.rstrip('\r\n')
    arr.append(lin)
    print(lin)
size = arr[0].split()
n = int(size[0])
m = int(size[1])
print(n, m)
strings = np.array(arr[1:]).reshape(m,n).tolist()

recur_to = []
recur_from = []
for i in range(m):
    for j in range(n):
        expression = strings[i][j]
        tokens = expression.split()
        v = calculate_rpn(tokens, strings, recur_to, recur_from,i, j)                       ###Evaluating Reverse Polish Notation
        print('%.5f'%v)