# -*- coding: utf-8 -*-
"""
Created on Wed May 11 03:39:39 2022

@author: Abdul
Simulation Outputs:
    This code outputs 2 files
    'Number_of_Mutants.txt' is a text file that contains information on the number of mutants per generation. This is recored for the first fixation/elimination and the overall mean.
    'Generations_until_Fixation_or_Elimination.txt' is a text file that stores information on how many generations it takes to reach fixation/elimination in each simulation.

Assumptions:
    1) Individuals reproduce asexually
    2) Each individual has a set chance to reproduce
    3) Each mutated individual creates the same range of offspring at the same probabilities. Same applies to wildtype individuals.
    4) If population (N) exceeds carrying capacity (K), random individuals die until N=K before next reproductive event
    5) All individuals reproduce at the same time
    6) Individuals are semelparous
    7) Populations start at carrying capacity 
    8) Mutation can affect: chance of reproduction, number of offspring, survival of offspring
    9) No mutations occur after the simulation begins
    10) No stochastic events affect the population's dynamics
    11) The environment (and thus the fitness gain / loss from the mutation) is constant

"""
#Establishing Variables
import random

with open("Variables.txt","r") as f:
    lines = f.read()

#Splitting the string into list
lines=lines.replace("\n","\t")                              #Sets up easier split
lines=lines.split('Number of Offspring (Wildtype)')         #Isolates the different offspring values for wildtype
lines2=lines[0].split('Number of Offspring (Mutant)')       #Isolates the different offspring values for mutant

MutantReproduction=lines2[1]                                #Assigns a variable to the string containing the mutant offspring values
MutantReproduction=MutantReproduction.split("\t")           #Converts from string to list and splits values         

#Deletes the blank fields in MutantReproduction
j=0
for i in range(len(MutantReproduction)):
    
    if MutantReproduction[j] == '':
        del MutantReproduction[j]
    elif MutantReproduction[j] == '-':
        del MutantReproduction[j]
    else:
        j += 1




WildReproduction=lines[1]                                   #Assigns a variable to the string containing the wildtype offspring values
WildReproduction=WildReproduction.split("\t")               #Converts from string to list and splits values

#Deletes the blank fields in WildReproduction
j=0
for i in range(len(WildReproduction)):
    
    if WildReproduction[j] == '':
        del WildReproduction[j]
    elif WildReproduction[j] == '-':
        del WildReproduction[j]
    else:
        j += 1

#Assigning variables for later use, tracking how many times the mutation reaches fixation, is eliminated, or persists
Fixation=0
Elimination=0
Persists=0



RefinedVariables=lines2[0]                                  #Assigns a variable to the string containing the other variables
RefinedVariables=RefinedVariables.split('\t')               #Splits the string into a list
K = int(RefinedVariables[1])                              #Extracts and assigns the value of carrying capacity
MStart = int(RefinedVariables[3])                         #Extracts and assigns the value of individuals carrying mutation at generation 0
WildTypeReproductiveRate = float(RefinedVariables[5])       #Extracts and assigns the value for wildtype reproductive chance
MutantReproductiveRate = float(RefinedVariables[7])         #Extracts and assigns the value for mutant reproductive chance
SurvivalModifier = float(RefinedVariables[9])

#Creating dictionary for mutant offspring values
MutantReproductionDict=[]
#Filling dictionary for mutant offspring values
j=0
for i in range (len(MutantReproduction)):
    if j+1 < len(MutantReproduction):
        MutantReproductionDict.append([float(MutantReproduction[j]), float(MutantReproduction[j+1])])
        j += 2
        
        
        
#Creating dictionary for Wildtype offspring values
WildReproductionDict=[]
#Filling dictionary for Wildtype offspring values
j=0
for i in range (len(WildReproduction)):
    if j+1 < len(WildReproduction):
        WildReproductionDict.append([float(WildReproduction[j]), float(WildReproduction[j+1])])
        j += 2


#Block of text relaying the inputs back to the reader
print(f"The chance of a wildtype individual reproducing is {WildTypeReproductiveRate*100}%.")
print(f"The chance of a mutated individual reproducing is {MutantReproductiveRate*100}%.")
print(f"The population carrying capacity (and thus the size of the starting population) is {K}.")
print(f"{MStart} individuals start with the mutation.")

GenerationCap=int(input("Maximum number of generations in simulation (failsafe against infinate loops): "))
NLoops=int(input("Number of times you want to run the simulation: "))

print("\nRunning Simulation......\n")

MeanMutatedDict = []    #Dictionary used to calculate the mean number of individuals mutated each generation
FixationDict = []       #Dictionary used to store how many generations it took to reach fixation
EliminationDict = []      #Dictionary used to store how many generations it took to be eliminated
FirstSimDict = []       #Dictionary used to store information on the first fixation and elimination, might trim for higher efficiency

