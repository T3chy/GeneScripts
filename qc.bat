#!/bin/bash
# QC time
plinkPath=$2./plink
dir=$1
#inputs to this script are the path to a vcf of your data and a path to the directory you plink app is in
echo "$dir"
echo "$plinkPath"
echo "cleaning data..."
# confirmation of directory inputs and tells user inital qc is starting
$plinkPath --allow-no-sex --make-bed .05 --mind .05 --vcf "$dir" --out "$dir""_mind"
# call mind first to take out SNPs with bad overall call rate
# prolly make a grep call to log file to print out num of inidivduals removed or smth 
$plinkPath --allow-no-sex --make-bed .05 --geno .05 --file "$dir""_mind" --out "$dir""_geno" 
# call geno after mind to take out individuals with bad overall call rate
# prolly make another grep call here to do the same thing but for mind
echo "generating Hardy-Weinberg figures..."
$plinkPath --allow-no-sex --hardy --file "$dir""_geno" --out "$dir""_hwe"
#generate HWE figures TODO take out outlier SNPs found using this analysis (p value <9*10^-5)
## MORE TODO do freq w --freq and graph do pihat w --genome and graph ##


