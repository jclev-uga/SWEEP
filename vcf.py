import sys
import re

##usage: python haplotypeSNPs.py input.txt output.txt

def main():
     infile = open(sys.argv[1], "rU")
     outfile = open(sys.argv[2], "w")
     num = int(sys.argv[3])
     win = int(sys.argv[4])

     file = {}
     x = 0

     for line in infile:

          line = line.strip()

          if line[0].startswith('#'):
               outfile.write(line)
               outfile.write('\n')
               continue

          file[x] = line
          x = x + 1


     for line in range(x-2):

          result = window(file[line],file[line+1],num,win)

          if result == 0:
               continue
          elif result == 1:
               outfile.write(file[line])
               outfile.write('\n')
          elif result == 2:
               outfile.write(file[line+1])
               outfile.write('\n')


     infile.close()
     outfile.close()

def window(first,second,num,win):


     one=re.findall('(\d+\,\d+\,\d+)', first)
     two=re.findall('(\d+\,\d+\,\d+)', second)
     first=first.split()
     second=second.split()

     if first[0] == second[0]:
          span = (int(second[1]) - int(first[1]))

          if span <= win:
               genotype1 = get_genotype(one,len(one))
               genotype2 = get_genotype(two,len(two))

               if genotype1 == 0 or genotype2 == 0:
                    return 0
               if len(one) < num or len(two) < num:
                    return 0
               if len(one) > num or len(two) > num:
                    return 0
               for x in range(len(one)):
                    if (genotype1[x] == genotype2[x]):
                         continue
                    else:
                         if genotype1[x] == -1 or genotype2[x] == -1:
                              continue
                         if genotype1[x] == 1:
                              if genotype2[x] == 3:
                                   continue
                              decision = 1
                              for i in range(len(one)):
                                   if genotype2[i] != 2:
                                        decision = 0
                                   if decision == 1:
                                        return 1
                         if genotype2[x] == 1:
                              if genotype1[x] == 3:
                                   continue
                              decision = 1
                              for i in range(len(one)):
                                   if genotype1[i] != 2:
                                        decision = 0
                                   if decision == 1:
                                        return 2
     return 0

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


main()
