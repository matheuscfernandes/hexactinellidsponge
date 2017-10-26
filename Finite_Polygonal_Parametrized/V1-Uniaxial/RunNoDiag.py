import numpy as np


oneDiag=False
twoDiag=False
fullDiag=False

execfile('AnalysisV1C.py')

for NUMBEROFSIDES in xrange(3,11):
    for NUMBEROFSYSTEMSPERSIDE in xrange(2,11):
        if (NUMBEROFSIDES % 2 != 1 or NUMBEROFSYSTEMSPERSIDE % 2 != 1):
            print "Running Job: ",(NUMBEROFSIDES,NUMBEROFSYSTEMSPERSIDE)
            FileWrite=open('TwoDiag_Output.txt', 'a+')
            RunSimulation(NUMBEROFSIDES,5,NUMBEROFSYSTEMSPERSIDE,FileWrite)
            FileWrite.close()
