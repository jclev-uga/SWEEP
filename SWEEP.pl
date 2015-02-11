use strict;
use warnings;
use threads;
no strict qw(subs refs);

use FindBin;
use lib ("$FindBin::Bin/../PerlLib");
use File::Basename;
use Cwd;
use Carp;
use Getopt::Long qw(:config no_ignore_case pass_through);
use threads;
use Data::Dumper;

my $usage = <<__EOUSAGE__;

######################################################################################################################
#                                                                                                                    #
#  REQUIRED:                                                                                                         #
#  -b <string>               sorted/indexed bam file of alignments                                                   #
#  -g <string>               indexed genome                                                                          #
#  -o <string>               filtered vcf output name                                                                #
#                                                                                                                    #
#  OPTIONAL:                                                                                                         #
#  -s <int>                  genotypic liklihood filtering stringency: default (0): 0 -> low, 1 -> medium, 2 -> high #
#  -d <int>                  minimum read depth filter per genotype: default (4): 1 - 100                            #
#  -r <float>                minimum ratio of alternate allele to reference allele: default (0): 0 - 2               #
#  -w <int>                  window size in bp: default (100) should be <= read length for optimal quality           #
#  --no_cleanup              does not delete intermediate vcf files: default (FALSE)                                 #
#                                                                                                                    #
######################################################################################################################
#                                                                                                                    #
#                                                                                                                    #
#  To use this script there are certain requirements:                                                                #
#                                                                                                                    #
#  (1) Samtools v0.1.9 and Bcftools v0.1.9 must be in your path -> Will not work with later versions                 #
#  (2) To do this easily you can add the path in your shell script                                                   #
#  (3) alignment Bam files must be sorted and indexed                                                                #
#  (4) include as many bam files as you need separated with '-b'                                                     #
#  (5) the vcf file will include at the end of each line a p-value for a genotypic contingency test                  #
#  (6) Example command line:                                                                                         #
#                                                                                                                    #
#      perl SWEEP.pl -b gen1.sorted.bam -b gen2.sorted.bam -g genome.fa -o output.vcf -s 1 -d 5 -r 0.25              #
#                                                                                                                    #
######################################################################################################################




__EOUSAGE__

    ;

my @bamfile;
my $genome;
my $output;
my $stringent=0;
my $filter=4;
my $lh;
my $ratio=0;
my $help_flag;
my $no_cleanup = 0;
my $contingency = 0;
my $window = 100;

&GetOptions ( 'h' => \$help_flag,
              'b=s@' => \@bamfile,
              'g=s' => \$genome,
              'o=s' => \$output,
              's:i' => \$stringent,
              'd:i' => \$filter,
              'r:f' => \$ratio,
              'w:i' => \$window,
              'no_cleanup' => \$no_cleanup,
              'geno_contingency_filter' => \$contingency
              );

if (@ARGV) {
    die "Error, don't understand arguments: @ARGV ";
}

if ($help_flag) { die $usage; }

open (STDERR, ">&STDOUT");  ## capturing stderr and stdout in a single stdout stream

main: {

     if ($stringent == 0) {
          $lh = 20; }
     if ($stringent == 1) {
          $lh = 125; }
     if ($stringent == 2) {
          $lh = 200; }

     my $input_bam = join(' ', @bamfile);
     my $length = 0+@bamfile;
     my $depth = $filter*$length;

     &process_cmd("samtools mpileup -u -f $genome $input_bam | bcftools view -bcv - > temp.raw.bcf");
     &process_cmd("bcftools view temp.raw.bcf > prefilter.vcf");
     &process_cmd("python Haplotype.py prefilter.vcf filter.vcf $length $window");
     &process_cmd("python FindSNP.py filter.vcf stringent.vcf $lh $length");
     &process_cmd("python FilterDepth.py stringent.vcf $output $depth $ratio $contingency");

     unless ($no_cleanup) {

     unlink "temp.raw.bcf";
     unlink "prefilter.vcf";
     unlink "filter.vcf";
     unlink "stringent.vcf";
     }

     exit(0);

}





####
sub process_cmd {
    my ($cmd) = @_;

    print "CMD: $cmd\n";

    my $start_time = time();
    my $ret = system($cmd);
    my $end_time = time();

    if ($ret) {
        die "Error, cmd: $cmd died with ret $ret";
    }

    print "CMD finished (" . ($end_time - $start_time) . " seconds)\n";

    return;
}
