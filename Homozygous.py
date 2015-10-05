from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
import pysam
import sys
import re

def get_genotype(line, number):
     genotype = []
     for x in range(number):
          prob = line[x].split(',')
          if len(prob) > 3:
               return 0
          if int(prob[0]) == 0 and int(prob[1]) >= 0 and int(prob[2]) > 0:
               genotype.append(1)

          if int(prob[0]) > 0 and int(prob[1]) == 0 and int(prob[2]) > 0:
               genotype.append(2)

          if int(prob[0]) > 0 and int(prob[1]) >= 0 and int(prob[2]) == 0:
               genotype.append(3)

          if int(prob[0]) == 0 and int(prob[1]) >= 0 and int(prob[2]) == 0:
               genotype.append(-1)

          if int(prob[0]) > 0 and int(prob[1]) > 0 and int(prob[2]) > 0:
               genotype.append(-1)
     return genotype


def parseCIGAR(CIGAR):

    for op, length in CIGAR:

        if op == 4:
            return 0
        if op == 2:
            return 2
    return 1

def getDel(CIGAR):

    for op, length in CIGAR:

        if op == 2:
            return length
    return 0


def parseMD(MD):

    #parse MD string (cf. SAM Format Specification v1.4-r985)

    mismatches, location, pos = [], [], 0
    for n in re.findall('(\d+|[a-zA-Z|^]+)', MD):
        if n.isalpha():
            mismatches.append(n)
            location.append(pos)
            pos += 1
        #ignore deletions i.e. ^[A-Z] (isalpha() is False)
        elif '^' not in n:
            pos += int(n)

    return mismatches,location

def getPile(samfile, chr, position, alt):
     if position -2 >= 0:
          for pileupcolumn in samfile.pileup(chr, position-2, position+2, stepper="all"):
               if (pileupcolumn.pos + 1) == position:
                    for pileupread in pileupcolumn.pileups:
                         if pileupread.alignment.query_sequence[pileupread.query_position] == alt:
                              return 1
     else:
          return 1
     return 0

record_dict = SeqIO.to_dict(SeqIO.parse(sys.argv[1], "fasta"))

samfile = []

samfile = sys.argv[4].split()

bamnumber = len(samfile)

out = open(sys.argv[3], "w")
snps = open(sys.argv[2], 'r')

for snp in snps:



     snp = snp.strip()

     hold = snp.split()

     if hold[0].startswith('#'):
          out.write(snp)
          out.write('\n')
          continue

     chr = hold[0]
     position = int(hold[1])
     ref = hold[3]
     alt = hold[4]
     PL = re.findall('(?<=\t)(\d+\,\d+\,\d+)', snp)
     genotype = get_genotype(PL,len(PL))
     for x in range(bamnumber):
          falsepositive = 0
          if int(genotype[x]) == 1:

               falsepositive = getPile(pysam.Samfile(samfile[x], "rb"),chr,position,alt)

               if falsepositive == 1:

                    break

     if falsepositive == 1:
          continue
     elif falsepositive == 0:
          out.write(snp)
          out.write('\n')

snps.close()
out.close()
