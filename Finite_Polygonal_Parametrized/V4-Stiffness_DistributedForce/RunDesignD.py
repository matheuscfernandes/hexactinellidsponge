import numpy as np


oneDiag=False
twoDiag=False
fullDiag=False

execfile('Analysis.py')

for NUMBEROFSIDES in xrange(3,41):
    for NUMBEROFSYSTEMSPERSIDE in [1]:
        print "Running Job: ",(NUMBEROFSIDES,NUMBEROFSYSTEMSPERSIDE)
        FileWrite=open('DesignD_Output.txt', 'a+')
        if FileCheck(FileWrite,NUMBEROFSIDES,NUMBEROFSYSTEMSPERSIDE):
       		RunSimulation(NUMBEROFSIDES,12,NUMBEROFSYSTEMSPERSIDE,FileWrite)
        FileWrite.close()
