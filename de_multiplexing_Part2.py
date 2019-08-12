#!usr/bin/env python
def de_multiplex(R1,R2,R3,R3,index_list):
    '''This functions calculautes number of reads that have:
            1) Index Swapped
            2) Undetermined Index
            3) Dual Index Matching
        and also writes results of all 3 into new files'''

        ''' Store all in barcodes in dictionary with barcode as key and sample number as value'''

        "Open files--> (R1,R2,R3,R3,index_list,swapped,Undetermined,dualmatch) as r1,r2,r3,r4,i,s,u,d:"
        ''' store four lines of R2 and R3 in an dictionary with header_sequence as key and others as values'''
            "Strip the sequence line of R2 and R3, Convert R3 into its complementory sequence"
            "if R2-sequence is present in barcode dictionary:"
                "check (if  reverse complement of R3 == R2) and (reverse complement of R3 in barcode dictionary)"
                    " increment Dual_Index_Matching variable)"
                    " write in dual_match"
                "check (if  reverse complement of R3 != R2) and  (reverse complement of R3 in barcode dictionary)"
                    " increment Index Swapped variable)"
                        " write in swap file"
                "check (if  reverse complement of R3 != R2) and  (reverse complement of R3 not in barcode dictionary)"
                    " increment Index Swapped variable)"
                        " write in swap file"

            "elif  R2-sequence is not present in barcode dictionary"
                    " increment Undetermined Index variable"
                    " write in undetermined file"


            return
''' Input Files- 1) all four read files (R1,R2,R3,R3,)
                 2) List of file containing barcodes
                 3) file for output- 2 for Swapped
                                     2 for Undetermined
                                     48 for dual_matched'''
''' Output Files-
                     2 for Swapped
                     2 for Undetermined
                     48 for Dual Matched'''
'''Example files -  R1.fastq,R2.fastq,R3.fastq,R4.fastq'''
