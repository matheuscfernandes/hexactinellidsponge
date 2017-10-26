import numpy as np


oneDiag=True
twoDiag=False
fullDiag=False

execfile('AnalysisV1C.py')

for NUMBEROFSIDES in xrange(11,21):
    for NUMBEROFSYSTEMSPERSIDE in xrange(1,6):
        print "Running Job: ",(NUMBEROFSIDES,NUMBEROFSYSTEMSPERSIDE)
        FileWrite=open('OneDiag_Output.txt', 'a+')
        RunSimulation(NUMBEROFSIDES,12,NUMBEROFSYSTEMSPERSIDE,FileWrite)
        FileWrite.close()
