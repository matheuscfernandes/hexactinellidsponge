from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import numpy as np
import math

spacing=5E-3
AppliedDisplacement=.3*0.08

print "PostBuckling Analysis Started"

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

execfile('Functions.py')

JobAll=['noDiag','oneDiag','fullDiag','fullDiagSame','twoDiag','twoDiagSame']
# JobAll=['fullDiag']
for JobName1 in JobAll:
    JobName=JobName1+'_PostBuckling'
    print JobName
    ExtractVirtualPointRF('REF-POINT-TOP','Step-1',JobName,JobName+'_Output.txt',AppliedDisplacement)
