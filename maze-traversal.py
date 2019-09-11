#Name: Surachan Liaowongphuthorn
#Picobot project
#04/30/2018
import random
from functools import reduce

SURROUNDING = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']
HEIGHT = 25
WIDTH = 25
NUMSTATES = 5
class Program(object):
    def __init__(self):
        self.rules = {}
        
    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        Keys = list(self.rules.keys())
        sortedKeys = sorted(Keys)    
        s = ''
        for i in range(len(sortedKeys)):
            s = s+str(sortedKeys[i][0])+' '+sortedKeys[i][1]+" -> "+self.rules[sortedKeys[i]][0]+' '+str(self.rules[sortedKeys[i]][1])+"\n" 
            
        #0 NExx -> W 2
        return s

    def __gt__(self, other):
        """Greater-than operator -- works randomly, but works!"""
        return random.choice([True, False])

    def __lt__(self, other):
        """Less-than operator -- works randomly, but works!"""
        return random.choice([True, False])

    def randomize(self):
        #self.rules[(0, "xExx")] = ("N", 1)
        POSSIBLE_MOVES = ['N','W','E','S']
        for i in range(NUMSTATES):
            for j in range(9):
                pattern = SURROUNDING[j]
                movedir = random.choice(POSSIBLE_MOVES)
                while movedir in pattern:
                    movedir = random.choice(POSSIBLE_MOVES)
                #print(pattern,' ',movedir,' ')
                self.rules[(i, pattern)] = (movedir,random.choice(range(1,NUMSTATES)))
                #print(self.rules[(i, pattern)])
    def getMove(self, state, surroundings):
        return self.rules[(state, surroundings)]

    def mutate(self):
        """
            change one rule of the of the program
            accept one program 
            return one program
        """
        Keys = list(self.rules.keys())
        #print(Keys)
        mutant = Keys[random.choice(range(len(Keys)))]
        
        newState = []
        for i in range(NUMSTATES):
            if i != mutant[0]:
                newState += [i]

        move = []
        if mutant[1][0] == 'x':
            move += ["N"]
        if mutant[1][1] == 'x':
            move += ["E"]
        if mutant[1][2] == 'x':
            move += ["W"]
        if mutant[1][3] == 'x':
            move += ["S"]

        #print(mutant)
        return (random.choice(move), random.choice(newState))
    def crossover(self, other):
        """
            crossover two programs at a randon state
            accept twp program
            return one program
        """

        crossState = random.choice([1,2,3]) # 0,1,2, crossoverState(from self), crossoverState+1, CS+2, ..., end(from other)
        
        Keys = list(self.rules.keys())
        #print('Keys',self)
        offSpring = {}
        for i in range(len(Keys)):
            if Keys[i][0] <= crossState:
                x = self.rules[Keys[i]]
                offSpring[Keys[i]] = x
        
        Keys2 = list(other.rules.keys())
        #print('Keys2',other)
        for j in range(len(Keys2)):       
            if Keys2[j][0] > crossState:
                x = self.rules[Keys2[j]]
                offSpring[Keys2[j]] = x
        #print(offSpring)
        return offSpring


    def working(self):
        """
        This method will set the current program (self) to a working
        room-clearing program. This is super-useful to make sure that
        methods such as step, run, and evaluateFitness are working!
        """
        POSSIBLE_SURROUNDINGS = ["NExx", "NxWx", "Nxxx", "xExS",
         "xExx", "xxWS", "xxWx", "xxxS", "xxxx"]
        POSSIBLE_MOVES = ['N', 'E', 'W', 'S']
        POSSIBLE_STATES = [0, 1, 2, 3, 4]
        for st in POSSIBLE_STATES:
            for surr in POSSIBLE_SURROUNDINGS:
                if st == 0 and ('N' not in surr):   val = ('N', 0)
                elif st == 0 and ('W' in surr):     val = ('E', 2)
                elif st == 0:                       val = ('W', 1)
                elif st == 1 and ('S' not in surr): val = ('S', 1)
                elif st == 1 and ('W' in surr):     val = ('E', 2)
                elif st == 1:                       val = ('W', 0)
                elif st == 2 and ('E' not in surr): val = ('E', 2)
                elif st == 2 and ('N' in surr):     val = ('S', 1)
                elif st == 2:                       val = ('N', 0)
                else:
                    stepdir = surr[0]
                    while stepdir in surr:
                        stepdir = random.choice(POSSIBLE_MOVES)
                    val = (stepdir, st)  # keep the same state
                self.rules[(st, surr)] = val


        
