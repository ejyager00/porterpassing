from laspy.file import File
import numpy as np

inFile = File('/path/to/file.las', mode='r')

I = inFile.Classification == 2

outFile = File('/path/to/output.las', mode='w', header=inFile.header)
outFile.points = inFile.points[I]
outFile.close()