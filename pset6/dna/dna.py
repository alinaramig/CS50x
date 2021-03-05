import csv
import sys


def main():

    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("MISSING COMMAND LINE ARGUMENTS")

    people = []
    # Read people's DNA from file into memory
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            people.append(row)

    # Stores STR's in memory
    STR = []
    for key in people[0]:
        if key != "name":
            STR.append(key)

    # Reads DNA string into memory
    with open(sys.argv[2]) as file:
        DNA = file.read()

    frequency = {}

    # Searches for each STR in the DNA string
    for key in STR:
        frequency[key] = repeat(DNA, key)

    # Searches for a DNA match
    for row in people:
        match = True
        for key in frequency:
            if int(row[key]) != frequency[key]:
                match = False
        if match == True:
            print(row["name"])
            return

    print("No match")

# Takes A DNA string and an STR as imput and outputs the number of times that STR is repeated


def repeat(DNA, STR):
    
    max_reapeated = 0
    for i in range(len(DNA)):
        reapeated = 0
        for n in range(i, len(DNA), len(STR)):
            end = len(STR) + n
            slicy = DNA[n:end]
            if DNA[n:end] == STR:
                reapeated += 1
            else:
                break
        
        max_reapeated = max(max_reapeated, reapeated)
        
    return max_reapeated

   
main()