Mdb()
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

session.journalOptions.setValues(
    replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

execfile('Functions.py')

# MODEL PARAMETERS
# THIS IS THE NUMBER OF DISCRETE SIDES THE CYLINDER HAS
NUMBEROFSYSTEMS = 2
# THIS IS THE NUMBER OF CYLINDERS STACKED ON TOP OF EACH OTHER
NUMBEROFVERTICALSYSTEMS = 8
# THIS IS THE NUMBER OF HALF UNITCELLS THERE ARE IN A SYSTEM
NUMBEROFSIDESPERSYSTEM = 2

spacing = 5E-3
TOL = 10E-8
timePeriod = 1
numberOfTimeSteps = 100.0
rr = 923.88E-6
BaseThickness = spacing / 5.
IntersectionCorrection = TOL * \
    1000.  # correction for the intersection of the 1D trusses to rigid ring
YoungsModulus = 1000.0

nonDiagHalf = False
nonDiagSameVolume = False
# oneDiag=False
# twoDiag=False
nonLinearGeom = True

# RADIUS=NUMBEROFSYSTEMS*2*spacing/(2*math.pi)
# BASED ON RADIUS OF A POLYGON (NOT APOTHEM)
RADIUS = spacing * NUMBEROFSIDESPERSYSTEM / (2 * math.sin(math.pi / (2 * NUMBEROFSYSTEMS)))
ANGLE = 180 * (NUMBEROFSYSTEMS * 2. - 2.) / (NUMBEROFSYSTEMS * 2.)
BaseRadius = RADIUS * 1.05

# CREATING THE GEOMETRY
Model_DimpleStr = mdb.models['Model-1']

# IN THIS CASE THE UNIT-CELLS ARE DISTRIBUTED INTO TWO SEPARATE ARRAYS WHICH WE SEPARATE INTO
# FIRST AND SECOND PART

# CREATING FIRST PART OF UNIT-CELL

# CREATING THE MAIN UNICEL
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
    spacing, 0.0))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, 2 * spacing), point2=(
    0, 0))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, spacing), point2=(
    spacing, spacing))


# CREATING UNICEL FOR THE ONE DIAGONAL PART
if oneDiag:
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing, spacing), point2=(
        0, 2 * spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, spacing), point2=(
        spacing, 2 * spacing))


if fullDiag:
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing, spacing), point2=(
        0, 2 * spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, spacing), point2=(
        spacing, 2 * spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, 0), point2=(
        spacing, spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, spacing), point2=(
        spacing, 0))


# CREATING UNICEL FOR THE TWO DIAGONAL PART
if twoDiag:
    # x1=sqrt(2)*spacing/(sqrt(2)*2)
    x2 = spacing / (sqrt(2) + 2)
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing - x2, 0), point2=(
        spacing, x2))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing, spacing - x2), point2=(
        0, 2 * spacing - x2))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing, spacing + x2), point2=(
        x2, 2 * spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, spacing - x2), point2=(
        spacing, 2 * spacing - x2))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, spacing + x2), point2=(
        spacing - x2, 2 * spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, x2), point2=(
        x2, 0))


