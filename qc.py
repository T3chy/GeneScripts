import subprocess #TODO figure out how to pipe output and also actually run plink, make funcs return plink output and grep it 
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
def getterms(string,terms):
    string = str(string.read())
    for line in string.split('\n'):
        for term in terms:
            if term in line:
                print(line)
def parser(stdoutput):
    if stdoutput.returncode == 1:
        print("graph makin' went wrong: here's the error output")
        print(stdoutput.stdout)
        return 0
    stdoutput = str(stdoutput.stdout)
    print("graph generated")
def recode(file, out="plink"):
    recode = subprocess.run(args=["plink","--allow-no-sex", "--make-bed", "--recode", "--file", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### echo "recoding to binary..." 
    output = recode.stdout
    print("recoding to binary...")
    return(out)
def geno(file, num=.05, out="data_genoed"):
    geno = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed","--geno", str(num), "--bfile", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### grep -e "warning" -e "removed"
    output = geno.stdout
    getterms(output,['warning','removed'])
    return(out)
def genome(file, out="IBD", filter=False, x=.05):
    if filter:
            genome = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed","--genome", "--min", str(x), "--bfile", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### grep -e "warning" -e "removed"
            output = genome.stdout
            getterms(output,["Finished","Error","Warning"])
            return(out)
    else:
        genome = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed","--genome", "--bfile", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### grep -e "warning" -e "removed"
        output = genome.stdout
def mind(file, num=.05, out="data_minded"):
    print("gamer")
    mind = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed",  "--mind", ".05", "--bfile", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### grep -e "warning" -e "removed" -e "genotyping"
    output = mind.stdout  
    getterms(output,['warning','removed'])  
    return(out)
def hardy(file, Filter=False, p=.05, out="data_hwed"):
    if Filter:
        hardy= subprocess.Popen(args=["plink","--allow-no-sex", "--bfile", file, "--hwe",str(p), "--make-bed", "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # | grep -e "removed"
        output = hardy.stdout    
        getterms(output,[""])    
    else:
        hardy = subprocess.Popen(args=["plink","--allow-no-sex", "--hardy", "--bfile", file], stdout=subprocess.PIPE, encoding='utf-8') # echo "writing unfiltered hwe data..."
        print("writing unfiltered hwe data...")
    return(out)
def filterfounders(file, out="data_founderfiltered"):
    ff = subprocess.Popen(args=["plink","--allow-no-sex", "--bfile", file, "--filter-founders", "--make-bed", "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # grep -e "removed" -e "among remaining"
    output = ff.stdout    
    getterms(output,['among remaining','removed']) 
    return(out)
def freq(file, filter=False, x=.05, out="freq"):
    if filter:
        freq= subprocess.Popen(args=['plink', "--allow-no-sex", "--bfile", file, "--maf", str(x), "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # | grep -e "Total genotyping rate"
    else:
        freq = subprocess.Popen(args=['plink', "--allow-no-sex", "--bfile", file, "--freq", "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # | grep -e "Total genotyping rate"
    output = freq.stdout
    getterms(output,['Total genotyping rate'])
    return(out)

# def cleanpihat(file,thresh,out='cleanedplink'):
#     ibd = pd.read_csv('plink.genome',sep=' ')
#     for index, row in ibd.iterrows():
        

#     # todo check for a large amount of one ID appearing in pairs 
    
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
        elif step ==  "5":
           out = genome(out,filter=True)
        elif step == "6":
            out = filterfounders(out)
        elif step == "7":
            hardy(out)
        elif step == "8":
            genome(out)
            # todo workin on this to make it actually useful
        elif step == "9":
            out = freq(out)
            # todo workin on this to make it actually useful
        elif step == "10":
           print("generating frequency graph...")
           freqgraph = subprocess.run(args=["Rscript", "-e", "require(\"tidyverse\"); setwd(getwd()); frq <- read.table(\"freq.frq\", skip=1); pdf(\"freq.pdf\"); hist(frq$V5);dev.off()"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
           parser(freqgraph)
           print("graph saved to \'freq.pdf\'")
        elif step == "11":
            print("generating hwe graph...")
            hwegraph = subprocess.run(args=["Rscript", "-e", "require(\"tidyverse\"); setwd(getwd()); hwe <- read.table(\"plink.hwe\",skip=1); pdf(\"hwe.pdf\"); hist(hwe$V9, main=\"Hardy-Weinberg Test Density\", xlab=\"p-value\");dev.off()"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
            parser(hwegraph)
            print("graph saved to \'hwe.pdf\'")
        elif step == "12":
            print("generating pi-hat value distribution...")
            pihatgraph = subprocess.run(args=["Rscript", "-e", "require(\"tidyverse\"); setwd(getwd()); ibd <- read.table(\"IBD.genome\",skip=1); pdf(\"IBD.pdf\");hist(ibd$V10, main=\"Pi-Hat Values\",xlab=\"pi-hat\");dev.off()"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='utf-8')
            parser(pihatgraph)
            print("graph saved to \'IBD.pdf\'")

inputfile = input("""path to data (write the full path including the name, but not the extension (an extension is the stuff following the period ex .map is an extension)
example: if my input plink files are named hapmap1.whateverextension, my input here would be /home/elamd/projects/GeneScripts/hapmap1""")
# inputfile = '/home/elamd/projects/GeneScripts/hapmap1'
outputdir = input("""path where you'd like your results?
example: /home/elamd/projects/GeneScripts/ will put all of the intermediary files, summary stats, and pdfs in the folder "GeneScripts"
""")
 #outputdir = '/home/elamd/projects/GeneScripts/'
steps = input ("""
planned qc steps:
1) recode vcf to binary (skip this if you already have .bim and .map files)
2) --geno .05 to remove all markers (SNPs) with more than 5% missingness
3) --mind .05 to remove all individuals with more than 5% missingness
4) --hwe .05 to filter out all individuals with a p value lower than 1e-6
5) --genome --min .05 to filter for IBD
8) --filter-founders to filter out all samples with at least one known parental ID

planned summary data generation steps:
6) --hardy to generate HWE data for p-value visualization
7) --genome to generate IBD data report for visualization
9) --freq to generate MAF data report for visualization

planned graphing steps:
10) graph p-values for HWE
11) graph MAF data
12) graph distribution of pi-hat values for IBD pairs
please enter any number of these steps in the order you'd by number seperated with spaces, or press enter to run them all in the order presented!
""")
if __name__ == "__main__":
    if steps == "":
        steps = "1 2 3 4 5 6 7 8 9 10 11 12"
    main(steps,inputfile,outputdir)
