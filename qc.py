import subprocess #TODO figure out how to pipe output and also actually run plink, make funcs return plink output and grep it 
import pandas as pd
import os 
def recode(file, out="plink"):
    subprocess.run(args=["--allow-no-sex", "--make-bed", "--recode", "--vcf " + file, "--out " + out], shell=True, check=True) ### echo "recoding to binary..."
    return(out)
def geno(file, num=.05, out="data_genoed"):
    subprocess.run(args=["--allow-no-sex", "--make-bed","--geno " + num, "--bfile "+ file, "--out " + out],shell=True,check=True) ### grep -e "warning" -e "removed"
    return(out)
def mind(file, num=.05, out="data_minded"):
    subprocess.run(args=["--allow-no-sex", "--make-bed",  "--mind " + num, "--bfile" + file, "--out " + out],shell=True,check=True) ### grep -e "warning" -e "removed" -e "genotyping"
    return(out)
def hardy(file, Filter=False, p=1e-6, out="data_hwed"):
    if Filter:
        subprocess.run(args=["--allow-no-sex", "--bfile " + file, "--hwe " + p, "--make-bed", "--out " + out],shell=True,check=True) # | grep -e "removed"
        return(out)
    else:
        subprocess.run(args=["--allow-no-sex", "--hardy", "--bfile " + file]) # echo "writing unfiltered hwe data..."
def filterfounders(file, out="data_founderfiltered"):
    subprocess.run(args=["--allow-no-sex", "--bfile " + file, "--filter-founders", "--make-bed", "--out " + out]) # grep -e "removed" -e "among remaining"
    return(out)
def cleanpihat(file):
    pihat = pd.DataFrame(pd.read_table(file))
    # todo check for a large amount of one ID appearing in pairs 

def main(steps,startfile,outdir): # add option to change around thresholds
    os.chdir(outdir)
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
            subprocess.run(args=["Rscript", "-e \"require(\"tidyverse\"); setwd(getwd()); frq <- read.table(\"\"freq.frq\"\", skip=1); pdf(\"\"freq.pdf\"\"); hist(frq\$V5);dev.off()\""])
        elif step == "10":
            subprocess.run(args=["Rscript", "-e \"require(\"tidyverse\"); setwd(getwd()); hwe <- read.table(\"\"plink.hwe\"\",skip=1); pdf(\"\"hwe.pdf\"\"); ggplot(hwe, aes(V9)) +geom_density();dev.off()\""])
inputfile = input("path to data?")
outputdir = input("path where you'd like your results?")
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