mdb.models['Model-1'].Part(dimensionality=THREE_D,
                           name='Part-1', type=DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseWire(
    sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# CREATING SETS FOR THE DIFFERENT DIAMETER SECTIONS
Part_Full = mdb.models['Model-1'].parts['Part-1']
edgeIndex = []
middleIndex = []
diagIndex = []
for ii in range(len(Part_Full.edges)):
    pointOnX = Part_Full.edges[ii].pointOn[0][0]
    pointOnY = Part_Full.edges[ii].pointOn[0][1]
    if pointOnX == spacing or pointOnY == spacing:
        middleIndex.append(Part_Full.edges[ii:ii + 1])
    elif pointOnX == 0.0 or pointOnX == 2 * spacing or pointOnY == 0.0 or pointOnY == 2 * spacing:
        edgeIndex.append(Part_Full.edges[ii:ii + 1])
    else:
        diagIndex.append(Part_Full.edges[ii:ii + 1])
edgeIndex = tuple(edgeIndex + middleIndex)
middleIndex = tuple(middleIndex)
diagIndex = tuple(diagIndex)

if twoDiag or oneDiag or fullDiag:
    Part_Full.Set(name='DIAGONAL', edges=diagIndex)
Part_Full.Set(name='EDGES', edges=edgeIndex)
Part_Full.Set(name='MIDDLE', edges=middleIndex)

# CREATING SECOND PART OF UNIT-CELL

# CREATING THE MAIN UNICEL
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
    spacing, 0.0))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, 2 * spacing), point2=(
    0, 0))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, spacing), point2=(
    spacing, spacing))


# CREATING UNICEL FOR THE ONE DIAGONAL PART
if oneDiag:
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, 0), point2=(
        spacing, spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing, 0), point2=(
        0, spacing))

if fullDiag:
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing, spacing), point2=(
        0, 2 * spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, spacing), point2=(
        spacing, 2 * spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, 0), point2=(
        spacing, spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, spacing), point2=(
        spacing, 0))


# CREATING UNICEL FOR THE TWO DIAGONAL PART
if twoDiag:
    # x1=sqrt(2)*spacing/(sqrt(2)*2)
    x2 = spacing / (sqrt(2) + 2)
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, x2), point2=(
        spacing, spacing + x2))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(x2, 0), point2=(
        spacing, spacing - x2))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing - x2, 0), point2=(
        0, spacing - x2))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing, x2), point2=(
        0, spacing + x2))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, 2 * spacing - x2), point2=(
        x2, 2 * spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing - x2, 2 * spacing), point2=(
        spacing, 2 * spacing - x2))

mdb.models['Model-1'].Part(dimensionality=THREE_D,
                           name='Part-2', type=DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-2'].BaseWire(
    sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# CREATING SETS FOR THE DIFFERENT DIAMETER SECTIONS
Part_Full = mdb.models['Model-1'].parts['Part-2']
edgeIndex = []
middleIndex = []
diagIndex = []
for ii in range(len(Part_Full.edges)):
    pointOnX = Part_Full.edges[ii].pointOn[0][0]
    pointOnY = Part_Full.edges[ii].pointOn[0][1]
    if pointOnX == spacing or pointOnY == spacing:
        middleIndex.append(Part_Full.edges[ii:ii + 1])
    elif pointOnX == 0.0 or pointOnX == 2 * spacing or pointOnY == 0.0 or pointOnY == 2 * spacing:
        edgeIndex.append(Part_Full.edges[ii:ii + 1])
    else:
        diagIndex.append(Part_Full.edges[ii:ii + 1])
edgeIndex = tuple(edgeIndex)
middleIndex = tuple(middleIndex)
diagIndex = tuple(diagIndex)

if twoDiag or oneDiag or fullDiag:
    Part_Full.Set(name='DIAGONAL', edges=diagIndex)
Part_Full.Set(name='EDGES', edges=edgeIndex + middleIndex)
Part_Full.Set(name='MIDDLE', edges=middleIndex)

# BEGINNING CONSTRUCTION OF THE ASSEMBLY OF CYLINDER
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1',
                                            part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-2-1',
                                            part=mdb.models['Model-1'].parts['Part-2'])

