#!/bin/bash
### EXAMPLE USAGE- if your plnk exexutable is in the downloads folder and you are in the directory with this script in it, you would run this script like so:  ###
### ./qc.bat /path/to/data/data.vcf ~/Downloads/ /folder/I/want/results/in###
# QC time
#inputs to this script are the path to a vcf of your data and a path to the directory you plink app is in
dir=$1
wd=$2
func=$3
infile=$4
outfile=$5
cd "$wd" 
# confirmation of directory inputs and tells user inital qc is starting
REM echo "$dir"
REM echo "plink"
REM # change vcf to binary .bed for use w/ plink
REM plink --allow-no-sex --make-bed --recode --vcf "$dir" | echo "recoding to binary..."
REM echo GENO
REM # call geno first to take out SNPs with bad overall call rate
REM plink --allow-no-sex --make-bed --geno .04 --bfile "plink" --out "data_genoed" | grep -e "warning" -e "removed"
REM echo MIND
REM # call mind after geno to take out individuals with bad overall call rate considering SNPs with bad call rates
REM plink --allow-no-sex --make-bed  --mind .05 --bfile "data_genoed" --out "data_minded" | grep -e "warning" -e "removed" -e "genotyping"
REM # prolly make another grep call here to do the same thing but for mind
REM echo HARDY
REM #generate hwe equalibrium data
REM plink --allow-no-sex --hardy --bfile "data_minded" | echo "writing unfiltered hwe data..."
REM # filter hwe file to remove all individuals w/ p values < 1*10^-5
REM awk '{ if ($9 < 0.00001) print $0 }' plink.hwe > plinkfilteredhwe.hwe # switch the inequality sign whoops
REM echo HARDY1
REM # this filters the actual binary file to individuals w p values > 1*10^-6 
REM plink --allow-no-sex --bfile "data_minded" --hwe 1e-6 --make-bed --out "data_hwed" | grep -e "removed"
REM # graph pihat values for all pairs- histogram, offer option to override and not do pihat if the user looks at graph and is like "nah" or script that looks if one person is paried w everyone else and rmeove that person or smth, look at times one person shows up
REM echo PIHAT
REM # pihat IBD estimate to .genome file showing pihats only over .2
REM plink --allow-no-sex --bfile "data_hwed" --genome --min 0.2 --out "pihat_min0.2" | grep -e "people" -e "excluding" -e "Among remaining" -e "are missing"
REM #filters .genome file to only over .9 pihat- this is just for graphing and stuff
REM awk '{if ($8 > 0.9) print $0 }' pihat_min0.2.genome > done_pihat.genome
REM echo FILTERFOUNDERS
REM #filters founders # should bfile be pihat_min-.2 ?
REM #do smth to give option to estimate relatedness for ancestry-adjusted analysis with reap or KING or RelateAdmixed kinship estimations in admixed populations- do visualization
REM plink --allow-no-sex --bfile "data_hwed" --filter-founders --make-bed --out "data_founderfiltered" | grep -e "removed" -e "among remaining"
REM echo FINALPIHAT
REM #pihat on the actual data after founder filtered, showing pihats only over .2
REM plink --allow-no-sex --bfile "data_founderfiltered" --make-bed --genome --min 0.2 --out "pihat_min0.2_in_founders" | grep -e "among remaining"
REM #generate allele frequency for analysis / visualization
REM plink --allow-no-sex --bfile "pihat_min0.2_in_founders" --freq --out "freq" | grep -e "Total genotyping rate"
REM ### GRAPHING TIME BABY ###
REM echo "Graphing Minor Allele Frequency..."

REM Rscript -e "require("tidyverse"); setwd(getwd()); frq <- read.table("\"freq.frq\"", skip=1); pdf("\"freq.pdf\""); hist(frq\$V5);dev.off()"
REM ### MAKE AXIS LABELS WORK AHH main="Minor Allele Frequency Distribution", xlab="Mean Minor Allele Frequency", ylab="Number of SNPs")" ###
REM echo "Graphing hwe..."
REM Rscript -e "require("tidyverse"); setwd(getwd()); hwe <- read.table("\"plink.hwe\"",skip=1); pdf("\"hwe.pdf\""); ggplot(hwe, aes(V9)) +geom_density();dev.off()"
###TODO grep output and simplify to just what got removed and stuff###
###ALSO TODO maybe plot pihat or smth?, install R packages if they aren't, more usability stuff, maybe concatenate graphing funcs ###
case $func in
    recode)
    plink --allow-no-sex --make-bed --recode --vcf "$infile" | echo "recoding to binary..."
    ;;
    geno)
    plink --allow-no-sex --make-bed --geno .04 --bfile "$infile" --out "$outfile" | grep -e "warning" -e "removed"
    ;;
    mind)
    plink --allow-no-sex --make-bed  --mind .05 --bfile "$infile" --out "$outfile" | grep -e "warning" -e "removed" -e "genotyping"
    ;;
    hardyw)
    plink --allow-no-sex --hardy --bfile "$infile" | echo "writing unfiltered hwe data..."
    ;;
    hardyf)
    plink --allow-no-sex --bfile "$infile" --hwe 1e-6 --make-bed --out "$outfile" | grep -e "removed"
    ;;
    pihat)
    plink --allow-no-sex --bfile "$infile" --genome --min 0.2 --out "$outfile" | grep -e "people" -e "excluding" -e "Among remaining" -e "are missing"
    ;;
    filterfounders)
    plink --allow-no-sex --bfile "$infile" --filter-founders --make-bed --out "$outfile" | grep -e "removed" -e "among remaining"
    ;;
    freq)
    plink --allow-no-sex --bfile "$infile" --freq --out "$outfile" | grep -e "Total genotyping rate"
    ;;
    gfreq)
    Rscript -e "require("tidyverse"); setwd(getwd()); frq <- read.table("\"$infile\"", skip=1); pdf("\"$outfile\""); hist(frq\$V5);dev.off()"
    ;;
    ghew)
    Rscript -e "require("tidyverse"); setwd(getwd()); hwe <- read.table("\"$infile\"",skip=1); pdf("\"$outfile\""); ggplot(hwe, aes(V9)) +geom_density();dev.off()"
    ;;