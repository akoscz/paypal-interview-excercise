import datetime
import argparse
import json
import random

parser = argparse.ArgumentParser(description="""Generate a dataset of stock ticks.
   Starting data point is:\n
\t["ts": timestamp.now(), "low": 700.89, "high": 701.25, "open": 700.00, "close": 708.20, "volume": 2.75]
   The output is printed to stdout in pretty printed JSON format.
""")
parser.add_argument('-d','--dataPerSec', default=5, help='Potential number of data points per second.  Default: up 5 data points per seconds')
parser.add_argument('-t','--totalDatasetSec', default=300, help='Number of total seconds in the data set.  Default: 300 seconds (5 minutes)')

args = parser.parse_args()

timestamp = int(datetime.datetime.now().strftime('%s'))
dataSet = []
startingDataPoint = {
	"ts"	: timestamp,
	"low"	: 700.89,
	"high"	: 701.25,
	"open"	: 700.00,
	"close"	: 708.20,
	"volume": 2.75
}

dataSet.append(startingDataPoint)

#
def generateNewValue(v, deltaPercent = 10):
	# value went up or down?
	sign = (-1, 1)[random.randrange(2) == 0]
	
	# percent change.  Cap the range between 1.0 and deltaPercent
	percent = random.randrange(1, deltaPercent * 10) / 10.0

	# percentage of the value
	percentOfV = (v * percent) / 100

	# return new value +/- the value of the percentage of v rounded to 2 decimal places
	return round(v + sign * percentOfV, 2)

def generateDataPointForTimestamp(previousDatapoint):
	newDatapoint = previousDatapoint.copy();
	newDatapoint['low'] = generateNewValue(newDatapoint['low'])
	newDatapoint['high'] = generateNewValue(newDatapoint['high'])
	newDatapoint['open'] = generateNewValue(newDatapoint['open'])
	newDatapoint['close'] = generateNewValue(newDatapoint['close'])
	newDatapoint['volume'] = generateNewValue(newDatapoint['volume'])
	
	return newDatapoint

# loop for the total number of seconds we want to generate data for
for t in range(int(args.totalDatasetSec)):
	# increment our timestamp.  Note: t starts at 0
	ts = dataSet[-1]['ts']
	dataSet[-1]['ts'] = ts + t
	# loop for the number of data points per second we need to generate for each timestamp
	for d in range(int(args.dataPerSec)):
		dataSet.append(generateDataPointForTimestamp(dataSet[-1]))

print json.dumps(dataSet, indent=4)
