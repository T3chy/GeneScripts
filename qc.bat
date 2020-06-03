#!/bin/bash
# QC time
plinkPath=$2./plink
dir=$1
echo "$dir"
echo "$plinkPath"
echo "cleaning data..."
$plinkPath --allow-no-sex --make-bed --geno .02 --mind .02 --vcf "$dir" --out "$dir"
echo "generating Hardy-Weinberg figures..."
$plinkPath --allow-no-sex --hardy --vcf "$dir" --out "$dir"
Rscript -e "hwe <- read.table("$dir" + ".hwe"); plot(hwe$V4,hwe$V5)
