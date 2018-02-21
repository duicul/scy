import sys

print sys.argv
for i in range(1,len(sys.argv)):
	print sys.argv[i]
print "\n"
for i in sys.argv:
	print i

