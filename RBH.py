#!/usr/bin/env python

# Test files: 
# zfile = "ZFish_temp"
# hfile = "Human_temp"

# Real input files:
zfile = "ZFish_against_Human_sorted"
hfile = "Human_against_ZFish_sorted"

# create data structure : [[ZFishID, Protein ID, E-value], [ZFishID, HProID, E-value]]
    # [['ENSDARP00000000004', 'ENSP00000417654', '1e-162'], ['ENSDARP00000000004', 'ENSP00000359172', '1e-20'], ['ENSDARP00000000004', 'ENSP00000416002', '6e-11'], ['ENSDARP00000000004', 'ENSP00000492745', '1e-10'], ['ENSDARP00000000004', 'ENSP00000358565', '5e-10'], ['ENSDARP00000000005', 'ENSP00000206423', '0.0'], ['ENSDARP00000000005', 'ENSP00000362095', '1e-11'], ['ENSDARP00000000005', 'ENSP00000362095', '6e-11'], ['ENSDARP00000000005', 'ENSP00000367794', '5e-10'], ['ENSDARP00000000005', 'ENSP00000362095', '3e-07'], ['ENSDARP00000000005', 'ENSP00000367794', '4e-07']]
n = 0
with open(zfile, "r") as zfh: # open the zebrafish_against_human file
    File_array = [] # create an empty array (GLOBAL variable) that will store all the records [[ZFishID, ProteinID, and E-value], ...]
    for line in zfh: # read is implicit
        record_array = [] # creates an array that will hold local variable 
        n += 1
        line_array = line.split() # split the lines on empty space (tabs)
        ZPro_ID = line_array[0] # grabs the ZProID and stores it as a local variable
        HPro_ID = line_array[1] # grabs the HProID and stores it as a local variable
        E_val = line_array[10] # grabs the E-value and stores it as a local variable
        record_array.append(ZPro_ID) # appends the ZProID to the local array 
        record_array.append(HPro_ID) # appends the HProID to the local array
        record_array.append(E_val) # appends the E value to the local array
        File_array.append(record_array) # appends the local array to the global array so it can be used outside the for loop

ZFish_dict = {} # creates a dictionary that will store {ZFish: Best_Hro_Match}
Candidate_best_ZPro_ID = File_array[0][0] # sets the ZProID in the first item in the File_array as the candidate best hit ZPro_ID
Candidate_best_HPro_ID = File_array[0][1] # sets the HProID in the first item in the File_array as the candidate best hit HPro_ID
Candidate_best_eval = File_array[0][2] # set the E-value in the first item in the File_array as the candidadate best e-value
Candidate_best_is_good = True # assume that the item can be kept and stored until proven otherwise
entry = 1 # start the for loop at the second item in the array. The first item is already stored in Candidate.
# Logic for finding unique best hits: 
    # Loop through the array and look for transitions to a new ZProID. When you find a new one:
        # Look back to see if the first (Candidate) ZProID had a lower eval. If yes, write it to the dict.
        # If there were multiple entries with same eval, don't write it to the dict.
            # Cases:
                # Case 1: multiple instances of same ZProID, only one best hit -> write to dict
                # Case 2: muttiple instanes of same ZProID, more than one with same eval -> don't write to dict
                # Case 3: only one instance of ZProID -> write to dict

