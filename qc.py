import subprocess #TODO figure out how to pipe output and also actually run plink, make funcs return plink output and grep it 
# take out redundant genome 
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
def king(file, out="king"):
    king = subprocess.Popen(args=["king", "-b", file + ".bed", "--related"],stdout=subprocess.PIPE,encoding="utf-8")
    output = king.stdout
    getterms(output,[""])
    return(out)
def chrom(file,rangeincl):
    if rangeincl == "":
        return file
    else:
        out = file + "_chromed"
        chrom = subprocess.run(args=["plink", "--allow-no-sex", "--make-bed", "--chr", rangeincl, "--out", out], stdout=subprocess.PIPE, encoding="utf-8")
        output = chrom.stdout
        getterms(output, [])
        return(out)
def recode(file, out="recoded"):
    out = file + "_recoded"
    recode = subprocess.run(args=["plink","--allow-no-sex", "--make-bed", "--recode", "--file", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### echo "recoding to binary..." 
    output = recode.stdout
    print("recoding to binary...")
    return(out)
def geno(file, num=.05, out="genoed"):
    
    out = file + "_genoed" + str(num)
    geno = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed","--geno", str(num), "--bfile", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### grep -e "warning" -e "removed"
    output = geno.stdout
    getterms(output,['warning','removed'])
    return(out)
def genome(file, out="IBD", filter=False, x=.05):
    if filter:
            out = file + "_IBD" + str(x)
            genome = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed","--genome", "--min", str(x), "--bfile", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### grep -e "warning" -e "removed"
            output = genome.stdout
            getterms(output,["Finished","Error","Warning"])
            return(out)
    else:
        out = file + "_IBD_no_filter" 
        genome = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed","--genome", "--bfile", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### grep -e "warning" -e "removed"
        output = genome.stdout
def mind(file, num=.05, out="minded"):
    out = file + "_minded" + str(num)
    mind = subprocess.Popen(args=["plink","--allow-no-sex", "--make-bed",  "--mind", ".05", "--bfile", file, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') ### grep -e "warning" -e "removed" -e "genotyping"
    output = mind.stdout  
    getterms(output,['warning','removed']) 
    return(out)
def hardy(file, Filter=False, p=.05, out="hwed"):
    if Filter:
        out = file + "_hwed" + str(p)
        hardy= subprocess.Popen(args=["plink","--allow-no-sex", "--bfile", file, "--hwe",str(p), "--make-bed", "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # | grep -e "removed"
        output = hardy.stdout    
        getterms(output,["removed"])
    else:
        out = file + "_hardy_no_filter" 
        hardy = subprocess.Popen(args=["plink","--allow-no-sex", "--hardy", "--bfile", file, "--out", out], stdout=subprocess.PIPE, encoding='utf-8') # echo "writing unfiltered hwe data..."
        print("writing unfiltered hwe data...")
    return(out)
def filterfounders(file, out="founderfiltered"):
    out = file + "_founderfiltered"
    ff = subprocess.Popen(args=["plink","--allow-no-sex", "--bfile", file, "--filter-founders", "--make-bed", "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # grep -e "removed" -e "among remaining"
    output = ff.stdout    
    getterms(output,['among remaining','removed']) 
    return(out)
def freq(file, filter=False, x=.05, out="freq"):
    out = file + "_freq" + str(x) # todo this fore the rest oif the commands 
    if filter:
        freq= subprocess.Popen(args=['plink', "--allow-no-sex", "--bfile", file, "--maf", str(x), "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # | grep -e "Total genotyping rate"
    else:
        freq = subprocess.Popen(args=['plink', "--allow-no-sex", "--bfile", file, "--freq", "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # | grep -e "Total genotyping rate"
    output = freq.stdout
    getterms(output,['Total genotyping rate'])
    return(out)
def maf(file, x=0.05, out="maf"):
    out = file + "_maf" + str(x)
    freq = subprocess.Popen(args=['plink', "--allow-no-sex", "--bfile", file, "--maf", x, "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # | grep -e "Total genotyping rate"
    output = freq.stdout
    getterms(output, ["removed"])
    return(out)
# def cleanpihat(file,thresh,out='cleanedplink'):
#     ibd = pd.read_csv('plink.genome',sep=' ')
#     for index, row in ibd.iterrows():
        

#     # todo check for a large amount of one ID appearing in pairs 
    
def main(steps,startfile,outdir): # add option to change around thresholds
    #os.chdir(outdir)
    out = startfile
    chrange = input("""Would you like to only include some chromosomes? If you would, enter the desired chromosomes in a plink-acceptable format eg. 1-4,22,xy or something similar. If you want to keep all chromosomes, just press enter!""")
    if chrange != "":
        out = chrom(out,chrange)
    steps = steps.split(" ")
    x = 0.05
    pos = 0
    for i in steps:
        try:
            if steps[pos+1].isnumeric():
                x = steps[i+1]
                flag = 1
            else:
                x = 0.05
                flag = 0
        except:
            x = 0.05
            flag = 0
        if steps[pos] == "recode":
             out = recode(out)
        elif steps[pos] == "geno":
             out = geno(out,x)
        elif steps[pos] == "mind":
             out = mind(out,x)
        elif steps[pos] == "hwe":
             out = hardy(out, x, Filter=True)
        elif steps[pos] == "filterfounders":
             out = filterfounders(out)
        elif steps[pos] == "hardy":
            hardy(out)
        elif steps[pos] == "maf":
            out = maf(out,x)
        pos += 2 if flag else 1
       # elif steps[pos] == "maf":
       #     genome(out)
      #  elif steps[pos] == "maf":
      #       freq(out)
            # todo workin on this to make it actually useful
#        elif steps[pos] == "9":
#           print("generating frequency graph...")
#           freqgraph = subprocess.run(args=["Rscript", "-e", "require(\"tidyverse\"); setwd(getwd()); frq <- read.table(\"" +out +"_frq0.05"+".frq\", skip=1); pdf(\"freq.pdf\"); hist(frq$V5);dev.off()"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
#           parser(freqgraph)
#           print("graph saved to \'freq.pdf\'")
#        elif steps[pos] == "10":
#            print("generating hwe graph...")
#            hwegraph = subprocess.run(args=["Rscript", "-e", "require(\"tidyverse\"); setwd(getwd()); hwe <- read.table(\""+out+"_hardy_no_filter.hwe\",skip=1); pdf(\"hwe.pdf\"); hist(hwe$V9, main=\"Hardy-Weinberg Test Density\", xlab=\"p-value\");dev.off()"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
#            parser(hwegraph)
#            print("graph saved to \'hwe.pdf\'")
#        elif steps[pos] == "11":
#            print("generating pi-hat value distribution...")
#            pihatgraph = subprocess.run(args=["Rscript", "-e", "require(\"tidyverse\"); setwd(getwd()); ibd <- read.table(\""+out+"_IBD_no_filter.genome\",skip=1); pdf(\"IBD.pdf\");hist(ibd$V10, main=\"Pi-Hat Values\",xlab=\"pi-hat\");dev.off()"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='utf-8')
#            parser(pihatgraph)
#            print("graph saved to \'IBD.pdf\'")
    return out
inputfile = input("""path to data (write the full path including the name, but not the extension (an extension is the stuff following the period ex .map is an extension)
example: if my input plink files are named hapmap1.whateverextension, my input here would be /home/elamd/projects/GeneScripts/hapmap1
""")
#inputfile = '/home/elamd/projects/GeneScripts/hapmap1'
outputdir = input("""path where you'd like your results?
example: /home/elamd/projects/GeneScripts/ will put all of the intermediary files, summary stats, and pdfs in the folder "GeneScripts"
""")
#outputdir = '/home/elamd/projects/GeneScripts/test/'
# ask laura about adding KING IBD and stuff
#steps = input ("""
#planned qc steps:
#1) recode vcf to binary (skip this if you already have .bim and .map files)
#2) --geno .05 to remove all markers (SNPs) with more than 5% missingness
#3) --mind .05 to remove all individuals with more than 5% missingness
#4) --hwe .05 to filter out all individuals with a p value lower than 1e-6
#5) --filter-founders to filter out all samples with at least one known parental ID
#
#planned summary data generation steps:
#6) --hardy to generate HWE data for p-value visualization
#7) --genome to generate IBD data report for visualization
#8) --freq to generate MAF data report for visualization
#
#planned graphing steps:
#9) graph p-values for HWE
#10) graph MAF data
#11) graph distribution of pi-hat values for IBD pairs
#please enter any number of these steps in the order you'd by number seperated with spaces, or press enter to run them all in the order presented!
#""")
steps = input ("""
___________________________________________________________________________________________________
|                                  Welcome to this QC Script!                                     |
| Please type the plink commands you would like to perform in the order you'd like them performed | 
|                           Put a value where applicable! (eg, geno 0.05)                         |
|                  For example, the default setting is \"geno 0.05 mind 0.05\"                    |
|                                   Available QC commands:                                        |
|                     geno(--geno x), mind(--mind x), hwe(--hwe x), maf(--maf)                    |
|_________________________________________________________________________________________________|

""")
if __name__ == "__main__":
    if steps == "":
        steps = "geno 0.05 mind 0.05"
    final = main(steps,inputfile,outputdir)
    print("your qced files have the filename: " +final + " (plus their associated file extension)")
