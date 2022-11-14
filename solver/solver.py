import numpy as np

numbers = {i for i in range(1, 10)}


class Solver:

    def __init__(self, board):
        self.sudoku = np.array(board, dtype=int)
        self.rows, self.cols = self.sudoku.shape
        self.zeroRows = []
        self.zeroRowsIndex = []
        self.zeroCols = []
        self.zeroColsIndex = []
        self.totalZeros = 0
        self.getInitialState()

    def getZeroCount(self, row):
        unique, counts = np.unique(row, return_counts=True)
        numDim = set(unique)
        numberZeros = 0
        indexes = []
        if 0 in numDim:
            numberZeros = counts[0]
            indexes = list(np.where(row == 0)[0])
            print(indexes)
        return numberZeros, indexes

    def getInitialState(self):

        print("Starting rows")
        for i in range(0, self.rows):
            row = self.sudoku[i, :]
            zeros, indexes = self.getZeroCount(row)
            self.zeroRows.append(zeros)
            self.zeroRowsIndex.append(list(indexes))
            self.totalZeros += zeros
        print("Starting Columns")
        for i in range(0, self.cols):
            row = self.sudoku[:, i]
            zeros, indexes = self.getZeroCount(row)
            self.zeroCols.append(zeros)
            self.zeroColsIndex.append(indexes)
            #self.totalZeros += zeros



    def solveRowCol(self, dimension: np.array, index: int, complementary: list, type: str = 'row') -> bool:
        options = numbers - set(dimension)

        sust = []
        sustitucion = False
        optionsDict = dict.fromkeys(options, None)
        for i in optionsDict.keys():
            optionsDict[i] = []

        for i in complementary:

            if(type == 'row'):
                col = set(self.sudoku[:, i])
            elif(type == 'col'):
                col = set(self.sudoku[i, :])

            aval = numbers - col
            inter = list(options.intersection(aval))

            if len(inter) == 1:
                sust.append((index, i, inter[0]))
            else:
                for j in inter:
                    optionsDict[j].append(i)

        if (len(sust) > 0):
            for j in sust:

                if (type == 'row'):
                    self.sudoku[j[0], j[1]] = j[2]
                    self.totalZeros -= 1
                    self.zeroColsIndex[j[1]].remove(j[0])
                elif (type == 'col'):
                    self.sudoku[j[1], j[0]] = j[2]
                    self.totalZeros -= 1
                    self.zeroRowsIndex[j[1]].remove(j[0])

                optionsDict.pop(j[2])
                complementary.remove(j[1])
                sustitucion = True

        for key, opt in optionsDict.items():
            if len(opt) == 1:
                if (type == 'row'):
                    self.sudoku[index, opt[0]] = key
                    self.totalZeros -= 1
                    self.zeroColsIndex[opt[0]].remove(index)


                elif (type == 'col'):
                    self.sudoku[opt[0], index] = key
                    self.totalZeros -= 1
                    self.zeroRowsIndex[opt[0]].remove(index)

                complementary.remove(opt[0])
                sustitucion = True

        #print(optionsDict)

        return sustitucion

    def solver(self):
        while (self.totalZeros > 0):
            print("Zeros: ", self.totalZeros)
            original = self.totalZeros
            print("Starting rows Analysis")

            for i in range(0, self.rows):
                row = self.sudoku[i, :]
                sus = self.solveRowCol(row, i, self.zeroRowsIndex[i])
            print(self.sudoku)

            print("Starting cols Analysis")
            for i in range(0, self.cols):
                row = self.sudoku[:, i]
                sus = self.solveRowCol(row, i, self.zeroColsIndex[i], type="col")
            print(self.sudoku)

            print("Zeros: ", self.totalZeros)
            if self.totalZeros == original:
                print("Salgo antes")
                break
