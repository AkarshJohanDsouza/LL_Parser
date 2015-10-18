import re
#FINDING TERMINALS AND NON-TERMINALS
def getnterminals(grammar):
        ntlist = set()
        for i in grammar:
                prod=i.split("->")
                ntlist.add(prod[0])
        return ntlist
                
def getterminals(grammar):
        tlist = set()
        for i in grammar:
                prod = i.split('->')
                for j in prod[1]:
                        if j not in nterminals and j != 'e':
                                tlist.add(j)
        return tlist

#FINDING FIRST
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
                                                if "e" not in first[s]:
                                                        epsFlag= False
                                                        break
                                        if epsFlag:
                                                if "e" not in first[nt]:
                                                        first[nt].append("e")
                                        else:
                                                if "e" in first[nt]:
                                                        first[nt].remove("e")



        
#FINDING FOLLOW
def find_follow(grammar):
  follow_not_found_dictionary ={}   
  grammar_dictionary = {}
  list_of_symbols_in_order = []

  for eachGrammarProduction in grammar:
     eachGrammarProduction = eachGrammarProduction.split("->")
     eachGrammarProduction[0] = eachGrammarProduction[0].replace(" ","")
     eachGrammarProduction[0] = eachGrammarProduction[0].replace("\n","")
     eachGrammarProduction[1] = eachGrammarProduction[1].replace(" ","")
     eachGrammarProduction[1] = eachGrammarProduction[1].replace("\n","")

     if not(eachGrammarProduction[0] in list_of_symbols_in_order):

      list_of_symbols_in_order.append(eachGrammarProduction[0])

     if(eachGrammarProduction[0] in grammar_dictionary):
       grammar_dictionary[eachGrammarProduction[0]].append(eachGrammarProduction[1])

     else:
       grammar_dictionary[eachGrammarProduction[0]] = [eachGrammarProduction[1]]

  follow_dictionary = {}
  first = getFirst(grammar_dictionary)#change made here

  start_symbol = list_of_symbols_in_order[0]
  follow_dictionary[start_symbol] = ['$']

  for everySymbol in list_of_symbols_in_order[1:]:
      follow_dictionary[everySymbol] =[]

  for everySymbol in list_of_symbols_in_order:

      productions_found = find_productions(grammar_dictionary,everySymbol)
      process_productions_found(productions_found,first,follow_dictionary,follow_not_found_dictionary,everySymbol)


  for everySymbol in follow_not_found_dictionary.keys():
    if len(follow_not_found_dictionary[everySymbol]) != 0:
      for NonTerminal in follow_not_found_dictionary[everySymbol]:
        for eachTerminal in follow_dictionary[NonTerminal]:
          if eachTerminal not in follow_dictionary[everySymbol]:
            follow_dictionary[everySymbol].append(eachTerminal)


  return follow_dictionary


def find_productions(grammar , symbol):
    
    productions_found_dictionary = {}
    for eachKey in grammar.keys():
        temp_list = []
        for eachElement in grammar[eachKey]:
            
            if symbol in eachElement:
                temp_list.append(eachElement)

        productions_found_dictionary[eachKey] = temp_list
        #change made here
    productions_found_dictionary={k : v for k,v in productions_found_dictionary.items() if v}

            
    return productions_found_dictionary  


def process_productions_found(productions,first,follow,follow_not_found_dictionary,symbol):
       
    follow_not_found_dictionary[symbol] = []

    for eachLeftHandSide in productions.keys():
       
       
       for eachRightHandSide in productions[eachLeftHandSide]:
         flag = 0
         i = -1 


         for everyCharacter in eachRightHandSide:
          if(flag == 0):
             i = i+ 1 
             if everyCharacter == symbol:
                 flag = 1
                 if((i+1) is len(eachRightHandSide)):

                     if not(eachLeftHandSide == eachRightHandSide[i]):
                         
                         if len(follow[eachLeftHandSide]) == 0:
                              follow_not_found_dictionary[symbol].append(eachLeftHandSide)
                         else:
                               for everySymbol in follow[eachLeftHandSide]:
                                 if not(everySymbol in follow[symbol]):
                                  follow[symbol].append(everySymbol)


                     else:
                          if not ("$" in follow[symbol]):
                              follow[symbol].append("$")
    
                 else:
                     
                     temp_list = []
                     first_union_flag = 0
                     no_of_non_terminals_found_continuously = 0;
                     no_of_epsolon = 0
                            
                     for s in range((i+1),len(eachRightHandSide)):
                         if not(eachRightHandSide[s].isupper()):
                            first_union_flag = 1
                            temp_list.append(eachRightHandSide[s])
                            no_of_non_terminals_found_continuously = 0;
                            no_of_epsolon = 0
                            break

                         else:
                              no_of_non_terminals_found_continuously =  no_of_non_terminals_found_continuously + 1
                              has_epsolon_flag = 0

                              for eachTerminal in first[eachRightHandSide[s]]:
                                  if eachTerminal == "e":
                                      no_of_epsolon = no_of_epsolon +1
                                      has_epsolon_flag =1

                                  else:

                                      if not(eachTerminal in temp_list):
                                          temp_list.append(eachTerminal)

                              if has_epsolon_flag == 0:
                                break

                     if first_union_flag == 1:
                         for eachSymbol in temp_list:
                             follow[symbol].append(eachSymbol)

                     elif no_of_non_terminals_found_continuously == no_of_epsolon and not(no_of_non_terminals_found_continuously == 0):
                         for m in follow[eachLeftHandSide]:
                             if not(m in follow[symbol]):
                                 follow[symbol].append(m)

                         for a in temp_list:
                             if not(a in follow[symbol]):
                                 follow[symbol].append(a)

                              

                     elif no_of_non_terminals_found_continuously != no_of_epsolon:
                          for n in temp_list:
                              if not(n in follow[symbol]):
                                  follow[symbol].append(n)
                                  

             else:
                 continue

#TABLE CONSTRUCTION
def maketable(nterminals,terminals,first,follow,grammar):
        table = dict()
        for i in grammar:
                table[i]=dict()
                for j in grammar[i]:
                        col = []
                        if j[0] == 'e':
                                col = follow[i]
                        elif j[0] in terminals:
                                col.extend(j[0])
                        else:
                                vals = firstNxt(j,first,grammar)
                                if(len(vals)==0):
                                        vals+='e'
                                
                                flag=1
                                for n in j:
                                        if n in nterminals:
                                                if 'e' not in first[n]:
                                                        flag=0
                                if flag == 1:
                                        vals+='e'
                        
                                if('e' in vals):
                                        for b in range(vals.count('e')):
                                                vals.remove('e')
                                        vals = vals + follow[i]
                                col.extend(vals)
                        for k in col:
                                table[i][k]=i+"->"+j
                for v in follow[i]:
                        if v not in table[i]:
                                table[i][v] = "sync"
        return table

#MAIN
f=open("grammar.txt","r")
k=[]
print("Grammar :")
for i in f.readlines():
        k.append(i.split('\n')[0])
        print(i)

nterminals = getnterminals(k)
print("NonTerminals :")
for i in nterminals:
        print(i)
print()

terminals = getterminals(k)
print("Terminals :")
for i in terminals:
        print(i)
print()

grammar=mkdic(k)
first=getFirst(grammar)
follow = find_follow(k)
print("First :")
for i in first:
        print(i," : ",first[i])
print()

print("Follow :")
for i in follow:
        print(i," : ",follow[i])
print()

table= maketable(nterminals,terminals,first,follow,grammar)
print("TABLE :")
for i in table:
        print(i,"->",table[i])
f.close()

