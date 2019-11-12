
# -*- coding: utf-8 -*-
"""
 Created on Sun Oct 20 19:54:52 2019

 @author: Pranav
"""
#imports
import argparse
import gzip

#Functions
def get_args():
    ''' This function creates arguments to be passed to the program'''
    parser=argparse.ArgumentParser(description="Please provide path to your folder as well the desired text")
    parser.add_argument("-r1","--READ1",help="READ1 File",required=True,type =str)
    parser.add_argument("-r2","--READ2",help="READ2 File",required=True,type =str)
    parser.add_argument("-r3","--READ3",help="READ3 File",required=True,type =str)
    parser.add_argument("-r4","--READ4",help="READ4 File",required=True,type =str)
    parser.add_argument("-i","--Index_list",help="Index_list File",required=True,type =str)
    parser.add_argument("-c","--CUTOFF",help="Quality Score Cutoff",required=True,type =int)
    parser.add_argument("-o","--OUTDIR",help="Specify Output Directory",required=True,type =str)
    
    return parser.parse_args()


#Variables
args=get_args()
R1=args.READ1
R2=args.READ2
R3=args.READ3
R4=args.READ4
index_list=args.Index_list
out=args.OUTDIR
cutoff=args.CUTOFF

global index_count
global indexes
index_count={}
indexes=set()


#Functions
def rev_comp(sequence):
    '''
    This function takes in a string representing a
    sequence of DNA, and returns it's reverse compliment.
    '''
    seq={'A':'T','T':'A','C':'G','G':'C','N':'N'}
    comp=''.join(seq[i] for i in sequence)
    return comp[::-1]

def convert_phred(letter):
    """Converts a single character into a phred score"""
    return ord(letter)-33

def store_index(index_list):
    ''' This funtion parses indexes from index file and stores them in a dictionary'''
    try:
        with open(index_list,"r") as i:
            i.readline()
            while True:
                data=i.readline().strip().split("\t")
                if data[0]=='':
                     break
                else:

                    indexes.add(data[4])

    except IOError:
        raise SystemError(index_list + " not found")


    return 

def create_files():
    '''This function return a dictionary of files with barcodes as key(string)
    and their path as value (tuple) generates 48 files dual-mathced pairs'''
    file_dict={}
    for barcode in indexes:
        file_R1= out +'R1_'+ barcode+ '_'+rev_comp(barcode) +'.fastq'
        file_R2= out +'R2_'+ barcode+ '_'+rev_comp(barcode) +'.fastq'
        f=(open(file_R1,"a"),open(file_R2,"a") )
        file_dict[barcode]=f
    return file_dict

    
def check_qual_scores(seq,length,cutoff):
    ''' This function returns True if quality score is greater than desired cutoff''' 
    for letter in range(0,length):
        q_score=convert_phred(seq[letter])
        if q_score > cutoff:
            return True
        else:
            return False
            

def is_valid(index_r2,index_r3):
    ''' This function returns True in case both indexes do not contain 'Ns' otherwise False''' 
    if ('N' in index_r2):
        return False
    else:
        if ( 'N' in index_r3):
            return False
        else:
            return True

def is_present(index_r2,index_r3):
    ''' This funcction return True in case both the indexes are present in the index set 
    obtained from store)index function.'''
    if index_r2 in indexes:
        if index_r2 in indexes:
            return True
    else:
        return False
