import subprocess #TODO figure out how to pipe output and also actually run plink, make funcs return plink output and grep it 
import pandas as pd
import os
import time
def recode(file, out="plink"):
    recode = subprocess.Popen(args=['./qc.bat'],stdout=subprocess.PIPE) ### echo "recoding to binary..."
    output = recode.stdout.read()
    return(out)
def geno(file, num=.05, out="data_genoed"):
    geno = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed","--geno", str(num), "--bfile", file, "--out", out],stdout=subprocess.PIPE) ### grep -e "warning" -e "removed"
    return(out)
def mind(file, num=.05, out="data_minded"):
    mind = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed",  "--mind", str(num), "--bfile", file, "--out", out],stdout=subprocess.PIPE) ### grep -e "warning" -e "removed" -e "genotyping"
    return(out)
def hardy(file, Filter=False, p=1e-6, out="data_hwed"):
    if Filter:
        hardy= subprocess.Popen(args=["plink","--allow-no-sex", "--bfile", file, "--hwe",str(p), "--make-bed", "--out", out],stdout=subprocess.PIPE) # | grep -e "removed"
    else:
        hardy = subprocess.Popen(args=["plink","--allow-no-sex", "--hardy", "--bfile", file]) # echo "writing unfiltered hwe data..."
    return(out)
def filterfounders(file, out="data_founderfiltered"):
    ff = subprocess.Popen(args=["plink","--allow-no-sex", "--bfile", file, "--filter-founders", "--make-bed", "--out", out],stdout=subprocess.PIPE) # grep -e "removed" -e "among remaining"
    return(out)
def freq(file, x=False, out="freq"):
    if x:
        freqx= subprocess.Popen(args=['plink', "--allow-no-sex", "--bfile", file, "--freqx", "--out", out],stdout=subprocess.PIPE) # | grep -e "Total genotyping rate"
    else:
        freq = subprocess.Popen(args=['plink', "--allow-no-sex", "--bfile", file, "--freq", "--out", out],stdout=subprocess.PIPE) # | grep -e "Total genotyping rate"
    return(out)

def cleanpihat(file,thresh,out='cleanedplink'):
    ibd = pd.read_csv('plink.genome',sep=' ')
    for index, row in ibd.iterrows():
        

    # todo check for a large amount of one ID appearing in pairs 
    
def main(steps,startfile,outdir): # add option to change around thresholds
    #os.chdir(outdir)
    out = startfile
    for step in steps.split(" "):
        if step == "1":
             out = recode(out)
        elif step == "2":
            out = geno(out)
        elif step == "3":
            out = mind(out)
        elif step == "4":
            hardy(out, Filter=True)
        elif step == "5":
            print(out)
            out = hardy(out)
        elif step == "6":
            print("work in progress")
            pass
            # todo workin on this to make it actually useful
        elif step == "7":
            out = filterfounders(out)
        elif step == "8":
            print("work in progress")
            pass
            # todo workin on this to make it actually useful
        elif step == "9":
            subprocess.run(args=["Rscript", "-e", "require(\"tidyverse\"); setwd(getwd()); frq <- read.table(\"freq.frq\", skip=1); pdf(\"freq.pdf\"); hist(frq\$V5);dev.off()\""])
        elif step == "10":
            subprocess.run(args=["Rscript", "-e", "require(\"tidyverse\"); setwd(getwd()); hwe <- read.table(\"plink.hwe\",skip=1); pdf(\"hwe.pdf\"); ggplot(hwe, aes(V9)) +geom_density();dev.off()\""])
inputdir= input("path to data?")
inputdir = '/home/elamd/Downloads/toy'
outputdir = input("path where you'd like your results?")
outputdir = '/home/elamd/projects/GeneScripts/'
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
if __name__ == "__main__":
    if steps == "":
        steps = "1 2 3 4 5 6 7 8 9 10"
    main(steps,inputfile,outputdir)