while entry < len(File_array): # for every entry in the File_array
    Current_ZPro_ID = File_array[entry][0] # set the ZProID of the entry you're on as the Current_ZPro_ID
    Current_HPro_ID = File_array[entry][1] # set the HProID of the entry you're on as the Current_HPro_ID
    Current_eval = File_array[entry][2] # set the E-value of the entry you're on as the Current_eval
    # this block deals with instances where there are multiple hits, but only one best hit
    if Current_ZPro_ID == Candidate_best_ZPro_ID: # if the ZProID of the entry you're on is the same as the first one (candidate)
        if (Current_eval == Candidate_best_eval): # and the e-value is the same (Case 2 (duplicate ZproID/ evals)) move onto entry + 1
            Candidate_best_is_good = False # switch Candidate best to False.

    else: # Case 1 or Case 3, no duplicate (ZproID/ evals)
        if Candidate_best_is_good == True: # if on the next entry you see that the e-value is changed, set Candidate_best_is_good back to true and store the Candidate_best_ZproID.
            ZFish_dict[Candidate_best_ZPro_ID] = Candidate_best_HPro_ID
    # now take this item and make it the new Candidate
        Candidate_best_ZPro_ID = Current_ZPro_ID # Make the current record the candidate best
        Candidate_best_HPro_ID = Current_HPro_ID 
        Candidate_best_eval  = Current_eval
        Candidate_best_is_good = True

    entry += 1     

    # special case: last line of the file
    if (entry == len(File_array)): 
        if Candidate_best_is_good == True:
            ZFish_dict[Candidate_best_ZPro_ID] = Candidate_best_HPro_ID

print(len(ZFish_dict))        

h = 0
with open(hfile, "r") as hfh:
    Human_file_array = [] # create an empty array (GLOBAL variable) that will store all the records [[HProID, ZProID, and E-value], ...]
    for line in hfh: # read is implicit
        record_array = [] # creates an array that will hold local variables  
        h += 1
        line_array = line.split() # split the lines on empty space (tabs)
        ZPro_ID = line_array[1] # grabs the ZProID and stores it as a local variable
        HPro_ID = line_array[0] # grabs the HProID and stores it as a local variable
        E_val = line_array[10] # grabs the E-value and stores it as a local variable
        record_array.append(HPro_ID) # make the first item in the local array the HProID
        record_array.append(ZPro_ID) # make the second item in the local array the ZProID
        record_array.append(E_val) # make the third item int he local array the E-Value
        Human_file_array.append(record_array) # append the local array to the global array

Human_dict = {} # create an empty dictionary. This dictionary will store { HProID: Best_ZFish_Hit} 
Candidate_best_HPro_ID = Human_file_array[0][0] # set the first HProID of the first item in Human_file_array be the Candidate_best_HProID
Candidate_best_ZPro_ID = Human_file_array[0][1] # set the first ZProID of the first item in Human_file_array be the Candidate_best_ZProID
Candidate_best_eval = Human_file_array[0][2] # set the first e-value of the first item in Human_file_array be the Candidate_best_eval
Candidate_human_best_is_good = True # assume that the item can be kept and stored until proven otherwise

human_entry = 1 # start the for loop at the second item in the array. The first item is already stored in Candidate.

while human_entry < len(Human_file_array): 
    Current_HPro_ID = Human_file_array[human_entry][0] # set the HProID of the item you're on as the Current_HPro_ID
    Current_ZPro_ID = Human_file_array[human_entry][1] # set the ZProID of the item you're on as the Current_ZPro_ID
    Current_eval = Human_file_array[human_entry][2] # set the eval of the item you're on as the Current_eval
    # this block deals with instances where there are multiple hits, but only one best hit
    if Current_HPro_ID == Candidate_best_HPro_ID:
        if (Current_eval == Candidate_best_eval): # Case 2 (duplicate ZproID/ evals)
            Candidate_human_best_is_good = False # set the logical statement to False (so nothing can be stored) and increment by 1. The logical statement will stay false until a new HProID is encountered and the hit after it (if still on the same HPro) is proven to have a different e-value. 

    else: # Case 1 or Case 3, no duplicate (ZproID/ evals)
        if Candidate_human_best_is_good == True: 
            Human_dict[Candidate_best_HPro_ID] = Candidate_best_ZPro_ID # store Candidate_best_HPro_ID (the previous record) and its best hit in the dictionary
    # now take this item and make it the new Candidate
        Candidate_best_HPro_ID = Current_HPro_ID # make the current record the Candidate_best
        Candidate_best_ZPro_ID = Current_ZPro_ID 
        Candidate_best_eval  = Current_eval
        Candidate_human_best_is_good = True

    human_entry += 1     

    # special case: last line of the file
    if (human_entry == len(Human_file_array)):
        if Candidate_human_best_is_good == True:
            Human_dict[Candidate_best_HPro_ID] = Candidate_best_ZPro_ID
