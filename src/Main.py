# Creator : Zaki Yudhistira Candra
# NIM     : 13522031
# Cyberpunk breach protocol solver

import random as rd
import time as tm

# Global variable
path = "test/Input/"
save_path = "test/Solution/"

class Sequence: # Contains sequence code and its score
    def __init__(self, sequence, points):
        self.sequence = sequence
        self.points = points

    def printData(self):
        first = True
        for seq in self.sequence:
            if first:
                print(seq, end="")
                first = False
            else:
                print(" " + seq, end="") 
        print("\nPoints : " + str(self.points))

def printSequences(sequences): # For displaying sequences
    first = True
    print(">>> Sequences <<<")
    for i in range (len(sequences)):
        if first:
            Sequence.printData(sequences[i])
            first = False
        else:
            print("")
            Sequence.printData(sequences[i])

def generateSequence(tokens, max, number_of_sequence):
    # Randomly generate sequences
    sequences = []
    for i in range(number_of_sequence):
        temp = []
        for j in range(rd.randint(1,max)):
            index = rd.randint(0, len(tokens)-1)
            temp.append(tokens[index])
        sequences.append(Sequence(temp, rd.randint(1,10)*10))
    return sequences
            
class Token: # Token class
    def __init__(self, token, x, y):
        self.token = token
        self.x = x
        self.y = y

def compareToken(tokens, seq):
    # Comparing 2 array of tokens and returns a boolean
    if len(seq) > len(tokens):
        return False
    else:
        for i in range(len(tokens) - len(seq) + 1):
            if seq[0] == tokens[i]:
                flag = True
                for j in range(1, len(seq)):
                    if seq[j] != tokens[i+j]:
                        flag = False
                        break
                if flag:
                    return True
        return False   

def getTokenList(tokens):
    # Converting from an array of token into an array of strings
    return [token.token for token in tokens]

class Matrix: # Matrix class where tokens are placed
    def __init__(self, content, row, column):
        self.content = content
        self.column = column
        self.row = row
        self.size = row*column

    def printMatrix(self):
        for i in range(self.row):
            first = True
            for j in range(self.column):
                if first:
                    print(self.content[i][j].token, end="")
                    first = False
                else:
                    print(" " + self.content[i][j].token, end="")
            print("")

def generateMatrix(tokens, row, column):
    # Randomly matrix generation
    matrix = []
    for i in range(row):
        line = []
        for j in range(column):
            index = rd.randint(0, len(tokens) - 1)
            line.append(Token(tokens[index],j,i))
        matrix.append(line)
    return Matrix(matrix, row, column)

# Misc functions

def getScore(sequences, tokens):
    # Calculate possible score from the sequences and a solution
    score = 0
    for seq in sequences:
        if compareToken(getTokenList(tokens), seq.sequence):
            score += seq.points
    return score

def getSolution(solutions, sequences):
    # Solving algorithm for finding the most optimal path / sequence
    max = getScore(sequences, solutions[0])
    solve = solutions[0]
    for i in range(1, len(solutions)):
        if getScore(sequences, solutions[i]) > max:
            max = getScore(sequences, solutions[i])
            solve = solutions[i]
    return max, solve

# Welcome menu
print("|| BREACH PROTOCOL SOLVER ||")
print("----------------------------")
print("||   By Zaki Yudhistira   ||")
print("----------------------------")

# Option to load a custom breach protocol
initiation = input("Do you want to load a custom protocol ? (y/n) : ")
initiation = initiation.lower()
if initiation == "y":
    # File handling
    initiation = input("Please enter file name  : ")
    path = path + initiation
    try:
        file = open(path, 'r')
    except FileNotFoundError:
        print(initiation + " is not found, please recheck your filename.")
        exit()
    
    # Initialization
    buffer_size = int(file.readline())
    matrix_WnH = file.readline()
    matrix_WnH = matrix_WnH.split(" ")
    matrix_length = int(matrix_WnH[0])
    matrix_width = int(matrix_WnH[1])
    print(matrix_width, matrix_length)
    main_matrix = []
    for i in range(matrix_length):
        lines = file.readline()
        lines = lines.rstrip('\n')
        lines = lines.split(" ")
        main_matrix.append(lines)
    for i in range(matrix_length):
        for j in range(matrix_width):
            main_matrix[i][j] = Token(main_matrix[i][j], j, i)
    main_matrix = Matrix(main_matrix, matrix_length, matrix_width)
    sequence_count = int(file.readline())
    sequences = []
    for i in range(sequence_count*2):
        line = file.readline()
        if i % 2 == 0:
            s_temp = (line.rstrip('\n')).split(" ")
        else:
            sequences.append(Sequence(s_temp, int(line)))

