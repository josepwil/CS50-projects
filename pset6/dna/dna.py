import sys
import csv


# FIND MAX REP helper function - takes in string and substring and returns max number of times the substring consecutively appears in the string
def findMaxRep(s, subS):
    temp = [0] * len(s)
    # iterate from end string to start
    for i in range(len(s) - len(subS), -1, -1):
        # if sub-string found
        if(s[i: i + len(subS)] == subS):
            # checks if first time i.e. it goes to the end of the string
            # if so add 1 to temp array at that start index
            if(i + len(subS) > len(s) - 1):
                temp[i] = 1
            # if not first time add 1 and the value of the next index to the index of temp
            else:
                temp[i] = 1 + temp[i + len(subS)]
    # return the max number in the temp array
    return max(temp)


# PRINT MATCH helper function - checks array against database for a match
def printMatch(reader, seqHeader):
    for row in reader:
        name = row[0]
        values = []
        for value in row[1:]:
            values.append(int(value))
        if (values == seqHeader):
            print(name)
            return
    print("No match")


def main():
    # check number of command line arguments
    if (len(sys.argv) != 3):
        print("error")

    # open csvfile and read into memory
    with open(sys.argv[1]) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)[1:]

        # open text file
        with open(sys.argv[2]) as txtFile:
            txtFile = txtFile.read()
            # returns an array (maxRepArray) of max repetitions for each Str 
            maxRepArray = []
            # for each str in the header [AGAT, AATG etc.] - find the max reps and append to max reps array
            for seq in header:
                maxRepArray.append(findMaxRep(txtFile, seq))

        printMatch(reader, maxRepArray)
        

if __name__ == "__main__":
    main()