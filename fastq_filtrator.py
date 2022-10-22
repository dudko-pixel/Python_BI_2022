## Functions
# This is a function that returns "Pass" if gc content of a read is between gc_bounds and "Fail" if it's not
def gc_filter(seq, gc_bounds):
    if len(gc_bounds) == 2:
        min_gc, max_gc = int(gc_bounds[0]), int(gc_bounds[1])
    elif len(gc_bounds) == 1:
        min_gc, max_gc = int(gc_bounds[0]), 0 
    else:
        min_gc, max_gc = 0, 100
    gc_count = int((seq.count('G') + seq.count('C')) * 100 / len(seq))
    if ((gc_count < max_gc) and (gc_count > min_gc)):
        return "Pass"
    else:
        return "Fail"
 
# This is a function that counts an average qual phred33 for a read and returns "Pass"  if qual is more than a quality threshhold or "Fail" if it's not
# 1. creating Qlist
a = []
for number in range(0,41):
    a += [number]
# 2. decoder function
def decode_qual(qual_seq, *quality_threshold):
    if len(quality_threshold) == 1:
        min_qual = int(quality_threshold[0])
    else:
        min_qual = 0
    q_quant = 0
    for q in qual_seq:
        q_quant += a[ord(q)-33]
    qual_count = int(q_quant/len(qual_seq))
    if (qual_count >= min_qual):
        return "Pass"
    else:
        return "Fail"

# This is a function that counts the len of a read and returns "Pass" (if it's more than a min_len and less than a max_len) or "Fail" if it's not
def len_filter(read, length_bounds):
    if len(length_bounds) == 2:
        min_len = length_bounds[0]
        max_len = length_bounds[1]
    elif len(length_bounds) == 1:
        max_len = length_bounds[0]
        min_len = 0
    else:
        max_len = 2**32
        min_len = 0
    if ((len(read) < max_len) and (len(read) > min_len)):
        return "Pass"
    else:
        return "Fail"
			
## This is a horrifying main function that takes all the above and uses it to filter your fastq file
def main(input_fastq, output_file_prefix, gc_bounds = [0, 100], length_bounds = [0, 2**32], quality_threshold = 0, save_filtered = 'False'):
    with open("test.fastq", "r") as fastq:
        lines = fastq.readlines()
        names=[item[:-1] for item in lines[::4]] 
        reads=[item[:-1] for item in lines[1::4]]
        comments=[item[:-1] for item in lines[2::4]]
        fastq_dic = {}
        for i in range(0, len(reads)):
            fastq_dic[reads[i]] = [names[i]] 
            fastq_dic[reads[i]] += [comments[i]]
            fastq_dic[reads[i]] += [quals[i]] # we'll have a dict with all our sequences as keys and their infos as values
        filt = {}
        for i in range(0, len(reads)):
            filt[reads[i]] = [gc_filter(reads[i], gc_bounds)]
            filt[reads[i]] += [len_filter(reads[i], length_bounds)]
            filt[reads[i]] += [decode_qual(quals[i], quality_threshold)]
        passed_fq = []
        failed_fq = []
        for key, value in filt.items():
            if 'Fail' not in value:
                passed_fq += [key]
            else:
                if save_filtered == "True":
                    failed_fq += [key]
                    failed_fq_lst = []
                    for read in failed_fq:
                        failed_fq_lst += [fastq_dic[read]] # list with infos about reads that failed the filter
                    with open(output_file_prefix + "_failed.fastq", "w+") as out_failed:
                        for i in range(0, len(failed_fq)):
                            out_failed.write(failed_fq_lst[i][0])
                            out_failed.write("\n")
                            out_failed.write(failed_fq[i])
                            out_failed.write("\n")
                            out_failed.write(failed_fq_lst[i][1])
                            out_failed.write("\n")
                            out_failed.write(failed_fq_lst[i][2])
                            out_failed.write("\n")    
        passed_fq_lst = []
        for read in passed_fq:
            passed_fq_lst += [fastq_dic[read]] # list with infos about reads that passed the filter
        output_passed_file_name = output_file_prefix + "_passed.fastq"
        with open(output_passed_file_name, "w+") as out_passed:
            for i in range(0, len(filtered_fq)):
                out_passed.write(passed_fq_lst[i][0])
                out_passed.write("\n")
                out_passed.write(passed_fq[i])
                out_passed.write("\n")
                out_passed.write(passed_fq_lst[i][1])
                out_passed.write("\n")
                out_passed.write(passed_fq_lst[i][2])
                out_passed.write("\n")