elif initiation == "n":
    # Data input
    number_of_token = int(input("Please input the number of tokens : "))
    print("Please provide the tokens below :")
    tokens = str(input())
    tokens = tokens.upper()
    tokens = tokens.split(" ")
    if len(tokens) != number_of_token:
        print("Token invalid, exiting program.")
        exit()
    buffer_size = int(input("| Enter buffer size : "))
    sequence_count = int(input("| Enter sequence count   : "))
    max_sequence_size = int(input("| Enter maximum sequence length : "))
    matrix_WnH = input("Enter matrix row and column (row column) : ")
    matrix_WnH = matrix_WnH.split(" ")
    row = int(matrix_WnH[0])
    column = int(matrix_WnH[1])

    # Generation
    print("Generating breach protocol...")
    main_matrix = generateMatrix(tokens, row, column)
    sequences = generateSequence(tokens, max_sequence_size, sequence_count)
else:
    print("Command is not recognized, exiting program...")
    exit()

print("\n>>> BREACH PROTOCOL <<<")
Matrix.printMatrix(main_matrix)
print("")
printSequences(sequences)

print("\nBuffer size :", buffer_size)
print("Solving...")

# Solving algorithm
def isIn(row, column, stack):
# isIn function to detect wether a token is already selected or not
    if stack != []:
        for token in stack:
            if (token.x, token.y) == (column, row):
                return True
    return False

def searchSequence(matrix : Matrix, stack, row, column, buffer, solution, horizontal):
# Solution finding algorithm
    if buffer == 1:
        solution.append(list(stack))
        # Recursion basis
    else:
        if horizontal:
        # Horizontal (column) traversal
            for i in range(matrix.column):
                if not isIn(row, i, stack):
                    stack.append(matrix.content[row][i])
                    searchSequence(matrix, stack, row, i, buffer - 1, solution, False)
                    stack.pop()
        else:
        # Vertical (row) traversal
            for i in range(matrix.row):
                if not isIn(i, column, stack):
                    stack.append(matrix.content[i][column])
                    searchSequence(matrix, stack, i, column, buffer - 1, solution, True)
                    stack.pop()

# Main execution
horizontal = True
stack = []
solution = []
start = tm.time()
searchSequence(main_matrix, stack, 0, 0, buffer_size+1, solution, True)
a,b = getSolution(solution, sequences) # Retrieving results in tuple form
string ="" # To be saved string
end = tm.time()
if a != 0:
    print(a)
    string += str(a) + "\n"
    first = True
    for i in b:
        print(i.token, end=' ')
        if not first:
            string += " "+i.token
        else:
            string += i.token
            first = False
    print("")
    for i in b:
        print(str(i.x+1) + ", " + str(i.y+1))
        string += '\n' + str(i.x+1) + ", " + str(i.y+1)
else:
    print("No optimum solution found") 

print("")
print(int((end-start)*1000), "ms")
string += "\n\nRuntime : " + str(int((end-start)*1000)) + " ms"


inputn = input("Do you want to save the solution ? (y/n) : ")
inputn = inputn.lower()
if inputn == "y": # File saving mechanism, the solution is saved into the Solution folder
    if initiation != "n":
        save = open(save_path+"_"+initiation, 'w')
    else:
        file_name = input("Enter save file name : ")
        save = open(save_path+file_name, 'w')
    save.write(string)
    save.close()
    print("Thank you for using the program...")
elif inputn == "n":
    print("Thank you for using the program...")
else:
    print("Command is not recognized, exiting program...")