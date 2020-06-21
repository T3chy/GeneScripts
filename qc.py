# import subproccess
def runstep(step, arg):
    pass
steps = input ("""
planned qc steps:
1) recode vcf to binary (skip this if you already have .bim and .map files)
2) --geno .05 to remove all markers (SNPs) with more than 5% missingness
3) --mind .05 to remove all individuals with more than 5% missingness
4) --hardy to generate HWE data for p-value visualization
5) --hwe 1e-6 to filter out all individuals with a p value lower than 1e-6
6) --genome to generate IBD data report for visualization
7) --filter-founders to filter out all samples with at least one known parental ID 
8) --freq to generate MAF data report for visualization
planned graphing steps:
9) graph p-values for HWE
10) graph MAF data
please enter any number of these steps in the order you'd by number seperated with spaces, or press enter to run them all in the order presented!
""")
if steps == "":
    steps = "1 2 3 4 5 6 7 8 9 10"

