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

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

def DeleteAbaqusFiles(Job):
	try:
		os.remove(Job+'.odb')
	except: pass

	try:
		os.remove(Job+'.dat')
	except: pass

	try:
		os.remove(Job+'.com')
	except: pass

	try:
		os.remove(Job+'.ipm')
	except: pass

	try:
		os.remove(Job+'.log')
	except: pass

	try:
		os.remove(Job+'.prt')
	except: pass

	try:
		os.remove(Job+'.sim')
	except: pass

	try:
		os.remove(Job+'.sta')
	except: pass

	# try:
	# 	os.remove(Job+'.msg')
	# except: pass

	try:
		os.remove(Job+'.lck')
	except: pass

def DeleteAbaqusFilesButODB(Job):
	try:
		os.remove(Job+'.dat')
	except: pass

	try:
		os.remove(Job+'.com')
	except: pass

	try:
		os.remove(Job+'.ipm')
	except: pass

	try:
		os.remove(Job+'.log')
	except: pass

	try:
		os.remove(Job+'.prt')
	except: pass

	try:
		os.remove(Job+'.sim')
	except: pass

	try:
		os.remove(Job+'.sta')
	except: pass

	# try:
	# 	os.remove(Job+'.msg')
	# except: pass

	try:
		os.remove(Job+'.lck')
	except: pass


def CreateEString(Number):
    string = '%e'
    for i in xrange(1, Number):
        string += ' %e'
    string += '\r\n'
    return string


def ExtractU(instancename, NameStep, setname, JobName):
	odb = openOdb(path=JobName + '.odb')
	Frame = odb.steps[NameStep].frames[-1]
	set = odb.rootAssembly.nodeSets[setname.upper()]
	displacement = Frame.fieldOutputs['U'].getSubset(region=set).values

	xDisp = displacement[0].data[0]
	yDisp = displacement[0].data[1]
	zDisp = displacement[0].data[2]

	odb.close()

	return [xDisp, yDisp, zDisp]
