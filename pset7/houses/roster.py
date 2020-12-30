from cs50 import SQL
import sys
import csv

db = SQL("sqlite:///students.db")


def main():
    # check command line arguments
    if (len(sys.argv) != 2):
        print("Error")

    # store command line argument
    chosenHouse = sys.argv[1]

    studentsInHouse = db.execute(
        "SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", chosenHouse)

    for row in studentsInHouse:
        if (row['middle'] == None):
            print(f'{row["first"]} {row["last"]}, born {row["birth"]}')
        else:
            print(f'{row["first"]} {row["middle"]} {row["last"]}, born {row["birth"]}')


if __name__ == "__main__":
    main()

    # roster sorted by last name and then by first name