# CONSTRUCTION OF ASSEMBLY FOR CASES WHERE THERE ARE ODD NUMBERS OF SIDES PER SYSTEM AND GREATER THAN 1
if NUMBEROFSIDESPERSYSTEM % 2 == 1 and NUMBEROFSIDESPERSYSTEM > 1:
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-2-1', ),
                                                 vector=(spacing, 0.0, 0.0))

    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                         0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-1-1', ), number1=(NUMBEROFSIDESPERSYSTEM + 1) / 2,
                                                             number2=1, spacing1=spacing * 2, spacing2=spacing)
    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                         0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-2-1', ), number1=(NUMBEROFSIDESPERSYSTEM + 1) / 2 - 1,
                                                             number2=1, spacing1=spacing * 2, spacing2=spacing)

    # MERGE ALL PARTS TO FORM NEW PART-3-1
    mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                                instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-3-1', originalInstances=DELETE)
    del mdb.models['Model-1'].rootAssembly.features['Part-3-1-1']

    # CREATING THE SECOND PART OF THE GEOMETRY

    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1',
                                                part=mdb.models['Model-1'].parts['Part-1'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-2-1',
                                                part=mdb.models['Model-1'].parts['Part-2'])

    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-1-1', ),
                                                 vector=(spacing, 0.0, 0.0))

    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                         0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-1-1', ), number1=(NUMBEROFSIDESPERSYSTEM + 1) / 2 - 1,
                                                             number2=1, spacing1=spacing * 2, spacing2=spacing)
    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                         0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-2-1', ), number1=(NUMBEROFSIDESPERSYSTEM + 1) / 2,
                                                             number2=1, spacing1=spacing * 2, spacing2=spacing)

    mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                                instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-3-2', originalInstances=DELETE)

    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-3-1-1',
                                                part=mdb.models['Model-1'].parts['Part-3-1'])

    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-3-2-1', ),
                                                 vector=(-spacing * (NUMBEROFSIDESPERSYSTEM), 0.0, 0.0))


# CONSTRUCTION OF ASSEMBLY FOR CASES WHERE THERE ARE EVEN NUMBERS OF SIDES PER SYSTEM AND GREATER THAN 1
if NUMBEROFSIDESPERSYSTEM % 2 == 0 and NUMBEROFSIDESPERSYSTEM > 1:
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-2-1', ),
                                                 vector=(spacing, 0.0, 0.0))

    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                         0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-1-1', ), number1=(NUMBEROFSIDESPERSYSTEM + 1) / 2,
                                                             number2=1, spacing1=spacing * 2, spacing2=spacing)
    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                         0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-2-1', ), number1=(NUMBEROFSIDESPERSYSTEM + 1) / 2,
                                                             number2=1, spacing1=spacing * 2, spacing2=spacing)

    # MERGE ALL PARTS TO FORM NEW PART-3-1
    mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                                instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-3-1', originalInstances=DELETE)
    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                         0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-3-1-1', ), number1=2,
                                                             number2=1, spacing1=0, spacing2=0.01)
    mdb.models['Model-1'].rootAssembly.features.changeKey(
        fromName='Part-3-1-1-lin-2-1', toName='Part-3-2-1')

    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-3-2-1', ),
                                                 vector=(-spacing * (NUMBEROFSIDESPERSYSTEM), 0.0, 0.0))


# ROTATE THE TWO PARTS
mdb.models['Model-1'].rootAssembly.rotate(angle=(180 - ANGLE) / 2., axisDirection=(0.0, 1.0,
                                                                                   0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-3-1-1', ))
mdb.models['Model-1'].rootAssembly.rotate(angle=-(180 - ANGLE) / 2., axisDirection=(0.0, 1.0,
                                                                                    0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-3-2-1', ))

# MERGE TWO PARTS TO FORM NEW PART-3
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                            instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-3', originalInstances=DELETE)


# TRANSLATE NEW PART AND CREATE CIRCULAR ARRAY AND MERGE
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-3-1', ),
                                             vector=(0.0, 0.0, RADIUS))
mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0),
                                                         instanceList=('Part-3-1', ), number=NUMBEROFSYSTEMS, point=(0.0, 0.0, 0.0), totalAngle=360.0)
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                            instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-3s', originalInstances=DELETE)
mdb.models['Model-1'].rootAssembly.regenerate()

mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(0.0, 1.0,
                                                                     0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-3s-1', ), number1=NUMBEROFVERTICALSYSTEMS,
                                                         number2=1, spacing1=2 * spacing, spacing2=2 * spacing)

mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                            instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-3ss', originalInstances=DELETE)
del mdb.models['Model-1'].rootAssembly.features['Part-3ss-1']
del mdb.models['Model-1'].parts['Part-3s']

del mdb.models['Model-1'].parts['Part-3-1']
try:
    del mdb.models['Model-1'].parts['Part-3-2']
except:
    pass


asdfasdfasdf
# CREATING THE TOP RING
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
    spacing, 0.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D,
                           name='Part-Top', type=DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-Top'].BaseWire(
    sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# WORKING WITH THE EDGES OF THE MODEL
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-Top-1',
                                            part=mdb.models['Model-1'].parts['Part-Top'])
