import numpy as np


oneDiag=False
twoDiag=False
fullDiag=True

execfile('Analysis.py')

for NUMBEROFSIDES in xrange(3,21):
    for NUMBEROFSYSTEMSPERSIDE in xrange(1,6):
        print "Running Job: ",(NUMBEROFSIDES,NUMBEROFSYSTEMSPERSIDE)
        FileWrite=open('DesignC_Output.txt', 'a+')
        if FileCheck(FileWrite,NUMBEROFSIDES,NUMBEROFSYSTEMSPERSIDE):
       		RunSimulation(NUMBEROFSIDES,12,NUMBEROFSYSTEMSPERSIDE,FileWrite)
        FileWrite.close()