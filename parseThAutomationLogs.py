import sys, argparse, datetime

def getListOfLogLines(nameOfFile):
	
	fileHandler = open(nameOfFile)
	return fileHandler.read().splitlines()

# identify blocks of logs for stories
def getNextBlockOfLogs(lines):
	
	block = []
	for line in lines:
		
		if "STORY FAILED:" in line:
			block.append(line)
			break
		if "STORY PASSED:" in line:
			block.append(line)
			break
		block.append(line)
		
	return block


def processLogs(lines):
	listOfBlocks=[]
	for i, line in enumerate(lines):
		if "Running story" in line:
			listOfBlocks.append( getNextBlockOfLogs(lines[i:]) )

	return listOfBlocks
	
# get step names and timeStamps	
def parseStepLine(line):
	lineParts = line.split("\t")
	stepTimeStamp = lineParts[1]
	stepName = " ".join( lineParts[2].split(" ")[1:] )
	
	# escape single quotation marks with double quotation marks
	return (stepName.replace('"', '""' ), stepTimeStamp)

def calculateTimeDifference(time1, time2):
	timeStart = datetime.datetime.strptime(time1, "%d-%b-%Y %H:%M:%S")
	timeEnd   = datetime.datetime.strptime(time2, "%d-%b-%Y %H:%M:%S")
	return timeEnd - timeStart
	

# for each identified block of code, find interesting data items for further processing
def parseBlockOfLogs(block): 

	stepLines = []
	storyName = ""
	storyPathAndName = ""
	executionTime = ""
	storyStartTime = ""
	storyEndTime = ""
	isStoryPassed = False

	for line in block:
		if "Running story" in line:
			storyPathAndName = line.split("Running story ")[1]
			executionTime = line.split("\t")[1]
		if "STARTING STORY:" in line:
			storyName = line.split("\t")[2].split(": ")[1:][0]
			storyStartTime = line.split("\t")[1]
		if "STEP:" in line:
			stepLines.append(parseStepLine(line))
		if "STORY FAILED:" in line:
			stepLines.append(parseStepLine(line))
			storyEndTime = line.split("\t")[1]
		if "STORY PASSED:" in line:
			stepLines.append(parseStepLine(line))
			storyEndTime = line.split("\t")[1]
			isStoryPassed = True
			
	storyExecutionTime = calculateTimeDifference(storyStartTime, storyEndTime).total_seconds()
			
	# identify runtime of each step
	stepTimeDurations = []
	n = len(stepLines)
	for i in range(0,n):
		if i == n-1:
			break
		step = stepLines[i][0]
		startTime = stepLines[i][1]
		endTime   = stepLines[i+1][1]
		stepTime  = calculateTimeDifference(startTime, endTime).total_seconds()
		stepTimeDurations.append((stepTime, step, storyPathAndName))
		
	return ([storyPathAndName, storyExecutionTime, isStoryPassed], stepTimeDurations)		

	
# read the arguments
parser = argparse.ArgumentParser()
parser.add_argument("fileName", help="name of the file containing logs of one single story")
args = parser.parse_args()

# parse the logs
listOfLogLines = getListOfLogLines(args.fileName)
listOfBlocksOfLogs = processLogs(listOfLogLines)

print("Count of log lines to parse {}".format(len(listOfLogLines)) )
print("Number of log blocks {}".format(len(listOfBlocksOfLogs)) )

storyDurations = []
storyStepDurations = []

for block in listOfBlocksOfLogs:
	response = parseBlockOfLogs(block)
	storyDurations.append(response[0])
	storyStepDurations.append(response[1])

# print how long stories take
for storyDuration in storyDurations:
	print( "\"{}\",\"{}\",\"{}\"".format(storyDuration[0], storyDuration[1], storyDuration[2]) )

# print duration of individual steps
for stepTimeDuration in storyStepDurations: 
	for stepInfo in stepTimeDuration:
		print("\"{}\",\"{}\",\"{}\"".format(stepInfo[2], stepInfo[1], stepInfo[0]) )