2 Bit history Branch Predictor
=============
This is a simple program that can run simply instruction.Then it will show the result of input instruction.
And it can record branch and if it is taken.
Then give a predict sequence if we have 2bit history branch predictor.
But your inputs must have the same format as sample.

Instruction Sample
-------------

The sample file is *project1.txt*

The sample is a program that calculates the sum of num 1~10.

        INIT:
            ADDI R1,R1,10
            ADDI R4,R4,1
        Loop:
            BEQZ R1,Exit
            AND R2,R1,R4
            BEQZ R2,Even
            ADD R3,R3,R1

        Even:
            ADDI R1,R1,-1
            B Loop
        Exit:

1.  Only a few instruction can be read in this program.

* ADD 
* ADDI
* SUB
* MUL
* DIV
* AND
* B
* BEQZ

2.  If you want to use tag for branch, you need to add ":" at the end of the tag.
3.  Every register in instruction need to be separated by ","
4.  Only R0~R9 can be use, and they are be set as 0.

Giving an input
-----------------------------
You have to put your input file in the same folder with this program.And you have to type full file name at beginning.


Result
------------------------
This is the result of sample input.


    register file resule =  {'R0': 0, 'R1': 0, 'R2': 1, 'R3': 25, 'R4': 1, 'R5': 0, 'R6': 0, 'R7': 0, 'R8': 0, 'R9': 0}
    Branch sequence =
    ['N', 'T', 'T', 'N', 'N', 'T', 'N', 'T', 'T', 'N', 'N', 'T', 'N', 'T', 'T', 'N', 'N', 'T', 'N', 'T', 'T', 'N', 'N', 'T', 'N', 'T', 'T', 'N', 'N', 'T', 'T']
    Predict Branch sequence =
    ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'T', 'N', 'N', 'N', 'N', 'N', 'T', 'N', 'N', 'N', 'N', 'N', 'T', 'N', 'N', 'N', 'N', 'N', 'T', 'N']
    Final History Counter State =
    {'NN': 3, 'NT': 2, 'TN': 0, 'TT': 0}
    Mispredict Count =  12
