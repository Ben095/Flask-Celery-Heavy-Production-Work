# def f2(n, result):
# 	if n == 0:
# 		return 0
# 	else:
# 		#print f2(2-1, 2)
# 		#print f2(n-1, n + result)
# 		print n -1 , n+result
# 		return f2(n-1, n + result)

# print f2(5,10)


# def f4(n):
# 	if n == 50:
# 		return 50
# 	else:
# 		#print n
# 		return f4(n+1)

# print f4(20)
# def simple(n):
# 	if n == 6:
# 		return 6
# 	return simple(n+4)

# print simple(2)
# counter = 1
# def count():
# 	global counter
# 	t = (1,2,3)
# 	##print type(t)
# 	#for i,v in enumerate(t):
# 		#print 0, 1

# 	for i,v in enumerate(t):
# 		#print i, v
# 		# #'0', '1'
# 		# ##'1', '2'
# 		# #'2', '3'
# 		# '0','1','2','3'
# 		# #3 + 5 + 7 + 9 + 10
# 		print i
# 		counter +=i + v
# 		#print counter
# #1+1 = 2+4=
# count()
# # 1 +1 = 2
# # 2 + 2 = 4
# # 4+3 = 7

# # 1 + 1 + 1 = 3
# # 3 + 1 + 2 = 6
# # 6 + 1 + 3 = 10
# print counter
# number = 1

# for i in range(3):

# 	number += 3
# 	print number
	# print "NUMBER" + str(number) + "," + str(i)
	# number +=i
	# # 1+0 = 1 
	# # 1+1 = 2
	# # 1+2 = 3
	# # 1+3 = 4
	# print number


# 0,1
# 1,2
# 2,3
# 3,1

# 1, 2
# 2, 3
# 3, 4
# 4, 2

#from functools import *

# def add(a,b,c):
# 	return 50*a+5*b+c

# res = partial(add, c=2,b=1)
# print res(2)


# def integer(b,c):
# 	return b+1+c

# res = partial(integer , b =1, c = 2)
# print res(4)

# L = [[[1,2,3],[4,5]],6] 
# # print L

# g = str(L).replace('[','').replace(']')

# nums = list()
# i = 3
# while (i < 9):
# 	nums.append(i)
# 	#[4+2,5+2,6+2,7+2,8+2]
# 	#[6,7,8,9,10]\	
# 	#print i
# 	i = i+1
# 	print i
# print(nums)
# import threading
# k = 10
# x = 20
# m = threading.Lock()
# #import threading
# def foo():
# 	global x
# 	return x
# 	# for i in xrange(k):
# 	# 	with m:
# 	# 		x+=1

# print foo()
# def bar():
# 	global x
# 	for i in xrange(k):
# 		with m:
# 			x -= 1


# t1 = threading.Thread(target=foo)
# print t1.start()
# t2 = threading.Thread(target=bar)
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print x

# fp = None
# with open('bingbeats.py','r') as fp:
# 	cont = fp.read()
# print fp.closed
# items = set()
# items.add('google')
# items.add('apple')
# items.add('microsoft')
# print(items)
# x = []
# y = x
# y.append(10)
# z = 5
# w = z
# z = z-1
# print (y)
# print (x)
# print (z)
# print (w)
# def a():
# 	print "a executed"
# 	return []

# def b(x=a()):
# 	x.append(5)
# 	x.append(1)
# 	print x
# b()
# b()
# b()
# orig = {'1':1,'2':2}
# a_copy = orig.copy()
# orig['1'] = 5
# sum = orig['1'] + a_copy['1']
# print sum



# class foo:
# 	def normal_call(self):
# 		print ("nromal call")
# 	def call(self):
# 		print ('first call')
# 		self.call = self.normal_call
# y = foo()
# y.call()
# y.call()
# y.call()