mdb.models['Model-1'].rootAssembly.rotate(angle=(180 - ANGLE) / 2., axisDirection=(0.0, 1.0,
                                                                                   0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-Top-1', ))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-Top-1', ),
                                             vector=(0.0, NUMBEROFVERTICALSYSTEMS * 2 * spacing, RADIUS))
mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0),
                                                         instanceList=('Part-Top-1', ), number=NUMBEROFSYSTEMS * 2, point=(0.0, 0.0, 0.0), totalAngle=360.0)
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                            instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-Top2', originalInstances=DELETE)
del mdb.models['Model-1'].parts['Part-Top']

# ASSIGNING TOP RING EDGES TO SET
Part_Full = mdb.models['Model-1'].parts['Part-Top2']
diagIndex = []
for ii in range(len(Part_Full.edges)):
    diagIndex.append(Part_Full.edges[ii:ii + 1])
Part_Full.Set(name='EDGES', edges=tuple(diagIndex))

# BRING IN REST OF THE PARTS INTO ASSEMBLY AND REGENERATE TO FORM FINAL PRODUCT
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-2-1',
                                            part=mdb.models['Model-1'].parts['Part-3ss'])
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                            instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-4', originalInstances=DELETE)
del mdb.models['Model-1'].parts['Part-3ss']
del mdb.models['Model-1'].parts['Part-Top2']

# CREATE SEEDING AND MESHING PART
mdb.models['Model-1'].parts['Part-4'].seedPart(deviationFactor=0.0001,
                                               minSizeFactor=0.0001, size=0.0005)

# mdb.models['Model-1'].parts['Part-4'].generateMesh()
mdb.models['Model-1'].rootAssembly.regenerate()

# change element type to quadratic interpolation
mdb.models['Model-1'].parts['Part-4'].Set(
    name='ALL-Edges', edges=mdb.models['Model-1'].parts['Part-4'].edges[:])
mdb.models['Model-1'].parts['Part-4'].setElementType(elemTypes=(ElemType(
    elemCode=B32, elemLibrary=STANDARD), ), regions=mdb.models['Model-1'].parts['Part-4'].sets['ALL-Edges'])
mdb.models['Model-1'].parts['Part-4'].generateMesh()
mdb.models['Model-1'].rootAssembly.regenerate()

mdb.models['Model-1'].parts['Part-4'].Set(name='ALL',
                                          nodes=mdb.models['Model-1'].parts['Part-4'].nodes[:])

# CREATE REFERENCE POINTS RIGID BODY FOR BOTTOM BASE
GeometryBottom = 0
GeometryTop = 2 * spacing * NUMBEROFVERTICALSYSTEMS

# CREEATING REFERENCE POINT
mdb.models['Model-1'].Part(dimensionality=THREE_D,
                           name='REF-POINT-BOTTOM', type=DEFORMABLE_BODY)
mdb.models['Model-1'].parts['REF-POINT-BOTTOM'].ReferencePoint(
    point=(0.0, GeometryBottom, 0.0))
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='REF-POINT-BOTTOM',
                                            part=mdb.models['Model-1'].parts['REF-POINT-BOTTOM'])