#Code used to create the empty dictionaries. In all dictionaries, i refers to the generation
if GenerationCap < 10000:
    for i in range (GenerationCap):
        FixationDict.append([0,i])
        EliminationDict.append([0,i])
        MeanMutatedDict.append([0,0,0,i])   #[Sum, Repeats, mean]
        FirstSimDict.append([0,0,i])  #Number of mutants per generation for the first elimination and fixation ([Fixation, Elimination])
else:
    for i in range (10000):
        FixationDict.append([0,i])
        EliminationDict.append([0,i])
        MeanMutatedDict.append([0,0,0,i])  #[Sum, Repeats, Mean]
        FirstSimDict.append([0,0,i])  #Number of mutants per generation for the first elimination and fixation ([Fixation, Elimination])

for p in range (0,NLoops):              #Loops the simulation based on user input
    Generation=0        #Tracks the generation
    M=int(MStart)            #Tracks number of individuals with mutation
    NextGenM=0          #Tracks number of offspring with mutation
    W=int(K-MStart)          #Tracks number of individuals without mutation
    NextGenW=0          #Tracks number of offspring without mutation

    
    while M != 0 and M != K and M + W != 0:       #Continues loop if mutation has not either reached fixation or been eliminated
        #Information added to dictionaries    
        MeanMutatedDict[Generation][0] += M     #Number of mutants that generation is stored to calculate mean
        MeanMutatedDict[Generation][1] += 1     #Number of simulations that reached this generation is stored to calculate mean
        if Fixation == 0:                       #If this is the first fixation simulation that occurs, information is stored. Isn't stored after 1st to increase efficiency
            FirstSimDict[Generation][0] = M
        if Elimination == 0:                    #If this is the first fixation simulation that occurs, information is stored. Isn't stored after 1st to increase efficiency
            FirstSimDict[Generation][1] = M
        #Simulates reproduction of mutated individuals
        for i in range (0,M):
            ReproductionCheckM=random.uniform(0,1)          #Generates random number to see if reproduction occurs
            if ReproductionCheckM <= MutantReproductiveRate:        #Reproduction occurs if random number is larger or equal to probability of reproduction
                SumChanceM=0                                         #Variable used to determine how many offspring are produced
                OffspringCheckM = random.uniform(0,1)               #Generates random number to see how many offspring are produced
                
                #Goes through the dictionary that stores offspring values, and decides how many offspring are made based on the number generated
                for l in range (len(MutantReproductionDict)):       
                    if OffspringCheckM <= MutantReproductionDict[l][1] + SumChanceM:     #Successful roll, number of offspring determined
                        NextGenM += MutantReproductionDict[l][0]
                    elif OffspringCheckM > MutantReproductionDict[l][1] + SumChanceM:        #Failed roll, next number checked
                        SumChanceM += MutantReproductionDict[l][1]
                    else: 
                        print("error 02")           #Error code
                
        
        #Simulates reproduction of wildtype individuals
        for i in range (0,W):
            ReproductionCheckW=random.uniform(0,1)
            if ReproductionCheckW <= WildTypeReproductiveRate:        #Reproduction occurs if random number is larger or equal to probability of reproduction
                SumChanceW=0                                         #Variable used to determine how many offspring are produced
                OffspringCheckW = random.uniform(0,1)               #Generates random number to see how many offspring are produced
                
                #Goes through the dictionary that stores offspring values, and decides how many offspring are made based on the number generated
                for l in range (len(WildReproductionDict)):       
                    if OffspringCheckW <= WildReproductionDict[l][1] + SumChanceW:     #Successful roll, number of offspring determined
                        NextGenW += WildReproductionDict[l][0]
                    elif OffspringCheckW > WildReproductionDict[l][1] + SumChanceW:        #Failed roll, next number checked
                        SumChanceW += WildReproductionDict[l][1]
                    else: 
                        print("error 03")           #Error code
                
                
    
        TotalNextGen = int(NextGenW+NextGenM)      #Tracks how many individuals in new generation
        if TotalNextGen > K:                  #Tests to see if population is above carrying capacity 
            for i in range (0,(TotalNextGen-K)):        #Loops code until carrying capacity isn't exceeded, removing an individual randomly each time
                EffectiveNextGenM = NextGenM * (1-SurvivalModifier)             #Used to calculate the chance of a mutated individual being selected (EffectiveNextGenM / EffectiveNextGenM + NextGenW)   
                RandomIndividual = random.uniform(1,(NextGenW+EffectiveNextGenM))        #Generates a random number corresponding to an individual
                if RandomIndividual <= EffectiveNextGenM:                                #Random individual chosen has mutation, and is "removed"
                    NextGenM -= 1
                elif RandomIndividual > EffectiveNextGenM:                                 #Random individual chosen is wildtype, and is "removed"
                    NextGenW -= 1
                else:
                    print("Error 01")       #Error code
        
        #New values set for next generation, and generation counter increases by 1            
        M = int(NextGenM)    
        W = int(NextGenW)
        NextGenM=0  #2 lines to reset the value of next gen, ready for next cycle
        NextGenW=0
        Generation += 1
        if Generation >= GenerationCap:  #Failsafe to make sure my computer doesn't explode
            break
    
    if M >= K:      #If mutation reaches fixation
        Fixation += 1   #Tracks how often it reaches fixation
        FixationDict[Generation][0] += 1    #Tracks how many generations it takes to reach fixation
    
    elif M <= 0:    #If mutation is eliminated
        Elimination += 1    #Tracks how often it is eliminated
        EliminationDict[Generation][0] += 1     #Tracks how many generations it takes to become eliminated
    
    else:       #If mutation is neither eliminated or fixed
        Persists += 1   #Tracks how often it persists without fixation

