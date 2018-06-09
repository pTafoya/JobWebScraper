#this is an example of passing lambda expressions in python

def greaterThan(a, b):
	if a > b: return a
	else: return b

def magic(left, op, right):
	return op(left, right)
	
ans = magic(5, (lambda a, b: greaterThan(a, b)), 5)
print(ans)