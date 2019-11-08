#!usr/bin/env python
###Import required Libraries
try:
    import numpy as np
    import matplotlib.pyplot as plt
    import argparse
    import gzip
    import seaborn as sns
    from multiprocessing import Pool
except ImportError:

    print("Module does not exist")
#Input File
#file = "C:/Bi621/shell/lane1_NoIndex_L001_R1_003.fastq"
#file = "C:/Bi622/De_multiplexing/ps4-pranavs22-master/ps4-pranavs22-master/test.fastq"
#Initializing 2D array
R1="/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz"
R2="/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz"
R3="/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz"
R4="/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz"
# R1="/projects/bgmp/pranavs/DE_Multiplexing/R1_fastq.gz"
# R2="/projects/bgmp/pranavs/DE_Multiplexing/R2_fastq.gz"
# R3="/projects/bgmp/pranavs/DE_Multiplexing/R3_fastq.gz"
# R4="/projects/bgmp/pranavs/DE_Multiplexing/R4_fastq.gz"

#
# def get_args():
#     parser = argparse.ArgumentParser(description="asa")
#     parser.add_argument("-r", "--read", help="Name of Read file", required=True, type=str)
#     return parser.parse_args()

# args=get_args()
# read=args.read
files=[R1,R2,R3,R4]

#Function to co nvert single character to phred score

def convert_phred(letter):
    """Converts a single character into a phred score"""
    return ord(letter)-33
#Function to populate all_qscores array with values
def populate_array(file):
    ''' This functions calculates mean scores of Quality Score at each Position.
    The quality score data is also stored in a separate file for future use'''
    Avg=percentage_reads_bet_30_35=percentage_reads_abv_35=bet_30_35=abv_35=0
    if "R1" in file or "R4" in file:
        all_qscores=np.zeros((101))
        X=np.arange(101)
    else:
        all_qscores=np.zeros((8))
        X=np.arange(8)
    #open File
    with gzip.open (file,'rb',) as fh:
        i=0
        LN=1
        for line in fh:

            i+=1
            line=line.decode('utf8').strip('\n')
            if i % 4 == 0:

                for score in range(0,len(line)):
                    q_score=convert_phred(line[score])
                    all_qscores[score]+=q_score
                Avg=sum(all_qscores)/101
                if Avg > 30.0  and Avg < 35.0:
                    bet_30_35+=1
                elif Avg > 35.0:
                    abv_35+=1

                LN+=1
    #calculate percentges
    percentage_reads_bet_30_35=(bet_30_35/(i/4))*100
    percentage_reads_abv_35=(abv_35/(i/4))*100
    # Recoed Qscores in new file for future reference
    out='/projects/bgmp/pranavs/DE_Multiplexing' + '_data.txt'

    for score in range(len(all_qscores)):
        all_qscores[score]=all_qscores[score]/(i/4)
    print(all_qscores)

    with open(out,'a') as o:
        o.writelines(str(all_qscores))
        o.write("\n Percentage of reads between 30 and 35:" + str(percentage_reads_bet_30_35))
        o.write("\n Percentage of reads above 35:" + str(percentage_reads_abv_35))
    ###Plots
    #X-Axis common to all plots

    Y=all_qscores
    plt.title("Mean Quality Score at each Position")
    plt.xlabel("Nucleotide Position")
    plt.ylabel("Mean Score")
    # alpha=0.5,color='green', animated=False,width=1.0
    sns.set_style("darkgrid")
    plt.bar(X,Y,color='blue')
    if "R1" in file:
         out_name= '/projects/bgmp/pranavs/DE_Multiplexing/R1' +'_' + 'Mean'+'.png'
         plt.savefig(out_name)
    elif "R2" in file:
         out_name= '/projects/bgmp/pranavs/DE_Multiplexing/R2' +'_' + 'Mean'+'.png'
         plt.savefig(out_name)
    elif "R3" in file:
         out_name= '/projects/bgmp/pranavs/DE_Multiplexing/R3' +'_' + 'Mean'+'.png'
         plt.savefig(out_name)
    elif "R4" in file:
         out_name= '/projects/bgmp/pranavs/DE_Multiplexing/R4' +'_' + 'Mean'+'.png'
         plt.savefig(out_name)



    return
if __name__=="__main__":
    with Pool(4) as p:
        print(p.map(populate_array, [R1,R2,R3,R4]))
