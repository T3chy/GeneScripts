#!/bin/bash
### EXAMPLE USAGE- if your plnk exexutable is in the downloads folder and you are in the directory with this script in it, you would run this script like so:  ###
### ./qc.bat /path/to/data/data.vcf ~/Downloads/ /folder/I/want/results/in###
# QC time
#inputs to this script are the path to a vcf of your data and a path to the directory you plink app is in
plinkPath=$2./plink
dir=$1
wd=$3
cd "$wd" 
# confirmation of directory inputs and tells user inital qc is starting
echo "$dir"
echo "$plinkPath"
# change vcf to binary .bed for use w/ plink
$plinkPath --allow-no-sex --make-bed --recode --vcf "$dir" | echo "recoding to binary..."
echo GENO
# call geno first to take out SNPs with bad overall call rate
$plinkPath --allow-no-sex --make-bed --geno .04 --bfile "plink" --out "data_genoed" | grep -e "warning" -e "removed"
echo MIND
# call mind after geno to take out individuals with bad overall call rate considering SNPs with bad call rates
$plinkPath --allow-no-sex --make-bed  --mind .05 --bfile "data_genoed" --out "data_minded" | grep -e "warning" -e "removed" -e "genotyping"
# prolly make another grep call here to do the same thing but for mind
echo HARDY
#generate hwe equalibrium data
$plinkPath --allow-no-sex --hardy --bfile "data_genoed" | echo "writing unfiltered hwe data..."
# filter hwe file to remove all individuals w/ p values < 1*10^-5
awk '{ if ($9 < 0.00001) print $0 }' plink.hwe > plinkfilteredhwe.hwe 
echo HARDY1
# this filters the actual binary file to individuals w p values > 1*10^-6 
$plinkPath --allow-no-sex --bfile "data_genoed" --hwe 1e-6 --make-bed --out "hwe_filter_step1" | grep -e "removed"
echo HARDY2
# for case-control data, this filters the subjects too to a looser standard
$plinkPath --allow-no-sex --bfile "hwe_filter_step1" --hwe 1e-10 "include-nonctrl" --make-bed --out "data_hwed" | grep -e "removed"
echo PIHAT
# pihat IBD estimate to .genome file with a min pihat value of .2
$plinkPath --allow-no-sex --bfile "data_hwed" --genome --min 0.2 --out "pihat_min0.2" | grep -e "people" -e "excluding" -e "Among remaining" -e "are missing"
#filters .genome file to only over .9 pihat- this is just for graphing and stuff
awk '{if ($8 > 0.9) print $0 }' pihat_min0.2.genome > done_pihat.genome
echo FILTERFOUNDERS
#filters founders
$plinkPath --allow-no-sex --bfile "data_hwed" --filter-founders --make-bed --out "data_founderfiltered" | grep -e "removed" -e "among remaining"
echo FINALPIHAT
#pihat on the actual data after founder filtered, filtering for pihat below .2
$plinkPath --allow-no-sex --bfile "data_founderfiltered" --make-bed --genome --min 0.2 --out "pihat_min0.2_in_founders" | grep -e "among remaining"
#generate allele frequency for analysis / visualization
$plinkPath --allow-no-sex --bfile "pihat_min0.2_in_founders" --freq --out "freq" | grep -e "Total genotyping rate"
### GRAPHING TIME BABY ###
echo "Graphing Minor Allele Frequency..."

Rscript -e "require("tidyverse"); setwd(getwd()); frq <- read.table("\"freq.frq\"", skip=1); pdf("\"freq.pdf\""); hist(frq\$V5);dev.off()"
### MAKE AXIS LABELS WORK AHH main="Minor Allele Frequency Distribution", xlab="Mean Minor Allele Frequency", ylab="Number of SNPs")" ###
echo "Graphing hwe..."
Rscript -e "require("tidyverse"); setwd(getwd()); hwe <- read.table("\"plink.hwe\"",skip=1); pdf("\"hwe.pdf\""); ggplot(hwe, aes(V9)) +geom_density();dev.off()"
###TODO grep output and simplify to just what got removed and stuff###
###ALSO TODO maybe plot pihat or smth?, install R packages if they aren't, more usability stuff, maybe concatenate graphing funcs ###
