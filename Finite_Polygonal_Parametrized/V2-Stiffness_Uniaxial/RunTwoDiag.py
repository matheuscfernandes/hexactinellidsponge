import numpy as np


oneDiag=False
twoDiag=True
fullDiag=False

execfile('AnalysisV1C.py')

for NUMBEROFSIDES in xrange(18,21):
    for NUMBEROFSYSTEMSPERSIDE in xrange(1,6):
        print "Running Job: ",(NUMBEROFSIDES,NUMBEROFSYSTEMSPERSIDE)
        FileWrite=open('TwoDiag_Output.txt', 'a+')
        RunSimulation(NUMBEROFSIDES,12,NUMBEROFSYSTEMSPERSIDE,FileWrite)
        FileWrite.close()
