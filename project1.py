'''
A simple program for running simply assembly language 
Only a few type of instruction can be read
ADD ADDI SUB MUL DEV AND B BEQZ

'''


import os
import linecache    
print('Your input filie name:')
script_dir = os.path.dirname(__file__) 
file_name = input()
rel_path = file_name                               
abs_file_path = os.path.join(script_dir, rel_path)      #trans local file path to system path
line_count = len(open(abs_file_path ,'rU').readlines())


reg={'R0': 0,'R1': 0,'R2': 0,'R3': 0,'R4': 0,'R5': 0,'R6': 0,'R7': 0,'R8': 0,'R9': 0}  #init all register to 0 only R0~R9 can be use
PC = 1                                                  #Program Counter is base on input line number
tag={}                                                  #use for save tag and their PC
tag_review_done = 0                                     #use for tag review if finish =1
branch_seq = ['N','N']                                  #when branch taken add 'T' to this list else add 'N' for 2bit listory branch predictor use start from 2N
predict = []                                     #show the predict result
history_counter={'NN': 0,'NT': 0,'TN': 0,'TT': 0,}                               #use for 2bit history counter init state = 0 0 0 0(in dec) 
mispredict = 0


add_entry = 2
mul_entry = 2


def insCompiler(ins,iftag):                             #use for exe instruction
    global PC
    
    if iftag>0:      
        PC=PC+1
        return
    else:
        if ins[0] == 'ADD':
            reg[ins[1]] = reg[ins[2]] + reg[ins[3]]
            PC=PC+1
            return
        elif ins[0] == 'ADDI':
            reg[ins[1]] = reg[ins[2]] + int(ins[3])
            PC=PC+1
            return
        elif ins[0] == 'SUB':
            reg[ins[1]] = reg[ins[2]] - reg[ins[3]]
            PC=PC+1
            return
        elif ins[0] == 'MUL':
            reg[ins[1]] = reg[ins[2]] * reg[ins[3]]
            PC=PC+1
            return
        elif ins[0] == 'DIV':
            if(reg[ins[3]]==0):
                print('error!! dev by 0')
                return 1
            reg[ins[1]] = int(reg[ins[2]] / reg[ins[3]])
            PC=PC+1
            return
        elif ins[0] == 'AND':
            reg[ins[1]] = reg[ins[2]] & reg[ins[3]]
            PC=PC+1
            return
        elif ins[0] == 'B':
            PC = tag[ins[1]]
            branch_seq.extend('T')
            return
        elif ins[0] == 'BEQZ':
            if reg[ins[1]] == 0:
                PC = tag[ins[2]]
                branch_seq.extend('T')
            else:
                PC = PC + 1
                branch_seq.extend('N')
            return
        #BNE BGT BLT not finish
        elif ins[0] == 'BNE':
            PC = tag[ins[2]]
            return
        elif ins[0] == 'BGT':
            PC = tag[ins[2]]
            return
        elif ins[0] == 'BLT':
            PC = tag[ins[2]]
            return
        else:
            PC=PC+1
            return





def tagRecoder(ins,iftag):
    global PC
    global tag_review_done
    global line_count
    
    if iftag>0:      
        tag[ins[0]] = PC#iftag>0 means this instrunction is a tag
        
        return
    else:
        
        return

