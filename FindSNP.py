import sys

records = open(sys.argv[1], "r")
outfile = open(sys.argv[2], "w")
stringent = int(sys.argv[3])
num = int(sys.argv[4])

for record in records:

     record = record.strip()
     record = record.split()

     if record[0].startswith('#'):
          for x in record:
                outfile.write("%s\t" % x)
          outfile.write('\n')
          continue

     genotypes = {}

     for x in range(9,9+num):
          genotypes.setdefault(x, []).append(record[x].split(':')[1].split(','))
     decision = 0
     for x in range(9,9+num):
          current = genotypes[x]
          if current[0][0] == '0':
               if int(current[0][1]) < 25:
                    decision = 1
          elif current[0][1] == '0':
               if int(current[0][0]) < stringent and int(current[0][2]) < stringent:
                    decision = 1


     if decision == 0:
          for x in record:
               outfile.write("%s\t" % x)
          outfile.write('\n')

records.close()
outfile.close()
