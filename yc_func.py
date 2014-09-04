from math import sqrt
import psycopg2
import ast,sys
from crawl_engine import now_ddlist
# from scores2ranks import scores2ranks
 
def svar(X):
    n = len(X)
    if n <= 1:
       raise ValueError, "sd(): n must be greater than 1"
    xbar = float(sum(X)) /n
    return (sum([(x-xbar)**2 for x in X])/(n-1))
 
def ssd(X):
   return sqrt(svar(X))
 
 
def pearsoncor(X, Y, code = 0):
    """
    Computes pearson's correlation coefficient.code
       0 - using deviations from means.
       1 - common formula.
    """
    n = len(X)
    sx = ssd(X)
    sy = ssd(Y)
    xbar = float(sum(X)) / n
    ybar = float(sum(Y)) / n
    if code == 0:
       return sum([(x - xbar) * (y - ybar) for x, y in zip (X,Y)])/(sx * sy*(n-1.0))
    else:
       numer = sum([x*y for x,y in zip(X,Y)]) - n*(xbar * ybar)
       denom = sqrt((sum([x*x for x in X]) - n* xbar**2)*(sum([y*y for y in Y]) -n* ybar**2))
       return (numer /denom)

	   

	   
def pearsonrankcor(Rx,Ry):
    """
    Computes Pearson's rank correlation coefficient.
    Rx and Ry must be rank scores from 1 to n , not necessarily integers.
    """    
    n = len(Rx)
    return 1 - 6 *sum([(x -y)**2 for x,y in zip(Rx,Ry)])/ (n* (n*n - 1))

lst_cmp = pearsoncor
	
def get_list(mn):
	conn = psycopg2.connect(database='postgres',user='postgres',password='1985712',host= '54.186.47.255',options='-c statement_timeout=10000')
	cur = conn.cursor()
	gsql = "select ddlist from yc_dd where matches = \'%s\'" %mn
	cur.execute(gsql)
	list1 = cur.fetchone()
	cur.close()
	conn.close()
	list1 = str(list1)
	list1 = list1[3:-4]
	list1 = ast.literal_eval(list1)
	list1 = list(list1)
	return list1
 

def comp_toall(mn):	
	mdic = get_mdic()
	list1 = get_list(mn)
	com_res = {}
	for i in mdic.keys():
		if abs(len(mdic[i])-len(list1))<= 5:
			com_res.update({i:lst_cmp(list1,mdic[i])})
	
	return com_res

def comp_now(mn):	
	list1 = now_ddlist(mn)
	mdic = get_mdic()
	com_res = {}
	res = {}
	for i in mdic.keys():
		if abs(len(mdic[i])-len(list1))<= 10:
			com_res.update({i:lst_cmp(list1,mdic[i])})
	for j in com_res.keys():
		if com_res[j] >0.5:
			res.update({j:com_res[j]})
	return res
	
	
	
	
def get_mdic():
	conn = psycopg2.connect(database='postgres',user='postgres',password='1985712',host= '54.186.47.255',options='-c statement_timeout=10000')
	cur = conn.cursor()
	cur.execute("select matches from yc_dd order by matches;")
	mlist1 = cur.fetchall()
	mlist = str(mlist1)
	mlist = mlist[3:-4]
	mlist = mlist.split("',), ('")
	gsql = "select ddlist from yc_dd order by matches;"
	cur.execute(gsql)
	ddlist_all = cur.fetchall()
	conn.close()
	cur.close()
	all = str(ddlist_all)
	all = all[3:-4]
	all = all.split("',), ('")
	i = 0
	while i< len(all):
		all[i] = list(ast.literal_eval(all[i][1:-1]))
		i = i+1
	mdic = {}
	j = 0
	while j< len(mlist):
		mdic.update({mlist[j]:all[j]})
		j = j+1
	return mdic

def winrate():
	mdic = get_mdic()
	mr = get_allresult()
	winrate = {}
	act_res = {}
	for i in mdic.keys():
		res = comp_all(i,mdic)
		if res != {}:
			reslist = []
			for j in res.keys():
				reslist.append(mr[j])
			winrate.update({mr[i]:reslist})
	return winrate

		
def comp_all(mn,mdic):	
	list1 = mdic[str(mn)]
	com_res = {}
	res = {}
	for i in mdic.keys():
		if abs(len(mdic[i])-len(list1))<= 5 and i !=str(mn):
			com_res.update({i:lst_cmp(list1,mdic[i])})
	for j in com_res.keys():
		if com_res[j] >0.40:
			res.update({j:com_res[j]})
	return res
	
def get_allresult():
	conn = psycopg2.connect(database='postgres',user='postgres',password='1985712',host= '54.186.47.255',options='-c statement_timeout=10000')
	cur = conn.cursor()
	cur.execute("select matches,result from yingchao order by matches;")
	mres = cur.fetchall()
	cur.close()
	conn.close()
	mr_dic = {}
	for i in mres:
		mr_dic.update({list(i)[0]:list(i)[1]})
	return mr_dic
		
	
	
	
	
#conn = psycopg2.connect(database='postgres',user='postgres',password='1985712',host= '54.186.47.255',options='-c statement_timeout=100')
#cur = conn.cursor()