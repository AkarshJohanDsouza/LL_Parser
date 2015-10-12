import re

def mkdic(grammar):
	gdict= {}
	for i in grammar:
		prod=i.split("->")
		if(prod[0] in gdict.keys()):
			gdict[prod[0]].append(prod[1])
		else:
			gdict[prod[0]]=[prod[1]]
	return gdict


def getFirst(grammar):
	first={}
	NTlist = grammar.keys()
	for prod in NTlist:
		Lfirst = get_Lfirst(prod,grammar,first)
		first[prod] = Lfirst
	
	for s in f:
		Lfirst = list(set(first[s]))
		first[s] = Lfirst

	epsilon(grammar,first)
	return first



def get_Lfirst(non_terminal,grammar,first):
	Lfirst = []
	for production in grammar[non_terminal]:
		m = re.search("[A-Z]+",production) 
		if m:
			if m.start() > 0:
				
				Lfirst.append(production[0]) 
			elif m.start() == 0:
				
				temp = firstNxt(production,first,grammar) 
				
				if temp:
					
					
					Lfirst = Lfirst + temp 


		else:
			if production is not "e":
				Lfirst.append(production[0]) 

	
	if "e" in grammar[non_terminal]:
			if "e" not in Lfirst:
				Lfirst.append("e") 
	
	return Lfirst

def firstNxt(production,first,grammar):
	Lfirst =[]
	for s in production:
		if s in first.keys():
			Lfirst = Lfirst + first[s]
		else:
			if s.isupper():
				Lfirst = Lfirst + get_Lfirst(s, grammar, first)
			else:
				return Lfirst	
		if len(production) > 1:
			if "e" in grammar[s]:
				for i in range(Lfirst.count("e")):
					Lfirst.remove("e")
					
				if production.index(s) + 1 < len(production) and production[production.index(s)+1:][0].isupper():
					temp = get_Lfirst(production[production.index(s)+1:][0], grammar, first)

				
					Lfirst = Lfirst + temp
					

					if "e" in temp:
						continue
					else:
						return Lfirst
				elif production.index(s) + 1 < len(production) and production[production.index(s)+1:][0].islower():
					Lfirst.append(production[production.index(s)+1:][0])
					return Lfirst
			else:
				return Lfirst
	return Lfirst

def epsilon(grammar,first):
	for nt in grammar.keys():
		for i in grammar[nt]:
			m=re.match("[A-Z]+",i)
			if m:
				if m.end()==len(i):
					epsFlag = True
					for s in i:
						if "e" not in first[i]:
							epsFlag= False
							break
					if epsFlag:
						if "e" not in first[nt]:
							first[nt].append("e")
					else:
						if "e" in first[nt]:
							first[nt].remove("e")


f=open("grammar.txt","r")
k=[]
for i in f.readlines():
	k.append(i.split('\n')[0])
grammar=mkdic(k)
print(getFirst(grammar))
f.close()
