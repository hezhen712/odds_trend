import numpy as np
import math
from math import log


def kl(p, q):
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
    return np.sum(np.where(p != 0,(p-q) * np.log10(p / q), 0))
	

def lstpadding(list1,list2):
	if len(list1)>len(list2):
		more = len(list1) - len(list2)
		p = len(list2)/more
		i=1
		while i<=more:
			list2.insert(i*p,list2[i*p-1])
			i = i+1
		return list1,list2
	if len(list1)<len(list2):
		more = len(list2) - len(list1)
		p = len(list1)/more
		i=1
		while i<=more:
			list1.insert(i*p,list1[i*p-1])
			i = i+1
		return list1,list2
	if len(list1) == len(list2):
		return list1,list2

def klcmp(list1,list2):
	lstpadding(list1,list2)
	res = kl(list1,list2)
	return res