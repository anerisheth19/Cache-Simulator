############My Cache###############
############Written by Aneri Sheth##############3
#############CA Homework 1 Problem 2################


#Import python libraries
import sys
import math


##########This is the function to read files#############
##############2 files: trace.din and pinatrace.out##################
def readFile(fileAddress):
	instructions=[]
	dataAddr=[]
	combined=[]
	with open(fileAddress) as f:  #open the file 
		lines = f.readlines()
		countLines = 0
		for line in lines: #count the lines in file and split to separate data, instruction and label
			countLines = countLines + 1
			data = line.split(' ')
			if fileType is 1: #trace.din
				label = int(data[0], 10)
				addr = int(data[1], 16)
				if(label == 2):
					instructions.append(addr)
				elif(label == 0 or label == 1):
					dataAddr.append(addr)
				else:
					print(data[0])
				combined.append(addr)
			elif fileType is 0: #pinatrace.out
				address = int(data[2], 16)
				dataAddr.append(address)
				if countLines == 4000000: #limit the iterations to 4 million
					break
	return [instructions, dataAddr, combined]

#######################This is the function that calculates index, offset and tag#######################
############################Implements direct mapping and 4-way set associativity######################
def HitorMiss(addr):

	getAddress = addr #get the address from file
	addr_length = 32 #assume 32 bit address length
	offset = int(math.log(blockSize,2)) #calculate offset
	calc_index = int(math.log(cacheSize/(assoc*blockSize),2)) #calculate index
	calc_tag = addr_length - offset - calc_index #get tag
	flag1 = int(('1' * calc_tag + '0' * calc_index + '0' * offset), 2) 
	tag = (getAddress & flag1) >> (calc_index + offset) #shif the tag 
	flag2 = int(('0' * calc_index + '1' * calc_index + '0' * offset), 2)
	index = (getAddress & flag2) >> (offset) #shift the index


#############Check for associativity - direct or 4-way#################
	if assoc == 1: #direct mapping
	
		if tag == cacheArr[index]:
			return 1 #set = 1 so just compare tag
		else:
			cacheArr[index] = tag; #if not, then assign tag
			return 0        
	elif assoc == 4: #4-way set
###########################Psuedo LRU##########################
		if tag in cacheArr[index]:
			temp = cacheArr[index].index(tag)
			#print(temp)    
			lruArr[index][temp] = max(lruArr[index]) + 1 #compute max index value 
			#print(lruArr)    
			return 1
		else:
			if 0 in cacheArr[index]: 
				temp = cacheArr[index].index(0) #else give tag 
				cacheArr[index][temp] = tag; 
				lruArr[index][temp] = max(lruArr[index]) + 1 #compute max index value 
			else:
				lru = min(lruArr[index]) #get least recently used index
				temp1 = lruArr[index].index(lru)
				cacheArr[index][temp1] = tag
				lruArr[index][temp1] = max(lruArr[index]) + 1 
			return 0

##############This is the function for unified cache#############
#############It takes input as both data and instruction from file############
def CombinedCache(data_and_inst):
	i=0 #loop
	misses = 0
	hits = 0
	for addr in data_and_inst:
		
		if HitorMiss(addr) is 1: #call a function for hit or miss
			
			hits+=1 #increment hits
		else:
			
			misses = misses + 1 #increment misses
		i = i+1
	print("Number of Misses " + str(misses))
	print("Number of Hits " + str(hits))


#############This is the function for instruction cache#################
###########It takes input as instruction from file###################	
def InstructionCache(inst):
	i=0 #loop
	misses = 0
	hits = 0
	for addr in inst:
		if HitorMiss(addr) is 1:   #call a function for hit or miss  
			hits+=1    #increment hits
		else:		
			misses = misses + 1  #increment misses
		i = i+1
	print("Number of Misses " + str(misses))
	print("Number of Hits" + str(hits))


####################This is the function for data cache#################
###############It takes input as data (read/write) from file###############
def DataCache(dataAdr):
	i=0 #loop
	misses = 0
	hits = 0
	for addr in dataAdr:
		if HitorMiss(addr) is 1:    #call a function for hit or miss
			hits+=1   #increment hits
		else:		
			misses = misses + 1  #increment misses
		i = i+1
	print("Number of Misses " + str(misses))
	print("Number of Hits " + str(hits))


############################Main function for command line arguments from user#######################
#######################It implements other functions###################
if __name__ =='__main__':
	print("This is MY CACHE")
	print("Please enter file name (trace.din/drystone.out/linpack.out , 32KB (shared) or 16KB (split) cache size, 8,32 or 128B block size, Associativity - 1 or 4, Cache type - 1 for Combined and 0 for Split, File type - 1 for trace and 0 for drystone/linpack")
	if(len(sys.argv) < 6): #read 6 arguments from user 
		print(sys.argv[0] + " fileTrace cacheSize(k) blockSize assoc cache_Type fileType")
		quit()
	filePath = sys.argv[1]
	cacheSize = int(sys.argv[2]) * 1024 #in KB
	blockSize = int(sys.argv[3]) #in Bytes 
	assoc= int(sys.argv[4]) #0 or 1
	cache_Type = int(sys.argv[5]) # 0 or 1
	fileType = int(sys.argv[6]) # 0 or 1
	cacheArr = [[0]*assoc]*int(cacheSize/(blockSize*assoc)) #empty array
	lruArr = [[0]*assoc]*int(cacheSize/(blockSize*assoc)) #empty lru
	[inst, dataAdr, shared] = readFile(filePath) #read from file
	if fileType == 1: #Trace file
		if cache_Type == 0: #split cache
			InstructionCache(inst) 
			DataCache(dataAdr)
		else:
			CombinedCache(shared) #combined cache
	else: #pinatrace file 
		CombinedCache(dataAdr)
