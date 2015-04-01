# SWEEP
Sliding Window Extraction of Explicit Polymorphisms

##This is a free pipeline open for use, modification, etc.  For allopolyplod species will filter allelic SNPs from homeologous SNPs (false positives).  Validated for 85% accuracy rate by Sanger Sequencing.
##written by Josh Clevenger 2014


  REQUIRED:                                                                                                         
  -b <string>               sorted/indexed bam file of alignments                                                   
  -g <string>               indexed genome                                                                          
  -o <string>               filtered vcf output name                                                                
                                                                                                                    
  OPTIONAL:                                                                                                         
  -s <int>                  genotypic liklihood filtering stringency: default (0): 0 -> low, 1 -> medium, 2 -> high 
  
  -d <int>                  minimum read depth filter per genotype: default (4): 1 - 100                            
  -r <float>                minimum ratio of alternate allele to reference allele: default (0): 0 - 2               
  -w <int>                  window size in bp: default (100) should be <= read length for optimal quality           
  --no_cleanup              does not delete intermediate vcf files: default (FALSE)   
  --ultimate                performs ultimate filtering for all homozygous calls                                                                         checks all reads mapped to base for any alterate allele (will take longer)              
                            REQUIRES Biopython with pysam module installed in your path!!
                            
  -vcf <string>             Optional use an existing vcf file as input                                              
  -num_genotypes <int>      if vcf file is used, enter number of genotypes
                                                                                                                    
                                                                                                                    
  To use this script there are certain requirements:                                                                
                                                                                                                    
  (1) Samtools v0.1.9 and Bcftools v0.1.9 must be in your path -> Will not work with later versions                 
  (2) To do this easily you can add the path in your shell script                                                   
  (3) alignment Bam files must be sorted and indexed                                                                
  (4) Include as many bam files as you need separated with '-b'                                                     
  (5) Option to include previously generated vcf file for SWEEP filtering
  (6) If input is vcf, you must still include bam files and genome for --ultimate filtering
  (7) Example command line:                                                                                         
  
      perl SWEEP.pl -b gen1.sorted.bam -b gen2.sorted.bam -g genome.fa -o output.vcf -s 1 -d 5 -r 0.25              
  
  (8) Example with input vcf:
  
      perl SWEEP.pl -b gen1.sorted.bam -b gen2.sorted.bam -g genome.fa -o output.vcf -s 1 -d 5 -r 0.25 -vcf snps.vcf    
                    -num_genotypes 2
