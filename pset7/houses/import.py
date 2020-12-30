from cs50 import SQL
import sys
import csv


# make database
db = SQL("sqlite:///students.db")


def main():

    # check command line arguments
    if (len(sys.argv) != 2):
        print("Error")

    # open csvfile and read into memory
    with open(sys.argv[1]) as csvfile:
        # gets rid of header info
        next(csvfile)
        reader = csv.reader(csvfile)

        # iterate over each row
        for row in reader:
            name = row[0].split(" ")

            if (len(name) == 3):
                first = name[0]
                middle = name[1]
                last = name[2]
            else:
                first = name[0]
                middle = None
                last = name[1]

            house = row[1]
            birth = row[2]

            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                       first, middle, last, house, birth)

# TODO


# open CSV file given by command line argument
    # csv.reader or csv.DictReader
    # for each row, parse name
        # separate name into first/middle/last
            # use split method (on space)
            # use None if no middle name
    # inset student into the students table od students.db
    # use db.execute to inset a row into the table
if __name__ == "__main__":
    main()