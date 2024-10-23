#!/usr/bin/python3
""" A program to ingest and track logs, periodically printing stats.
"""


from sys import stdin, exit


def printCodeTracking(totalFileSize, codeTracker):
    """ Print formatted log stats.
    """
    # Print total size of data passed to date
    print('File size: ' + str(totalFileSize))

    codeList = sorted(codeTracker.keys())

    # Print formatted count of requests by status code
    for code in codeList:
        if codeTracker[code] != 0:
            print(code + ': ' + str(codeTracker[code]))


codeTracker = {
    '200': 0, '301': 0, '400': 0, '401': 0,
    '403': 0, '404': 0, '405': 0, '500': 0
}
totalFileSize = 0
loopCounter = 0

try:
    for line in stdin:
        # Pull necessary fields from log line
        lineSplit = line.split()

        if len(lineSplit) >= 2:
            statusCode, fileSize = [part for part in lineSplit[-2:]]

            # Update persistent size and status counters
            totalFileSize += int(fileSize)
            if statusCode in codeTracker:
                codeTracker[statusCode] += 1

                # Keep track of how many logs have been read in print loop
                if loopCounter == 9:
                    printCodeTracking(totalFileSize, codeTracker)
                    loopCounter = 0
                else:
                    loopCounter += 1

    # Print stats at end of input stream
    printCodeTracking(totalFileSize, codeTracker)

except KeyboardInterrupt:
    printCodeTracking(totalFileSize, codeTracker)