def twoBHP(seq):        #function for 2 bit history predictor
    global mispredict

    seq_num = len(seq)
    for i in range(seq_num-2):

        if branch_seq[i] == 'N' and branch_seq[i+1] == 'N' :

            if history_counter['NN'] <=1:

                predict.extend('N')
                if branch_seq[i+2] == predict[-1]:                      #if predict correct
                    history_counter['NN'] = history_counter['NN'] - 1
                    if history_counter['NN'] <= 0:                      
                        history_counter['NN'] = 0
                else:
                    mispredict = mispredict + 1
                    history_counter['NN'] = history_counter['NN'] + 1

            else:                                              
                predict.extend('T')
                if branch_seq[i+2] == predict[-1]:                      #if predict correct
                    history_counter['NN'] = history_counter['NN'] + 1
                    if history_counter['NN'] >= 3:
                        history_counter['NN'] = 3
                else:
                    mispredict = mispredict + 1
                    history_counter['NN'] = history_counter['NN'] - 1
                
            #NN
        elif branch_seq[i] == 'N' and branch_seq[i+1] == 'T' :
            if history_counter['NT'] <=1:

                predict.extend('N')
                if branch_seq[i+2] == predict[-1]:                      #if predict correct
                    history_counter['NT'] = history_counter['NT'] - 1
                    if history_counter['NT'] <= 0:                      
                        history_counter['NT'] = 0
                else:
                    mispredict = mispredict + 1
                    history_counter['NT'] = history_counter['NT'] + 1

            else:                                              
                predict.extend('T')
                if branch_seq[i+2] == predict[-1]:                      #if predict correct
                    history_counter['NT'] = history_counter['NT'] + 1
                    if history_counter['NT'] >= 3:
                        history_counter['NT'] = 3
                else:
                    mispredict = mispredict + 1
                    history_counter['NT'] = history_counter['NT'] - 1
                
            #TN
        elif branch_seq[i] == 'T' and branch_seq[i+1] == 'N' :
            if history_counter['TN'] <=1:

                predict.extend('N')
                if branch_seq[i+2] == predict[-1]:                      #if predict correct
                    history_counter['TN'] = history_counter['TN'] - 1
                    if history_counter['TN'] <= 0:                      
                        history_counter['TN'] = 0
                else:
                    mispredict = mispredict + 1
                    history_counter['TN'] = history_counter['TN'] + 1

            else:                                              
                predict.extend('T')
                if branch_seq[i+2] == predict[-1]:                      #if predict correct
                    history_counter['TN'] = history_counter['TN'] + 1
                    if history_counter['TN'] >= 3:
                        history_counter['TN'] = 3
                else:
                    mispredict = mispredict + 1
                    history_counter['TN'] = history_counter['TN'] - 1
                
            #NT
        else:
            if history_counter['TT'] <=1:

                predict.extend('N')
                if branch_seq[i+2] == predict[-1]:                      #if predict correct
                    history_counter['TT'] = history_counter['TT'] - 1
                    if history_counter['TT'] <= 0:                      
                        history_counter['TT'] = 0
                else:
                    mispredict = mispredict + 1
                    history_counter['TT'] = history_counter['TT'] + 1

            else:                                              
                predict.extend('T')
                if branch_seq[i+2] == predict[-1]:                      #if predict correct
                    history_counter['TT'] = history_counter['TT'] + 1
                    if history_counter['TT'] >= 3:
                        history_counter['TT'] = 3
                else:
                    mispredict = mispredict + 1
                    history_counter['TT'] = history_counter['TT'] - 1
                
            #TT
        '''
        print (branch_seq)
        print (predict)
        print (history_counter)
        print ()
        '''

end   = 0

#print (line_count)
while PC<=line_count:
    line  =  linecache .getline(abs_file_path, PC)  
    line=line.replace(","," ")
    iftag = line.count(':')
    line=line.replace(":"," ")
    #print (iftag, end='')
    

    if line.split():                                    #ingore space line
        pass
    else:
        PC=PC+1
        continue
    #print (PC, end='')
    line=line.split()
    
    if tag_review_done == 1:
        end = end + 1
        insCompiler(line,iftag)
        #print (end, end='')
        
        
    else:
        tagRecoder(line,iftag)
        #print (tag)
        if PC == line_count:
            tag_review_done = 1
            PC = 0
        PC=PC+1

    #print (line[0])
    
    if end>100:
        break
    #print (reg)

    
        

    
    
#show result

print ('register file resule = ',reg)
#print (tag)
print ('Branch sequence = \n',branch_seq[2:])
twoBHP(branch_seq)
print ('Predict Branch sequence = \n',predict)
print ('Final History Counter State = \n',history_counter)
print ('Mispredict Count = ',mispredict)
