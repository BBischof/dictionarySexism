import sys
import re
femaleWords = [" she ", " She ", " she'", " She'", " her ", " Her ", " her'", " Her'", " woman ", " Woman ", " woman'", " Woman'", " female ", " Female ", " female'", " Female'", " hers ", " Hers ", " hers'", " Hers'"]
maleWords = [" he ", " He ", " he'", " He'", " him ", " Him ", " him'", " Him'", " man ", " Man ", " man'", " Man'", " male ", " Male ", " male'", " Male'", " his ", " His ", " his'", " His'"]

if len(sys.argv) >= 2:
	args = sys.argv
	sentimentfile = args[1]
	dictionaryfile = args[2]

sentDict = {}
for line in open(sentimentfile):
	record = line.strip("\n").split("	")
	sentDict[record[0]] = int(record[1])

exDict = {}
current = ""
for line in open(dictionaryfile):
	if line[0] != "-":		
		if line.strip("\n") in sentDict.keys():
			#print line
			current = line.strip("\n")
			exDict[current] = {"f": [], "m": []}
	else:
		if any(x in line for x in femaleWords):
			exDict[current]["f"].append(line.strip("\n"))
		if any(x in line for x in maleWords):
			exDict[current]["m"].append(line.strip("\n"))


# print maleWords
# print femaleWords

#print sentDict
#print dictionaryfile
count = 0
for k in exDict.keys():
	if (len(exDict[k]["f"]) + len(exDict[k]["m"]) > 0):
		count +=1
		print k + "	" + str(sentDict[k]) + "	" + str(len(exDict[k]["f"])) + "	" + str(len(exDict[k]["m"]))
#print count