mdb.models['Model-1'].rootAssembly.Set(name='REF-POINT-BOTTOM', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['REF-POINT-BOTTOM'].referencePoints[1],))

# CREATE REFERENCE POINTS RIGID BODY FOR TOP BASE
# CREEATING REFERENCE POINT

mdb.models['Model-1'].Part(dimensionality=THREE_D,
                           name='REF-POINT-TOP', type=DEFORMABLE_BODY)
mdb.models['Model-1'].parts['REF-POINT-TOP'].ReferencePoint(
    point=(0.0, GeometryTop, 0.0))
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='REF-POINT-TOP',
                                            part=mdb.models['Model-1'].parts['REF-POINT-TOP'])
mdb.models['Model-1'].rootAssembly.Set(name='REF-POINT-TOP', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['REF-POINT-TOP'].referencePoints[1],))

# CREATE TOP AND BOTTOM SETS FOR TYING TO THE REFERENCE POINT
Instance_Full = mdb.models['Model-1'].rootAssembly.instances['Part-4-1']
mdb.models['Model-1'].rootAssembly.Set(name='BOTTOM', nodes=Instance_Full.nodes.getByBoundingBox(
    -RADIUS - TOL, -TOL, -RADIUS - TOL, RADIUS + TOL, TOL, RADIUS + TOL))
mdb.models['Model-1'].rootAssembly.Set(name='TOP', nodes=Instance_Full.nodes.getByBoundingBox(-RADIUS - TOL, 2 * spacing * NUMBEROFVERTICALSYSTEMS - TOL, -RADIUS - TOL,
                                                                                              RADIUS + TOL, 2 * spacing * NUMBEROFVERTICALSYSTEMS + TOL, RADIUS + TOL))

# RIGID BODY TIE
mdb.models['Model-1'].RigidBody(name='BOTTOM-CONSTRAINT', refPointRegion=Region(
    referencePoints=(
        mdb.models['Model-1'].rootAssembly.instances['REF-POINT-BOTTOM'].referencePoints[1],
    )), tieRegion=mdb.models['Model-1'].rootAssembly.sets['BOTTOM'])

mdb.models['Model-1'].RigidBody(name='TOP-CONSTRAINT', refPointRegion=Region(
    referencePoints=(
        mdb.models['Model-1'].rootAssembly.instances['REF-POINT-TOP'].referencePoints[1],
    )), tieRegion=mdb.models['Model-1'].rootAssembly.sets['TOP'])

#####CREATE STEP#######
mdb.models['Model-1'].BuckleStep(name='Buckle',
                                 numEigen=25, previous='Initial', vectors=30)
mdb.models['Model-1'].steps['Buckle'].setValues(maxIterations=300)

# APPLY BOUNDARY CONDITIONS

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, buckleCase=PERTURBATION_AND_BUCKLING, createStepName='Buckle',
                                     distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-BOTTOM', region=Region(referencePoints=(
                                         mdb.models['Model-1'].rootAssembly.instances['REF-POINT-BOTTOM'].referencePoints[1],
                                     )), u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0)


mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, buckleCase=PERTURBATION_AND_BUCKLING, createStepName='Buckle',
                                     distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-TOP', region=Region(referencePoints=(
                                         mdb.models['Model-1'].rootAssembly.instances['REF-POINT-TOP'].referencePoints[1],
                                     )), u1=1.0, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)


# DEFINING MATERIAL PROPERTIES AND SECTION PROPERTIES
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(
    table=((YoungsModulus, 0.0), ))

# CREATE PROFILE AND SECTION ASSIGNMENT - THIS IS FOR THE ROUND CROSSECTION
if oneDiag:  # THIS CASE IS FOR WHEN THERE IS ONE DIAGONAL IN ALTERNATIVE SQUARES
    kl = sqrt(1. / (sqrt(2.) / 2. + 1.))
    REDGES = rr * kl
    RDIAGONALS = rr * kl

