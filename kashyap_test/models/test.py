def add(n):
    return n+n
number=[1,2,3,4]
k=map(add,number)
print(list(k))


l=map(lambda x:x+x,number)
print(list(l))


j=filter(lambda x:True if 2<x<4 else False,number)
print(list(j))



