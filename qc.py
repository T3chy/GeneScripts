import subprocess  
# take out redundant genome 
import pandas as pd
import matplotlib.pyplot as plt
import os
import time

def cls():
        os.system('cls' if os.name=='nt' else 'clear')
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
        out = file + "_chromed" + rangeincl
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
def filterfounders(file):
    out = file + "_founderfiltered"
    ff = subprocess.Popen(args=["plink","--allow-no-sex", "--bfile", file, "--filter-founders", "--make-bed", "--out", out],stdout=subprocess.PIPE, encoding='utf-8') # grep -e "removed" -e "among remaining"
    output = ff.stdout    
    getterms(output,['among remaining','removed']) 
    return(out)
def freq(file, filter=False, x=.05):
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
# def cleanpihat(file,thresh,out='cleanedplink'):     # todo check for a large amount of one ID appearing in pairs 
def main(steps,startfile,outdir,chrange): 
    out = startfile
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
        try:
            steps[pos]
        except:
            break
    return out
def menu():
    cls()
    inputfile = input("""   
    ___________________________________________________________________________________________________
    |                                  Welcome to this QC Script!                                     |            
    |                              Please input the path to your data                                 |
    |         Input the full path including the name of the data file, excluding the extension        |
    |            (an extension is the stuff following the period ex .map is an extension)             |
    |        For example, if my data is called "hapmap1" in the home directory, I would enter:        |
    |                                    /home/elamd/hapmap1                                          |
    |_________________________________________________________________________________________________|
    """)
    cls()
    outputdir = input("""
    ___________________________________________________________________________________________________
    |                                  Welcome to this QC Script!                                     |
    |           Please input the path to the folder you'd like your data outputted to!                |
    |                Warning: there may be a lot of intermediary files generated                      |
    |_________________________________________________________________________________________________|
    """)
    cls()
    chrange = input("""
___________________________________________________________________________________________________
|                                  Welcome to this QC Script!                                     |
|                       Would you like to only include some chromosomes?                          |
|          If you would, enter the desired chromosomes in a plink-acceptable format               |
|                                   For example: 1-4,22,xy                                        |
|                    If you want to keep all chromosomes, just press enter!                       |
|_________________________________________________________________________________________________|
    """)
    cls()
    steps = input ("""
    ___________________________________________________________________________________________________
    |                                  Welcome to this QC Script!                                     |
    | Please type the plink commands you would like to perform in the order you'd like them performed | 
    |                           Put a value where applicable! (eg, geno 0.05)                         |
    |                  For example, the default setting is \"geno 0.05 mind 0.05\"                      |
    |    Make sure to convert your data into binary files by entering "recode" as the first command!  |
    |                            (if they aren't covnerted already)                                   |
    |                                   Available QC commands:                                        |
    |                geno(--geno x), mind(--mind x), hwe(--hwe x), maf(--maf x)                       |
    |_________________________________________________________________________________________________|
 
    """)
    return steps, inputfile, outputdir, chrange
if __name__ == "__main__":
    steps, inputfile, outputdir, chrange = menu()
    if steps == "":
        steps = "geno 0.05 mind 0.05"
    final = main(steps,inputfile,outputdir,chrange)
    print("your qced files have the filename: " +final + " (plus their associated file extension)")
