import sys
import math
import re

def main():

     records = open(sys.argv[1], "r")
     outfile = open(sys.argv[2], "w")
     filter = int(sys.argv[3])
     alleles = float(sys.argv[4])
     cont = int(sys.argv[5])

     for record in records:

          record = record.strip()
          record = record.split()

          if record[0].startswith('#'):
               for x in record:
                    outfile.write("%s\t" % x)
               outfile.write('\n')
               continue


          Info = record[7].split(';')
          if Info[0] == "INDEL":
               for x in record:
                    outfile.write("%s\t" % x)
               outfile.write('\n')
               continue

          for i in range(len(Info)):
               if Info[i].startswith('DP='):
                    DP = Info[i].split('=')
                    Depth = DP[1]
                    Total = Depth
                    ratio = alleles
                    break
               if Info[i].startswith('DP4'):
                    DP = Info[i].split('=')
                    Depth = DP[1].split(',')
                    Total = int(Depth[0]) + int(Depth[1]) + int(Depth[2]) + int(Depth[3])
                    ratio = float(((float(Depth[2]) + float(Depth[3])+1))/((float(Depth[0]) + float(Depth[1])+1)))
                    break

          if Total > filter:
               if ratio >= alleles:
                    if cont == 1:
                         if p < 0.05:
                              for x in record:
                                   outfile.write("%s\t" % x)
                              outfile.write('\n')
                    elif cont == 0:
                         for x in record:
                              outfile.write("%s\t" % x)
                         outfile.write('\n')


     records.close()
     outfile.close()
