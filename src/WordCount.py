import operator

def word_count(str):
    counts = dict()
    words = str.split()
    #total=0
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
       #total+=1
        
    return counts
dataset = open("mergedDebates.txt", "r").read()
dataset = dataset.lower()
results=word_count(dataset)
#total=0
sorted_d = dict( sorted(results.items(), key=operator.itemgetter(1),reverse=True))
#print('Dictionary in descending order by value : ',sorted_d)
#print(total)
count=0
for line in dataset:
    # Splits into words
    word = line.split(" ")
    # Counts each words
    count += len(word)
print("Total Number of Words: " + str(count))

s = count
for k, v in results.items():
    pct = v * 100.0 / s
    if pct>0.01:
     print(k, pct)