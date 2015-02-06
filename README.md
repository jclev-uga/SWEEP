# SWEEP
Sliding Window Extraction of Explicit Polymorphisms

##This is free software and is not subject to support.  For allopolyplod species will filter allelic SNPs from homeologous SNPs (false positives).  Has been validated for 85% accuracy rate.
##written by Josh Clevenger 2014

######################################################################################################################
#                                                                                                                    #
  REQUIRED:                                                                                                         #
  -b <string>               sorted/indexed bam file of alignments                                                   #
  -g <string>               indexed genome                                                                          #
  -o <string>               filtered vcf output name                                                                #
                                                                                                                    #
  OPTIONAL:                                                                                                         #
  -s <int>                  genotypic liklihood filtering stringency: default (0): 0 -> low, 1 -> medium, 2 -> high #
  -d <int>                  minimum read depth filter per genotype: default (4): 1 - 100                            #
  -r <float>                minimum ratio of alternate allele to reference allele: default (0): 0 - 2               #
  -w <int>                  window size in bp: default (100) should be <= read length for optimal quality           #
  --no_cleanup              does not delete intermediate vcf files: default (FALSE)                                 #
                                                                                                                    #
                                                                                                                    #
######################################################################################################################
######################################################################################################################
#                                                                                                                    #
#                                                                                                                    #
  To use this script there are certain requirements:                                                                #
                                                                                                                    #
  (1) Samtools v0.1.9 and Bcftools v0.1.9 must be in your path -> Will not work with later versions                 #
  (2) To do this easily you can add the path in your shell script                                                   #
  (3) alignment Bam files must be sorted and indexed                                                                #
  (4) include as many bam files as you need separated with '-b'                                                     #
  (5) Example command line:                                                                                         #
#                                                                                                                    #
      perl SWEEP.pl -b gen1.sorted.bam -b gen2.sorted.bam -g genome.fa -o output.vcf -s 1 -d 5 -r 0.25              #
#                                                                                                                    #
######################################################################################################################
