#!/bin/bash
# QC time
plinkPath=$2./plink
dir=$1
echo "$dir"
echo "$plinkPath"
echo "cleaning data..."
$plinkPath --allow-no-sex --make-bed --geno .02 --mind .02 --noweb --vcf "$dir"
echo "generating Hardy-Weinberg figures..."
$plinkPath --allow-no-sex --noweb --hardy --vcf "$dir"