elif fullDiag:  # THIS CASE IS FOR WHEN THERE IS ONE DIAGONAL IN EVERY SQUARE
    if fullDiagSame:
        kl = sqrt(1. / (sqrt(2.) + 1.))
        REDGES = rr * kl
        RDIAGONALS = rr * kl
    else:
        kl = sqrt(1. / ((sqrt(2.) / 2.) + 1.))
        REDGES = rr * kl
        RDIAGONALS = rr * kl / sqrt(2.)

elif twoDiag:
    if twoDiagSame:  # THIS IS WHEN THERE IS TWO DIAGONALS WHERE THE VOLUME IS A=B=C1=C2
        kl = sqrt(1. / (sqrt(2.) + 1.))
        REDGES = rr * kl
        RDIAGONALS = rr * kl
    else:  # THIS IS WHEN THERE ARE TWO DIAGONALS WHERE THE VOLUME IS DESCRIBED BY A=B=C1+C2
        kl = sqrt(1. / ((sqrt(2.) / 2.) + 1.))
        REDGES = rr * kl
        RDIAGONALS = rr * kl / sqrt(2.)
else:
    REDGES = rr

# DEFINING SECTION FOR THE EDGES
mdb.models['Model-1'].CircularProfile(name='EDGES', r=REDGES)
mdb.models['Model-1'].BeamSection(consistentMassMatrix=False, integration=DURING_ANALYSIS, material='Material-1', name='EDGES', poissonRatio=0.0,
                                  profile='EDGES', temperatureVar=LINEAR)
mdb.models['Model-1'].parts['Part-4'].SectionAssignment(offset=0.0,
                                                        offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models['Model-1'].parts['Part-4'].sets['EDGES'], sectionName='EDGES', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-2'].assignBeamSectionOrientation(method=N1_COSINES, n1=(
    0.0, 0.0, -1.0), region=mdb.models['Model-1'].parts['Part-4'].sets['EDGES'])


if oneDiag or twoDiag or fullDiag:
    # DEFINING SECTION FOR THE DIAGONAL STRUTS
    mdb.models['Model-1'].CircularProfile(name='DIAGONAL', r=RDIAGONALS)
    mdb.models['Model-1'].BeamSection(consistentMassMatrix=False, integration=DURING_ANALYSIS, material='Material-1', name='DIAGONAL', poissonRatio=0.0,
                                      profile='DIAGONAL', temperatureVar=LINEAR)
    mdb.models['Model-1'].parts['Part-4'].SectionAssignment(offset=0.0,
                                                            offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models['Model-1'].parts['Part-4'].sets['DIAGONAL'], sectionName='DIAGONAL', thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['Part-2'].assignBeamSectionOrientation(method=N1_COSINES, n1=(
        0.0, 0.0, -1.0), region=mdb.models['Model-1'].parts['Part-4'].sets['DIAGONAL'])


mdb.models['Model-1'].rootAssembly.regenerate()
# CREATE JOB AND RUN IT
if oneDiag:
    JobName = "oneDiag"
elif twoDiag:
    JobName = "twoDiag"
    if twoDiagSame:
        JobName = JobName + "Same"
elif fullDiag:
    JobName = "fullDiag"
    if fullDiagSame:
        JobName = JobName + "Same"
else:
    JobName = "noDiag"
if not nonLinearGeom:
    JobName = JobName + "_linear"
DeleteAbaqusFiles(JobName)

mdb.models['Model-1'].rootAssembly.regenerate()
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF,
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF,
        memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF,
        multiprocessingMode=DEFAULT, name=JobName, nodalOutputPrecision=SINGLE,
        numCpus=1, numGPUs=0, queue=None, scratch='', type=ANALYSIS,
        userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs[JobName].submit(consistencyChecking=OFF)
mdb.jobs[JobName].waitForCompletion()

mdb.saveAs(JobName + '.cae')
DeleteAbaqusFilesButODB(JobName)
