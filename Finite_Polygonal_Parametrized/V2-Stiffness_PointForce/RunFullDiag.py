import numpy as np


oneDiag=False
twoDiag=False
fullDiag=True

execfile('AnalysisV1C.py')

for NUMBEROFSIDES in xrange(3,21):
    for NUMBEROFSYSTEMSPERSIDE in xrange(1,6):
        print "Running Job: ",(NUMBEROFSIDES,NUMBEROFSYSTEMSPERSIDE)
        FileWrite=open('FullDiag_Output.txt', 'a+')
        RunSimulation(NUMBEROFSIDES,12,NUMBEROFSYSTEMSPERSIDE,FileWrite)
        FileWrite.close()