print(len(Human_dict))


RBH = [] # create an empty array which will hold the reciprocal best hits
# if the value of the Human dictionary matches the key of the ZFish dictionary 
for Zkey in ZFish_dict:
    for Hkey in Human_dict:
        if Zkey == Human_dict[Hkey] and Hkey == ZFish_dict[Zkey]:
            ZFish_Human_pair = []
            ZFish_Human_pair.append(Zkey)
            ZFish_Human_pair.append(Hkey)
            RBH.append(ZFish_Human_pair)

#print(RBH)
        
# Human Gene ID, Human Protein ID, Human Gene Name, Zebrafish Gene ID, Zebrafish Protein ID, Zebrafish Gene Name
# You may want to use your Biomart output from part 1.2 to look up gene names and IDs. These are also provided by Leslie in the same folder on talapas.

# Human Gene ID: in the Human_against_ZFish_sorted file, column 1
# Human Gene Name: in the BioMart output from part 1.2    
# Gene stable ID: column 1
# Gene name: column 3
    
ZFish_biomart = open("ensembl_zebrafish.txt", "r")		# open the ensembl chart file
ZFish_all_lines = ZFish_biomart.read()		# read it into a single line
chart_record_array = ZFish_all_lines.split('\n')	# split that line on the \n characters to make a list, each record is an item in that array
ln_count = 0		
ZFish_biomart_list = []					# set a counter to 0
for line in chart_record_array:
    ln_count += 1			# for each record increment the counter by 1
    chart_rec_line_array = line.split('\t') 	# split the record on tab so each record is now a list with GSID, PSID, gene name
    ZFish_biomart_list.append(chart_rec_line_array) # append Chart_rec_line_array to the global list ZFish_biomart_list

Human_biomart = open("ensembl_human", "r")		# open the ensembl chart file
Human_all_lines = Human_biomart.read()		# read it into a single line
Human_chart_record_array = Human_all_lines.split('\n')	# split that line on the \n characters to make a list, each record is an item in that array
hln_count = 0		
Human_biomart_list = []					# set a counter to 0
for line in Human_chart_record_array:
    hln_count += 1			
    human_chart_rec_line_array = line.split('\t') # split the line on the empty space . Chart_rec_line_array = [GSID, PSID, gene name]
    Human_biomart_list.append(human_chart_rec_line_array) # append Chart_rec_line_array to the global list ZFish_biomart_list

All_items_record = []
for record in RBH:
    current_record = []
    for Hitem in Human_biomart_list:
        if len(Hitem) == 3:
            if record[1] == Hitem[1]: # if the Human Protein ID in the RBH matches the Human protein ID in the biomart outpue
                current_record.append(record[1]) # append the Human Protein ID
                current_record.append(Hitem[0])    # append the Human Gene Stable ID
                current_record.append(Hitem[2])  # append the Human Gene Name             
                # All_items_record.append(current_record)
    for Zitem in ZFish_biomart_list:
        if len(Zitem) == 3:
            if record[0] == Zitem[1]: # if the ZFish Protein ID in the RBH array matches the ZFish Protein ID in the biomart array
                current_record.append(record[0]) # append the ZFish Protein ID
                current_record.append(Zitem[0])    # append the ZFish Gene Stable ID
                current_record.append(Zitem[2])  # append the gene name              
    All_items_record.append(current_record)
print(All_items_record)
#Human Gene ID, Human Protein ID, Human Gene Name, Zebrafish Gene ID, Zebrafish Protein ID, Zebrafish Gene Name] 

with open("Human_Zebrafish_RBH.tsv", "wt") as RBH_tsv:   
    for i in All_items_record:
        print(i[0], "\t", i[1],"\t",i[2], "\t", i[3], "\t", i[4], "\t", i[5],  file = RBH_tsv)

   
