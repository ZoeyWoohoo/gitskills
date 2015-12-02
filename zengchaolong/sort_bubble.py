# -*- coding:UTF-8 -*-

def bubble_sort(arry):
	n = len(arry)
	for i in range(n):
		for j in range(1,n-i):
			if arry[j-1] > arry[j] :
				arry[j-1],arry[j] = arry[j],arry[j-1]
	return arry

numbers = raw_input("input your unsorted numbers split by comma:")
arry = numbers.split(",")
print "the number list sorted:%s" %bubble_sort(arry)