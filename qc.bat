#!/bin/bash
# QC time
plinkPath=$2./plink
dir=$1
cd /mnt/HDD/Data/
#inputs to this script are the path to a vcf of your data and a path to the directory you plink app is in
echo "$dir"
echo "$plinkPath"
# confirmation of directory inputs and tells user inital qc is starting
echo RECODE
$plinkPath --allow-no-sex --make-bed --recode --vcf "$dir"
echo GENO
$plinkPath --allow-no-sex --make-bed --geno .04 --file "plink" --out "data_genoed"
# call geno first to take out SNPs with bad overall call rate
# prolly make a grep call to log file to print out num of inidivduals removed or smth 
echo MIND
$plinkPath --allow-no-sex --make-bed  --mind .05 --bfile "data_genoed" --out "data_minded"
# call geno after mind to take out individuals with bad overall call rate
# prolly make another grep call here to do the same thing but for mind
echo "generating Hardy-Weinberg figures..."
echo HARDY
$plinkPath --allow-no-sex --hardy --bfile "data_genoed"
awk '{ if ($9 < 0.00001) print $0 }' plink.hwe > plinkfilteredhwe.hwe
echo HARDY1
$plinkPath --allow-no-sex --bfile "data_genoed" --hwe 1e-6 --make-bed --out "hwe_filter_step1"
echo HARDY2
$plinkPath --allow-no-sex --bfile "hwe_filter_step1" --hwe 1e-10 "include-nonctrl" --make-bed --out "data_hwed"
echo PIHAT
$plinkPath --allow-no-sex --bfile "data_hwed" --genome --min 0.2 --out "pihat_min0.2"
awk '{if ($8 > 0.9) print $0 }' pihat_min0.2.genome > done_pihat.genome
echo FILTERFOUNDERS
$plinkPath --allow-no-sex --bfile "data_hwed" --filter-founders --make-bed --out "data_founderfiltered"
echo FINALPIHAT
$plinkPath --allow-no-sex --bfile "data_founderfiltered" --make-bed --genome --min 0.2 --out "pihat_min0.2_in_founders"
$plinkPath --allow-no-sex --bfile "pihat_min0.2_in_founders" --freq --out "freq"
#generate HWE figures TODO take out outlier SNPs found using this analysis (p value <8*10^-5)
#use --recode to make map and ped files for --freq and stuff



