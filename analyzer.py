import sys

if len(sys.argv) >= 2:
	args = sys.argv
	datafile = args[1]

totalSent = 0
femaleCount = 0
maleCount = 0
femaleSentSum = 0
maleSentSum = 0

for line in open(datafile):
	if line[0] != "w":
		columns = line.split("	")
		totalSent += int(columns[1])
		if int(columns[2])>0:
			femaleCount += int(columns[2])
			femaleSentSum += (int(columns[1])*int(columns[2]))
		if int(columns[3])>0:
			maleCount += int(columns[3])
			maleSentSum += (int(columns[1])*int(columns[3]))


print "all sentiment words sum: -1434"
print "total sentiment sum of words in gendered sentences: ", totalSent
print "count of sentences with female pronouns: ", femaleCount
print "count of sentences with male pronouns: ", maleCount
print "total sentiment sum of sentences with female pronouns: ", femaleSentSum
print "total sentiment sum of sentences with male pronouns: ", maleSentSum
print "average sentiment of sentences with female pronouns: ", float(femaleSentSum)/float(femaleCount)
print "average sentiment of sentences with male pronouns: ", float(maleSentSum)/float(maleCount)