def de_multiplex(R1,R2,R3,R4,index_list):
    '''This functions calculautes number of reads that have:
    1) Index Swapped
    2) Undetermined Index
    3) Dual Index Matching and also writes results of all 3 into new files'''
    dual_matched=swapped=undetermined=total_records=0
    graph_index=[]
    graph_count=[]  
    store_index(index_list)
    file_dict=create_files()
    print("Part1 : Data Processing...")
    #open all files
    with gzip.open(R1) as r1, gzip.open(R2) as r2 , gzip.open(R3) as r3 , gzip.open(R4) as r4, open(swapped_r1,"a") as s1, open(swapped_r2,"a") as s2,open(Undetermined_r1,"w") as u1 ,open(Undetermined_r2,"w") as u2,open(summary,"w") as s :        
        while True:

            header_r1=r1.readline().decode('utf-8').strip()
            if header_r1=='':                                      #Read1 header
                break                                              #breaks if it reaches end of file
            else:
                                                                   #store all four lines of four files             
                seq_r1=r1.readline().decode('utf-8').strip()       #Read1 seq
                q_head_r1=r1.readline().decode('utf-8').strip()    #Read1 quality header
                q_seq_r1=r1.readline().decode('utf-8').strip()     #Read1 quality sequence
                
                r2.readline().decode('utf-8').strip()              #index header
                index_r2=r2.readline().decode('utf-8').strip()     #index sequence
                r2.readline().decode('utf-8').strip()              #Quality header line
                q_seq_r2=r2.readline().decode('utf-8').strip()     # Quality sequence
                
                r3.readline().decode('utf-8').strip()              #index header
                index_r3=r3.readline().decode('utf-8').strip()     #index sequence
                r3.readline().decode('utf-8').strip()              #Quality header line
                q_seq_r3=r3.readline().decode('utf-8').strip()     #Quality sequence
    
                header_r4=r4.readline().decode('utf-8').strip()    #Read4 header 
                seq_r4=r4.readline().decode('utf-8').strip()       #Read4 sequence
                q_head_r4=r4.readline().decode('utf-8').strip()    #Read4 quality header
                q_seq_r4=r4.readline().decode('utf-8').strip()     #Read4 quality sequence

            
                total_records+=1                                   #Increment counter for all records
                if (is_present(index_r2,index_r3)) and is_valid(index_r2,index_r3) and check_qual_scores(q_seq_r2,8,cutoff) and check_qual_scores(q_seq_r3,8,cutoff):
                    if index_r2 == rev_comp(index_r3):
                        if index_r2 in index_count:
                            index_count[index_r2]+=1
                        else:
                            index_count[index_r2]=1
                        
                        dual_matched+=1

                        header_r1='_'.join([header_r1,index_r2,index_r3])
                        file_dict[index_r2][0].write('\n'.join([header_r1,seq_r1,q_head_r1,q_seq_r1,'']))
                        
                        header_r4='_'.join([header_r4,index_r2,index_r3])
                        file_dict[rev_comp(index_r3)][1].write('\n'.join([header_r4,seq_r4,q_head_r4,q_seq_r4,'']))
                        
                    else: 
                        swapped+=1
                        
                        header_r1='_'.join([header_r1,index_r2,index_r3])
                        s1.write('\n'.join([header_r1,seq_r1,q_head_r1,q_seq_r1,'']))


                        header_r4='_'.join([header_r4,index_r2, index_r3])
                        s2.write('\n'.join([header_r4,seq_r4,q_head_r4,q_seq_r4,'']))
                else:
                    undetermined+=1
                    header_r1='_'.join([header_r1,index_r2,index_r3])
                    u1.write('\n'.join([header_r1,seq_r1,q_head_r1,q_seq_r1,'']))

                    header_r4='_'.join([header_r4,index_r2, index_r3])
                    u2.write('\n'.join([header_r4,seq_r4,q_head_r4,q_seq_r4,'']))

        print("Finished")
        print("Part 2: Writing Summary File...")

        s.write('  **Summary**   \n\n')
        s.write("1) Total number of records  "+ str(total_records)+"\n\n")
        s.write(" Index \t Percentage\n\n")
        for k,v in index_count.items():
            s.write(str(k) + "\t" + str(((v/total_records)*100)) + "\n")
            graph_index.append(k)             
            graph_count.append(v)

        s.write("3) Overall amount of Index swapping:" + str((swapped/total_records)*100)+"\n\n")

        s.write('\n **Other Information** \n\n')
        s.write("1) Total Number of records processed:" + str(total_records) + '\n')
        s.write("2) Number of dual matched pairs:" + str(dual_matched)+ '\n')
        s.write("3) Number of index hopped pairs:" + str(swapped)+ '\n')
        s.write("4) Number of undetermined read pairs:"+ str(undetermined) + '\n')
        s.write("5) Percentage of dual matched:" + str((dual_matched/total_records)*100)+ '\n')
        s.write("6) Percentage of undetermined reads:" + str((undetermined/total_records)*100)+ '\n')
        print("Demultiplexing Complete")

    return 


#outfiles
swapped_r1=out+'swapped_r1.fastq'
swapped_r2=out+'swapped_r2.fastq'
Undetermined_r1=out+'undetermined_r1.fastq'
Undetermined_r2=out+'undetermined_r2.fastq'
summary=out + 'summary.txt'


#Run the file
if __name__=='__main__':
    de_multiplex(R1,R2,R3,R4,index_list)
    
    