class World(object):
    def __init__(self, initial_row, initial_col, program):
        self.prow = initial_row+1
        self.pcol = initial_col+1
        self.state = 0
        self.prog = program
        self.room = [[' ']*(WIDTH+2) for row in range(HEIGHT+2)]
        for col in range(WIDTH+2):
                if col != 0:
                    self.room[0][col] = str((col-1)%10)
              #self.room[0][col] = 'W'

        for row in range(1, HEIGHT+2):
            self.room[row][0] = str((row-1)%10)
            #self.room[row][0] = 'W'
            for col in range(1, WIDTH+2):
                self.room[row][col] = ' '
            self.room[row][col] = 'W'

        for col in range(WIDTH+2):
              self.room[row][col] = 'W'

        self.room[self.prow][self.pcol] = 'P'
    
    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''
        for row in range(0, HEIGHT+2):
            for col in range(0, WIDTH+2):
                s+=self.room[row][col]+' '
            s+= '\n'
        return s       # the board is complete, return it
    
    def getCurrentSurroundings(self):
        s = ['x','x','x','x']
        if not self.room[self.prow-1][self.pcol] in [' ','O','P']:
            s[0] = 'N'
        if not self.room[self.prow][self.pcol+1] in [' ','O','P']:
            s[1] = 'E'
        if not self.room[self.prow][self.pcol-1] in [' ','O','P']: 
            s[2] = 'W'
        if not self.room[self.prow+1][self.pcol] in [' ','O','P']: 
            s[3] = 'S'
        
        return reduce((lambda x, y: x + y),s)
    
    def step(self):
        #print('fsdfds',self.state,self.getCurrentSurroundings())
        move = self.prog.getMove(self.state, self.getCurrentSurroundings())
        #print('move',move)
        self.state = move[1]
        self.room[self.prow][self.pcol] = 'O'
        if move[0] == 'N':
            self.prow = self.prow-1
        elif move[0] == 'E':
            self.pcol = self.pcol+1
        elif move[0] == 'W':
            self.pcol = self.pcol-1
        else:
            self.prow = self.prow+1
        self.room[self.prow][self.pcol] = 'P'
    
    def run(self, steps):
        for i in range(steps):
            self.step()
    
    def fractionVisitedCells(self):
        visited = 0.0
        for row in range(1, HEIGHT+1):
            for col in range(1, WIDTH+1):
                if self.room[row][col] != ' ':
                    #self.room[row][col] = 'K'
                    visited += 1
        return visited/(HEIGHT*WIDTH)
                

def evaluateFitness(program, trials, steps):
    average = 0
    for i in range(trials):
        sample = World(random.choice(range(22)),random.choice(range(22)),program)
        sample.run(steps)
        average += sample.fractionVisitedCells()
    return average/trials

def saveToFile(filename, p):
   """Saves the data from Program p
           to a file named filename."""
   f = open(filename, "w")
   print(p, file = f)        # prints Picobot program from __repr__
   f.close()

#    # here's how to call this... probably within GA's main loop...
#    saveToFile("gen1.txt", best_p_in_gen_1)
#    saveToFile("gen2.txt", best_p_in_gen_2) # and so on...

def GA(popsize, numgens):
    L = []
    record = []
    Answer = []
    #create numgens generations of bestfit program 
    for i in range(numgens):
        average = 0
        if i == 0: #generate parents
            for j in range(popsize):
                program = Program()
                program.randomize()
                fitness = evaluateFitness(program, 10, 800)
                L += [[fitness,program]]
                average += fitness
        else: #crossing over parents and mutate generating children using 10% of popsize
            parent = SL[:int((popsize*10/100))]
            L = [a for a in parent]
            for k in range(popsize-len(parent)):
                x = random.choice(parent)
                #x = parent[0]
                dad = x[1]

                y = random.choice(parent)
                #count = 0
                # while y[0] == x[0] or count > 5:
                #     count+=1
                #     y = random.choice(parent)
                mom = y[1]

                mom.crossover(dad)
                # dad.crossover(x[1])
                # fitnessMom = evaluateFitness(mom, 20, 800)
                # fitnessDad = evaluateFitness(dad, 20, 800)
                
                # if fitnessMom > fitnessDad:
                #     child = mom
                #     fitness = fitnessMom
                # else:
                #     child = dad
                #     fitness = fitnessDad
                child = mom
                #fitness = evaluateFitness(child, 20, 800)
                if random.choice(range(100))>30:
                    #for l in range((i)%10+5):
                    child.mutate()
                    #fitness = evaluateFitness(child, 20, 800)
                fitness = evaluateFitness(child, 10, 800)
                L += [[fitness,child]]
                average += fitness

        SL = sorted(L)
        SL = SL[::-1]
        Answer += [[SL[0][0]],SL[0][1]]
        print("Fitness is measured using 20 random trials and running for 800 steps per trial:")
        print("Generation ",i)
        print("Average fitness:  ", average/popsize)
        print("Best fitness:  ", SL[0][0]) 

    saveToFile("BestPico.txt", Answer)
    return Answer





# a = Program()
# a.randomize()
# b = Program()
# b.randomize()
# c = World(5,5,a)