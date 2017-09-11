#!/usr/bin/env python
import fileinput, sys, argparse
from argparse import RawTextHelpFormatter

'''
This function normalizes the selected cell
'''
def normalize(string, ignore_list=list(")('n")):

    nbuffer = [] #we will use this list to keep the digits until a non-digit letter is found
    groups = []  #we will save the groups of letters here

    #loop through the string from right to left
    #C6H8N2O2R2' <= starting here, from right to left
    #The [::-1] is a trick to put the list of letters "string" backwards
    for letter in string[::-1]:
        if letter in ignore_list: #remove useless letters
            continue #stop this iteration, start over with the next letter

        try: #try to convert the letter to a number
            _ = int(letter) #convert the letter to a number and discard the result '1' => 1
            nbuffer.append(letter) #add the letter to the buffer because it might have more than one digit
        except: #if it fails to convert the letter to a number, then it's a letter and not a digit
            #replace letters
            if letter == 'A': #radical. Change A by R
                letter = 'R'
            #if the current letter is not a digit it means we have already seen a digit or this is a sole letter with no number
            #check if the list "nbuffer" has something and if so, convert the digit letters to the corresponding number
            if len(nbuffer) > 0:
                number = ''.join(nbuffer) #the join function joins the digit together ['1', '2'] => '12'
                number = int(number[::-1])      #the int function converts the string to a number '12' => 12
                nbuffer = []              #reset the buffer to an empty list
            else:
                number = 1                #if there is no number, then multiply by one
            groups.append(letter*number)  #append the "letter" repeated by "number" times
    #the string must finish (actually begin) with a non-digit letter
    groups = sorted(groups) #sort the groups of letters ['OO', 'CCC'] => ['CCC', 'OO']
    return ''.join(groups)  #join groups of letters into a string ['CCC', 'OO'] => 'CCCOO'

'''
Function for processing the execution parameters
'''
def parse_args():
    description = """

       _~
    _~ )_)_~
    )_))_))_)
    _!__!__!_
    \_______/
  ~~~~~~ ~~~~~~
  ~~ ~~~~  ~~~~
   Carlos Vega
    8-Sept-17
      v0.1

Molecular Formulae Comparator

This program checks if two columns of chemical equations are the same.
Asumes numbers can have multiple digits. Asumes elements have ONLY one letter
And if there is a letter without number, it assumes there is a "1" besides

It ignores the following characters: ' ) ( n
It replaces the letter A to R for the radical

Examples:

C6H8N2O2R2'             would yield true compared to:   A2C6H8N2O2'
C4H7N2O3R(C2H2NOR)n'    would yield true compared to:   A2C6H9N3O4'

C5H8N2O2'               would yield FALSE compared to:  A2C6H9N3O3'

"""
    parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input', dest='input', required=True, default='-', help='Input file. Default: stdin')
    parser.add_argument('-o', '--output', dest='output', required=False, type=argparse.FileType('w'), default=sys.stdout, help='Output file. It will use the same separator. Default stdout')
    parser.add_argument('-s', '--separator', dest='separator', required=False, default=';', help='File Separator. Default: Semicolon ";"')
    parser.add_argument('-a', '--column_a', dest='column_a', required=False, type=int, default=1, help='Number of the column A, starting in 1. Default 1.')
    parser.add_argument('-b', '--column_b', dest='column_b', required=False, type=int, default=2, help='Number of the column B, starting in 1. Default 2.')
    parser.add_argument('--ignore', dest="ignore_letters", required=False, default=")(n'", help='The letters specifed will be ignored. Introduce them without spaces like this, which is the default, including quotes: ")(n\'"')
    parser.add_argument('--no-header', dest='no_header', default=False, action='store_true', help="Use this option if you don't want to avoid the first line.")
    parser.add_argument('--keep-columns', dest='keep_columnns', default=False, action='store_true', help='Keep the other columns and append the new at the right.')
    parser.add_argument('--version', dest='version', default=False, action='store_true', help="Prints the program version.")
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.version:
        print >> sys.stderr, 'Molecular Formulae Comparator v0.1'
        sys.exit()

    if args.column_a == args.column_b:
        print >> sys.stderr, 'Column A and B must be different'
        sys.exit()
    return args


#MAIN PROGRAM
args = parse_args() #load the execution parameters

try:
    for line in fileinput.input(args.input): #open the file
        line = line.rstrip() #remove the break line character from the line

        split_line = line.split(args.separator) #split by the given separator
        a = split_line[args.column_a - 1]
        b = split_line[args.column_b - 1]

        if fileinput.isfirstline() and not args.no_header: #don't process the first line if the option no_header is not used
            if args.keep_columnns:
                print >> args.output, args.separator.join([line, 'A Normalized', 'B normalized', 'Is Equal?'])
            else:
                print >> args.output, args.separator.join([a, b, 'A Normalized', 'B normalized', 'Is Equal?'])
            continue #jump to the next iteration

        norm = lambda x : normalize(x, ignore_list=list(args.ignore_letters))

        norm_a = norm(a)
        norm_b = norm(b)
        result = str(norm_a == norm_b)
        if args.keep_columnns:
            print >> args.output, args.separator.join([line, norm_a, norm_b, result])
        else:
            print >> args.output, args.separator.join([a, b, norm_a, norm_b, result])
except IOError as e:
    print >> sys.stderr, "I/O error({0}): {1} {2}".format(e.errno, e.strerror, args.input)