#Code used to calculate the mean generations until fixation
FixationSum = 0
FixationMean =0
for i in range (len(FixationDict)):
    if FixationDict[i][0] != 0:
        FixationSum += i*EliminationDict[i][0]
if Fixation != 0:
    FixationMean = FixationSum/Fixation


#Code used to calculate the mean generations until Elimination
EliminationSum = 0
EliminationMean = 0
for i in range (len(EliminationDict)):
    if EliminationDict[i][0] != 0:
        EliminationSum += i*EliminationDict[i][0]
if Elimination != 0:
    EliminationMean = EliminationSum/Elimination
    


if Fixation == 0:           #Removes information from dictionaries if there is no fixation event
    for i in range (len(FirstSimDict)):
        FirstSimDict[i][0] = 'N/A'
        FixationDict[i][0] = 'N/A'


if Elimination == 0:           #Removes information from dictionaries if there is no elimination event
    for i in range (len(FirstSimDict)):
        FirstSimDict[i][1] = 'N/A'
        EliminationDict[i][0] = 'N/A'



if NLoops == 1:       #Output if only 1 simulation is ran
    if M == K:              #Mutation reaches fixation
        print(f"After {Generation} generations, the mutation reached fixation.")
        
    elif M == 0:              #Mutation is eliminated from the population
        print(f"After {Generation} generations, the mutation is eliminated from the population.")
        
    else:
        print(f"After {Generation} generations, {M} individuals carried the mutation, while {W} individuals carried the wildtype allele.")

else:               #Output if multiple simulations are ran
    print(f"The mutation reached fixation in {Fixation} of the {NLoops} simulations.")
    if Fixation != 0:
        print(f"The mutation reached fixation in a mean number of {FixationMean} generations.")
    print(f"The mutation was eliminated in {Elimination} of the {NLoops} simulations.")
    if Elimination != 0:
        print(f"The mutation was eliminated in a mean number of {EliminationMean} generations.")
    print(f"The mutation persisted without reaching fixation in {Fixation} of the {NLoops} simulations.")

#Code used to calculate mean mutated individuals per generation
for i in range (len(MeanMutatedDict)):
    if MeanMutatedDict[i][1] != 0:
        MeanMutatedDict[i][2] = MeanMutatedDict[i][0]/MeanMutatedDict[i][1]
    
    
#Code used to export information on the number of mutants per generation
outfile=open('Number_of_Mutatants.txt','w')
outfile.write("Generation"+'\t'+'First Fixation'+'\t'+'First Elimination'+'\t'+'Mean'+'\n')
for i in range (len(FirstSimDict)):
    outfile.write(str(i)+'\t'+str(FirstSimDict[i][0])+'\t'+str(FirstSimDict[i][1])+'\t'+str(MeanMutatedDict[i][2])+'\n')
outfile.close()

#Code used to store information on how many generations it takes to reach fixation/elimination
outfile=open('Generations_until_Fixation_or_Elimination.txt','w')
outfile.write("Generation"+'\t'+'Fixations'+'\t'+'Eliminations'+'\n')
for i in range(len(FixationDict)):
    if FixationDict[i][0] != 0 and FixationDict[i][0] != 'N/A' or EliminationDict[i][0] != 0 and EliminationDict[i][0] != 'N/A':
        outfile.write(str(i)+'\t'+str(FixationDict[i][0])+'\t'+str(EliminationDict[i][0])+'\n')
outfile.close()
