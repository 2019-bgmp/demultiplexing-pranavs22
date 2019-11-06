The script: clean3.py
Description:
The script contains total 9 Functions:
Function:1 get_args
	Gives user option to input 4 gzipped fastq files.
Function:2 rev_comp
"""This function takes in a string representing a
    sequence of DNA, and returns it's reverse compliment."""

Function:3 convert_phred
"""Converts a single character into a phred score"""

Function:4 store_index
''' This funtion parses indexes deom index file and stores them in a dictionary'''

Function:5 create_files
'''This function return a dictionary of files with barcodes as key(string)
    and their path as value (tuple) generates 48 files dual-mathced pairs'''

Function:6 check_qual_scores
''' This function returns True if quality score is greater than desired cutoff''' 

Function:7 is_valid
''' This function returns True in case both indexes do not contain 'Ns' otherwise False''' 

Function:8 is_present
''' This funcction return True in case both the indexes are present in the index set 
    obtained from store)index function.'''
Function:9 de_multiplex
    '''This functions calculautes number of reads that have:
    1) Index Swapped
    2) Undetermined Index
    3) Dual Index Matching and also writes results of all 3 
    into new files'''

Variables:
Global:index_count,indexes


Script Logic (Overview):
Lines-: 156:187
1) if-else condition to :
	1) Check if indexes are present (using is_present) in given indexes. If not, collect them in undetermined bin
	2) check if indexes are valid  (i.e. does not contain 'N')using is_valid function.If not, collect them in undetermined bin
	3) check if indexes satisify desired quality score cutoff using (check_qual_scores).If not, collect them in undetermined bin 
2) if all these conditions are True:
check if indexes are reverse complement of each other, put them in dual-matched bin. if not put them in hopped bin


3) Print Relevant Info

Output : 

1)Numbers and Percentages of each bin.
2)Numbers and Percentages of read counts belonging to each barcode.
3) An image file.  

Cutoff-30
Reason: After observing histograms from Part-1, 
we see all read files (except Read 3) have quality score atleast above 30. To exclude reads below 30 from Reaad-3, a quality score of 30 was chosen.
Parameters used to run this script-
R1,R2,R3,R4,index_list,cutoff,output directory.
All of the file paths were symlinked.

** END **

2) Check Points:

1) Utilize appropriate functions --> Done
2) Sufficiently comment your code/use docstrings --> Done
3) Use unit tests on functions/entire algorithm to ensure it works properly----> Done Test files in folder named 'test_files'
4) Create a useful report for the end user of your code
Use argparse to "generalize" your code
Follow the specifications laid out in Demultiplexing, part 1 for the code 

Note:
Issues while submitting Work:
Issue 1:
Talapas system was down. (17:51pm). I could not copy slurm output file from talapas to local laptop, thus I could not push to Github.

Error:
"""Could not chdir to home directory /home/pranavs: Stale file handle
bash: /home/pranavs/.bashrc: Stale file handle
scp: /projects/bgmp/pranavs/DE_Multiplexing/outfiles/test_scripts/slurm-10409377-clean.out: Stale file handle"""

Solution:

I copied contents from Terminal (fortunately, I had cat-ed slurm output before it went down) into a new text file. 
All files can be verified later on when Talapas is up.

Issue 2: I ran this script. The image does not include proper axis and titles. 
Solution: Made Graphs in excel.

The output from current script is obtained in slurm script-"slurm-10409377-clean.out"
To address this, I created a new script- demultiplex.py, that covers all these issues. 
I was not able to run that script as Talapas was down.
