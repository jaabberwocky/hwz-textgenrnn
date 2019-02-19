import sys
import os
import re

# command line arguments
if len(sys.argv) != 2:
    raise Exception("Incorrect command-line argument given.")
else:
    try:
        filename = sys.argv[1]
    except:
        raise Exception("Error reading filename.")

# check if cleanedText.txt exists
if os.path.isfile("cleanedText.txt"):
    os.remove("cleanedText.txt")

g = open("cleanedText.txt", "w", encoding="utf-8")

lineCtr = 0

with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        lineCtr += 1
        try:
            if re.match(r'^\s*$', line):
                # nothing found in line
                continue
            elif "Sent from" in line:
                continue
            elif line.split(" ")[1] == "wrote:":
                # skip quotes
                continue
            elif "https://forums.hardwarezone.com.sg/users/" in line:
                continue
        except IndexError:
            pass
        try:   
            s = line.strip()
            print("Writing line : %s" % s)
            g.write(s + "\n")
        except UnicodeDecodeError:
            print("Unicode error, skipping...")

f.close()
g.close()

print("Cleaning complete. %d lines read" % lineCtr)
