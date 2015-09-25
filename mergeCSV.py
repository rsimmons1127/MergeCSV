# MergeCSV
# Written by Ryan Simmons (Ryan.Simmons@asu.edu)
#
# This program is for ASU BIO-310 research group. It will take the
# 2 .csv files that are produced from Cowlog and merge them into
# a single .csv file that is needed.

import os, string, sys, time, re, Tkinter, tkFileDialog

def error(errStr):
	print "\nError: ", errStr
	raw_input("Press enter to exit....")
	sys.exit()

files = []
file1Lines = []
file2Lines = []

entryRE = re.compile('\d+\.\d+[, ]+\d+[, ]+\d+')
dateRE = re.compile('\d{4}-\d{2}-\d{2} *\d{2}:\d{2}:\d{2} *')

print "\n\n********************************************"
print "*   MergeCSV                               *"
print "********************************************\n"

# Open dialog to choose files
print "Please select directory containing the 2 .csv files..."
root = Tkinter.Tk()
root.withdraw()
chosenFiles = tkFileDialog.askopenfilenames(parent=root,initialdir="/",title='Please select the 2 .csv files')

# If not 2 files were selected, throw an error
if len(chosenFiles) == 0:
	error("No files were selected")
elif len(chosenFiles) < 2:
	error("Only selected 1 file")
elif len(chosenFiles) >= 3:
	error("Selected " + str(len(chosenFiles)) + " files. Can only have 2")
elif chosenFiles[0].endswith('.csv') == 0 or chosenFiles[1].endswith('.csv') == 0:
	error("1 or more of the selected files are not .csv files")

# Show the selected 2 files
print "Selected ", len(chosenFiles), " files..."
for f in chosenFiles:
	print "\t", f
	files.append(open(f))

# Get all lines of each file
print "\nReading lines from first file..."

file1Text = files[0].read()
file2Text = files[1].read()

f1Entries = entryRE.findall(file1Text)
for line in f1Entries:
	line = re.sub('[, ]+', " ", line)
	file1Lines.append(string.split(line))
	
print "Reading lines from second file..."

f2Entries = entryRE.findall(file2Text)
for line in f2Entries:
	line = re.sub('[, ]+', " ", line)
	file2Lines.append(string.split(line))

f1Date = re.sub('\D+', "", dateRE.findall(file1Text)[0])
f2Date = re.sub('\D+', "", dateRE.findall(file2Text)[0])

if f2Date < f1Date:
	temp = file1Lines
	file1Lines = file2Lines
	file2Lines = temp

# Close both files
files[0].close()
files[1].close()

# Convert string numbers to floating point values and merge
print "Incrementing values in second file..."
for line in file1Lines:
	line[0] = string.atof(line[0])

for line in file2Lines:
	line[0] = round(string.atof(line[0]) + 2793, 2)

# create new file
print "Creating new file, \"merged.csv\"..."
out = open(os.path.dirname(os.path.realpath(chosenFiles[0])) + "/" + 'merged.csv', 'w')

# Write values to new file
print "Writing data to \"merged.csv\"..."
out.write("Time,Behavior,Class\n")
for line in file1Lines:
	out.write(str(line[0]) + "," + line[1] + "," + line[2] + "\n")
for line in file2Lines:
	out.write(str(line[0]) + "," + line[1] + "," + line[2] + "\n")

# Close the output file
print "Closing output file"
out.close()

print "Merge successfully completed!\n"

x = raw_input("Press enter to quit...")
