README file for fixation simulation

How to fill excel sheet for data collection:

"Carrying Capacity (K)" represents the maximum number of individuals the population can hold. This is the number of individuals that the simulation starts at, and if it is exceeded, 
an individual is randomly killed until carrying capacity is restored. Input as an integer (e.g. 10000).

"Mutated Individuals at start" represents how many individuals carry the mutation at the start of the simulation. Input as an integer (e.g. 500).

"Chance of Reproduction (Wildtype)" represents how likely each individual with the wildtype allele is to reproduce. Input as a decimal (e.g. 0.5).

"Chance of Reproduction (Mutant)" represents how likely each individual with the mutant allele is to reproduce. Input as a decimal (e.g. 0.6). Value can also be lower than the wildtype reproduction if desired.

"Change in Mutant Survival Rate" represents any increase or decrease in the survival rate of mutant individuals when K is exceeded. An increase should be represented as a positive decimal (e.g. 0.2, representing a 20% increase in survival).
A decrease should be represented as a negative decimal (e.g. -0.2, representing a 20% decrease in survival). No change in survival should be represented with a 0.

"Number of Offspring (Mutant)" represents the probability distribution of different numbers of offspring for the mutated individuals. The field directly to the right of "Number of Offspring (Mutant)" should be left blank.
Rows can be added below as needed to allow for different ammounts of offspring, with the value in column "A" representing the number of offspring and the value in column "B" representing how likely it is to occur as a decimal. 
All decimals must sum to equal 1.
Example:
1	0.2
2	0.5
3	0.2
4	0.1

"Number of Offspring (Wildtype)" is the same as above, but refers to wildtype individuals. 

After filling the Excel document, save as .txt file named 'Variables' in your open directory.

Thanks for using my code!