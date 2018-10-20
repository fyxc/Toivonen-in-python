# import module
import re
import random
import itertools
import datetime


# read data from the dataset
input_file = open('datset.txt','r')
p=0.1 #sample size 
sup_ratio = 4.0/15
count = 0
baskets=[]
lines = input_file.readlines() #reading input from file
for line in lines:
    line= re.findall('\d+', line)
    line = map(int,line)
    # results = [int(i) for i in results]
    baskets.append(sorted(line))
    count+=1
sample_basket = []
global_support = int(sup_ratio*count)
newSupport = int(p*sup_ratio*count)

## define func

# func to generate sample
def generateSample(totalnum,iteration,sampleSize):
    random.seed(iteration)
    index = random.randint(0, totalnum-sampleSize) 
    sample_basket = baskets[index: index+30]
    return sample_basket

# func to get fre set
    
frequentItemsets ={}
infrequentItemsets = {}

def FreqItems(basket, size, support):
    global infrequentItemsets
    global frequentItemsets
    flag=False
    Items={}    
    for line in basket:
        if size ==1:
            tempItems=list(itertools.combinations(line,size))
            for tuples in tempItems:
                if tuples in Items:
                    Items[tuples]+=1
                else:
                    Items[tuples]=1
        else:
            tempItems=list(itertools.combinations(line,size))
            for tuples in tempItems:
                temp2Items=list(itertools.combinations(tuples,size-1))
                for item in temp2Items:
                    if item in frequentItemsets:
                        flag=True
                    else:
                        flag=False
                        break
                if flag==True:
                    tuples=tuple(sorted(tuples))
                    if tuples in Items:
                        Items[tuples]+=1
                    else:
                        Items[tuples]=1

    for key in Items:
        if Items[key]>= support:
            frequentItemsets[key]=Items[key]   # list_key_value = [ [k,v] for k, v in dict. items() ]   	
            
    length_current_iter=len(frequentItemsets)
    
    return frequentItemsets,infrequentItemsets,length_current_iter


# func to get negtiveboard

negativeBorder = {}
def getNegtiveBoard(infrequentItemsets, previousFrequentItemsets, size):
    for key in infrequentItemsets:
        if len(key)==1:
                negativeBorder.add(key)
        else:
            count =0;

            for subset in itertools.combinations(key, size-1):

                if  list(subset) not in previousFrequentItemsets:
                    count+=1
            if count ==0:
                negativeBorder.add(key)	
    return negativeBorder


# global frequent set
size = 1
length_current_iter_all=1
length_pre_iter_all=0
while length_current_iter_all!=length_pre_iter_all:
    length_pre_iter_all=length_current_iter_all  
    allfrequentItemsets,nouse,length_current_iter_all = FreqItems(baskets,size, global_support)
    size+=1



#Main Function
if __name__ == '__main__':
    starttime = datetime.datetime.now()
    repeatToivonen=True
    numberofiterations = 0
    while repeatToivonen==True:
        
        numberofiterations+=1
        repeatToivonen=False

    #Generating local frequent and find the negative board
        sample_basket=generateSample(300, numberofiterations, 30)       
        size= 1  

        previousFrequentItemsets = []

        length_current_iter=1
        length_pre_iter=0
        while length_current_iter!=length_pre_iter:
            length_pre_iter=length_current_iter  
            frequentItemsetsCandidates,infrequentItemsets,length_current_iter = FreqItems(sample_basket,size,newSupport)
            negativeBorder = getNegtiveBoard(infrequentItemsets, previousFrequentItemsets, size)
            previousFrequentItemsets = frequentItemsetsCandidates
            size+=1
        
        false_negative = []
        for item in negativeBorder:
            if item in allfrequentItemsets:
                false_negative.append(item)
        print ('False Negative:',sorted(false_negative))
        
        global_fre = []
        for key in frequentItemsetsCandidates:
            if key in allfrequentItemsets:
                global_fre.append(key)
        
     
    #****************************************************************"""
             # write files
        filename = "OutputForIteration_{}.txt".format(str(numberofiterations))
        output = open(filename, "w")

        output.write("Sample created: \n")
        for sample_itemset in sample_basket:
            output.write(str(list(sample_itemset)) + ", ")
        output.write("\n")

        output.write("Frequent itemsets: \n")
        for frequent_itemset in global_fre:
            if len(frequent_itemset) == 1:
                output.write("(" + str(frequent_itemset[0]) + "), ")
            else:
                output.write(str(frequent_itemset) + ", ")
        output.write("\n")

        output.write("Negative border: \n")
        for border_itemset in negativeBorder:
            if len(border_itemset) == 1:
                output.write("(" + str(border_itemset[0]) + "), ")
            else:
                output.write(str(border_itemset) + ", ")

        output.close()

        if len(false_negative) != 0: 
            repeatToivonen=True
        else:
            repeatToivonen=False
    
    
    endtime = datetime.datetime.now()
    print ("-----" + str((endtime - starttime).seconds) + " s" + "-----")
    
