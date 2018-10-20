import sys
import itertools
import time
from random import shuffle

def combination(frequent_item,size):
    out = []
    for i in range(len(frequent_item)):
        for j in range(i+1,len(frequent_item)):
            if (sorted(frequent_item[i])[:size-1] == sorted(frequent_item[j])[:size-1]) \
            and (tuple(sorted(set(frequent_item[i]).union(set(frequent_item[j])))[1:]) in frequent_item):
                out.append(tuple(sorted(set(frequent_item[i]).union(set(frequent_item[j])))))

    return out



def Priori_count(sample, support,itemsets):
    baskets = sample
    size = 0
    final_iterator = []
    negative_border = []
    max_size = len(itemsets)
    while len(itemsets) != 0 and size < max_size:
        size += 1
        frequent_item = []
        for i in itemsets:
            count = 0
            for j in baskets:
                if isinstance(i, int):
                    if i in j:
                        count += 1
                else:
                    if set(i).issubset(j):
                        count += 1
            if count >= support:
                if isinstance(i, int):
                    frequent_item.append(i)
                    final_iterator.append(i)
                else:
                    frequent_item.append(tuple(i))
                    final_iterator.append(tuple(i))
            else:
                if isinstance(i, int):
                    negative_border.append(i)
                else:
                    negative_border.append(tuple(i))
        candidate = set(tuple(sorted(i)) for i in itertools.combinations(tuple(frequent_item),2)) if size == 1 else combination(frequent_item,size)
        if size != 1:
            itemsets = [i for i in candidate if
                        all(leave in frequent_item for leave in itertools.combinations(i,size)) is True]
        else:
            itemsets = [i for i in candidate if
                        all(leave in frequent_item for leave in i) is True]
    return final_iterator, negative_border


def countanddecide(items, datasets, s):
    final_iterator = []
    for i in items:
        count = 0
        for j in datasets:
            if isinstance(i, int):
                if i in j:
                    count += 1
            else:
                if set(i).issubset(j):
                    count += 1
        if count >= s:
            final_iterator.append(i)
    return sorted(final_iterator)


def main(filename):
    start_time = time.time()
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    whole_data=[]
    for i in content:
        i = i.strip('()\n').split(',')
        i = list([int(j) for j in i])
        whole_data.append(i)
    itemsets = set([item for line in whole_data for item in line])
    threshold = 80
    p = 10
    support = threshold/p
    index = 0
    times = -1
    step = len(whole_data)/p
    test = ['smt']
    while test:
        if index+step > len(whole_data):
            sys.exit("Error message")
        sample = whole_data[index:index+step]
        candidate,negative_border = Priori_count(sample, support,itemsets)
        test = countanddecide(negative_border,whole_data,threshold)
        print (test)
        index += 10
        times += 1
    data = countanddecide(candidate,whole_data,threshold)
    print (data)
    maxsize = max([len(x) if not isinstance(x, int) else 1 for x in data])
    f = open('sample.txt', "w")
    # f.write('\n'.join('({})'.format(str(x).strip('[]')) for x in whole_data))
    f.write(', '.join('({})'.format(x) for x in [x for x in data if isinstance(x, int)]))
    line = 2
    while line <= maxsize:
        f.write('\n\n')
        f.write(', '.join('{}'.format(x) for x in [x for x in data if (not isinstance(x, int)) and len(x) == line]))
        line += 1
    f.close()
    print("--- %s times interation ---" % times)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    filename = sys.argv[1]
    # Execute Main functionality
    main(filename)
