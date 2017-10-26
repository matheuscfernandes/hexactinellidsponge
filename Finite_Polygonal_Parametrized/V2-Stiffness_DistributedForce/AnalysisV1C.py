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

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

execfile('Functions.py')

# MODEL PARAMETERS
# THIS IS THE NUMBER OF DISCRETE SIDES THE CYLINDER HAS
# NUMBEROFSIDES = 4
# THIS IS THE NUMBER OF CYLINDERS STACKED ON TOP OF EACH OTHER
# NUMBEROFVERTICALSYSTEMS = 10
# THIS IS THE NUMBER OF HALF UNITCELLS THERE ARE IN A SYSTEM
# NUMBEROFSYSTEMSPERSIDE = 2

def RunSimulation(NUMBEROFSIDES,NUMBEROFVERTICALSYSTEMS,NUMBEROFSYSTEMSPERSIDE,FileWrite):
    Mdb()
    NUMBEROFSYSTEMSPERSIDE=2*NUMBEROFSYSTEMSPERSIDE

    spacing = 1
    TOL = 10E-7
    DD = 0.1
    YoungsModulus = 1.
    PoissonsRatio=0.3
    LOAD=1.

    # BASED ON RADIUS OF A POLYGON (NOT APOTHEM)
    RADIUS = spacing * NUMBEROFSYSTEMSPERSIDE / \
        (2 * math.sin(math.pi / (NUMBEROFSIDES)))
    ANGLE = 180 * (NUMBEROFSIDES - 2.) / (NUMBEROFSIDES)

    # DATA VALIDATION FOR INPUT PARATMETERS/ WILL SPIT OUT ERROR IF SOMETHING IS NO CORRECT
    assert not NUMBEROFSIDES < 3,'Cannot have system with less than 3 sides: Problem not posed correctly!'

    assert not NUMBEROFSYSTEMSPERSIDE < 1,'Cannot have less than 1 cell in each system: Problem not posed correctly!'

    assert not NUMBEROFVERTICALSYSTEMS < 2,'Cannot have less than 2 systems high: Implemented code does not support!'

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
    if NUMBEROFSYSTEMSPERSIDE % 2 == 1 and NUMBEROFSYSTEMSPERSIDE > 1:
        mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-2-1', ),
                                                     vector=(spacing, 0.0, 0.0))

        mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                             0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-1-1', ), number1=(NUMBEROFSYSTEMSPERSIDE + 1) / 2,
                                                                 number2=1, spacing1=spacing * 2, spacing2=spacing)
        mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                             0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-2-1', ), number1=(NUMBEROFSYSTEMSPERSIDE + 1) / 2 - 1, number2=1, spacing1=spacing * 2, spacing2=spacing)

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
                                                                             0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-1-1', ), number1=(NUMBEROFSYSTEMSPERSIDE + 1) / 2 - 1, number2=1, spacing1=spacing * 2, spacing2=spacing)
        mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                             0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-2-1', ), number1=(NUMBEROFSYSTEMSPERSIDE + 1) / 2, number2=1, spacing1=spacing * 2, spacing2=spacing)

        mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                                    instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-3-2', originalInstances=DELETE)

        mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-3-1-1',
                                                    part=mdb.models['Model-1'].parts['Part-3-1'])

        mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-3-2-1', ),
                                                     vector=(-spacing * (NUMBEROFSYSTEMSPERSIDE), 0.0, 0.0))


    # CONSTRUCTION OF ASSEMBLY FOR CASES WHERE THERE ARE EVEN NUMBERS OF SIDES PER SYSTEM AND GREATER THAN 1
    if NUMBEROFSYSTEMSPERSIDE % 2 == 0 and NUMBEROFSYSTEMSPERSIDE > 1:
        mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-2-1', ),
                                                     vector=(spacing, 0.0, 0.0))

        mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                             0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-1-1', ), number1=(NUMBEROFSYSTEMSPERSIDE + 1) / 2, number2=1, spacing1=spacing * 2, spacing2=spacing)

        mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0,
                                                                             0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-2-1', ), number1=(NUMBEROFSYSTEMSPERSIDE + 1) / 2,
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
                                                     vector=(-spacing * (NUMBEROFSYSTEMSPERSIDE), 0.0, 0.0))


    # ROTATE THE TWO PARTS
    mdb.models['Model-1'].rootAssembly.rotate(angle=(180 - ANGLE) / 2., axisDirection=(0.0, 1.0,
                                                                                       0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-3-1-1', ))
    mdb.models['Model-1'].rootAssembly.rotate(angle=-(180 - ANGLE) / 2., axisDirection=(0.0, 1.0,
                                                                                        0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-3-2-1', ))

    # TRANSLATE NEW PART AND CREATE CIRCULAR ARRAY AND MERGE
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-3-1-1', ),
                                                 vector=(0.0, 0.0, RADIUS))
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-3-2-1', ),
                                                 vector=(0.0, 0.0, RADIUS))
    if NUMBEROFSIDES % 2 == 1:
        mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0),
                                                                 instanceList=('Part-3-1-1', ), number=int(NUMBEROFSIDES / 2. - 0.5), point=(0.0, 0.0, 0.0), totalAngle=360.0 * ((float(NUMBEROFSIDES) - 3.) / float(NUMBEROFSIDES)))

        mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0),
                                                                 instanceList=('Part-3-2-1', ), number=int(NUMBEROFSIDES / 2. - 0.5), point=(0.0, 0.0, 0.0), totalAngle=360.0 * ((float(NUMBEROFSIDES) - 3.) / float(NUMBEROFSIDES)))

        mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0),
                                                                 instanceList=('Part-3-1-1', ), number=2, point=(0.0, 0.0, 0.0), totalAngle=-360.0 *2./float(NUMBEROFSIDES))

    else:

        mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0),
                                                                 instanceList=('Part-3-1-1', ), number=int(NUMBEROFSIDES / 2), point=(0.0, 0.0, 0.0), totalAngle=360.0)
        mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0),
                                                                 instanceList=('Part-3-2-1', ), number=int(NUMBEROFSIDES / 2), point=(0.0, 0.0, 0.0), totalAngle=360.0)



    mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                                instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-3s', originalInstances=DELETE)
    mdb.models['Model-1'].rootAssembly.regenerate()

    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(0.0, 1.0, 0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-3s-1', ), number1=NUMBEROFVERTICALSYSTEMS, number2=1, spacing1=2 * spacing, spacing2=2 * spacing)

    mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY,
                                                                instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-3ss', originalInstances=DELETE)
    del mdb.models['Model-1'].rootAssembly.features['Part-3ss-1']
    del mdb.models['Model-1'].parts['Part-3s']


    # CREATING THE TOP RING
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        spacing*NUMBEROFSYSTEMSPERSIDE, 0.0))
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
                                                             instanceList=('Part-Top-1', ), number=NUMBEROFSIDES, point=(0.0, 0.0, 0.0), totalAngle=360.0)
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
    mdb.models['Model-1'].parts['Part-4'].seedPart(deviationFactor=0.05,
                                                   minSizeFactor=0.05, size=0.1)

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

    #####CREATE STEP#######
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')


    # CREATING SETS FOR DISTRIBUTED LOAD BOUNDARY CONDITIONS AND BOTTOM BOUNDARY CONDITION
    mdb.models['Model-1'].rootAssembly.Set(name='BOTTOM', vertices=
        mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].vertices.getByBoundingBox(-100*RADIUS,-TOL,-100*RADIUS,100*RADIUS,+TOL,100*RADIUS))
    mdb.models['Model-1'].rootAssembly.Set(name='ALL-VERTECIS', vertices=
        mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].vertices.getByBoundingBox(-100*RADIUS,-TOL,-100*RADIUS,100*RADIUS,+TOL+NUMBEROFVERTICALSYSTEMS*2*spacing,100*RADIUS))
    mdb.models['Model-1'].rootAssembly.Set(name='POINT-SET', vertices=
        mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].vertices.getByBoundingBox(-TOL,2*spacing*NUMBEROFVERTICALSYSTEMS-TOL,RADIUS-TOL,TOL,2*spacing*NUMBEROFVERTICALSYSTEMS+TOL,RADIUS+TOL))

    # GENERATING THE SET FOR THE
    CornerVertices=[]
    if NUMBEROFSIDES==3:
        for i in mdb.models['Model-1'].rootAssembly.sets['ALL-VERTECIS'].nodes:
            if ((sqrt(i.coordinates[0]**2+i.coordinates[2]**2))>(RADIUS-TOL) and not i.coordinates[1]%spacing and i.coordinates[0]>0-TOL and i.coordinates[1]>0):
                CornerVertices.append(i.label)
    else:
        ZDist=RADIUS-(spacing*NUMBEROFSYSTEMSPERSIDE*np.cos(np.radians(ANGLE/2.)))
        for i in mdb.models['Model-1'].rootAssembly.sets['ALL-VERTECIS'].nodes:
            if ((sqrt(i.coordinates[0]**2+i.coordinates[2]**2))>(RADIUS-TOL) and not i.coordinates[1]%spacing and i.coordinates[0]>0-TOL and i.coordinates[2]>ZDist-TOL and i.coordinates[1]>0):
                CornerVertices.append(i.label)

    llabels=tuple(CornerVertices)

    mdb.models['Model-1'].rootAssembly.SetFromNodeLabels(name='LOAD-SET', nodeLabels=(('Part-4-1',llabels),)  )

    CornerVertices=[]
    for i in mdb.models['Model-1'].rootAssembly.sets['BOTTOM'].nodes:
        if ((sqrt(i.coordinates[0]**2+i.coordinates[2]**2))>(RADIUS-TOL)):
            CornerVertices.append(i.label)

    llabels=tuple(CornerVertices)

    mdb.models['Model-1'].rootAssembly.SetFromNodeLabels(name='BOTTOM-SET', nodeLabels=(('Part-4-1',llabels),)  )

    # APPLYING DISTRIBUTED LOAD BOUNDARY CONDITIONS

    mdb.models['Model-1'].ConcentratedForce(cf1=-LOAD*np.cos(np.radians(ANGLE)/2.),cf3=-LOAD*np.sin(np.radians(ANGLE)/2.), createStepName='Step-1',
        distributionType=UNIFORM, field='', localCsys=None, name='LOAD', region=
        mdb.models['Model-1'].rootAssembly.sets['LOAD-SET'])

    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, buckleCase=PERTURBATION_AND_BUCKLING, createStepName='Step-1',
                                         distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-BOTTOM', region=
                                         mdb.models['Model-1'].rootAssembly.sets['BOTTOM-SET'],
                                         u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET)

    # DEFINING MATERIAL PROPERTIES AND SECTION PROPERTIES
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Elastic(
        table=((YoungsModulus, PoissonsRatio), ))

    # CREATE PROFILE AND SECTION ASSIGNMENT - THIS IS FOR THE ROUND CROSSECTION
    if oneDiag:
        REDGES = DD/2.
        RDIAGONALS = REDGES/sqrt(2.)
    elif fullDiag:
        REDGES = DD/2.
        RDIAGONALS = REDGES/2.
    elif twoDiag:
        REDGES = DD/2.
        RDIAGONALS = REDGES/2.
    else:
        REDGES = (DD*sqrt(1.+sqrt(2.)/4.))/2.

    # DEFINING SECTION FOR THE EDGES
    mdb.models['Model-1'].CircularProfile(name='EDGES', r=REDGES)
    mdb.models['Model-1'].BeamSection(consistentMassMatrix=False, integration=DURING_ANALYSIS, material='Material-1', name='EDGES', poissonRatio=0.0,
                                      profile='EDGES', temperatureVar=LINEAR)
    mdb.models['Model-1'].parts['Part-4'].SectionAssignment(offset=0.0,
                                                            offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models['Model-1'].parts['Part-4'].sets['EDGES'], sectionName='EDGES', thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['Part-2'].assignBeamSectionOrientation(method=N1_COSINES, n1=(
        1.0, 1.0, 2.0), region=mdb.models['Model-1'].parts['Part-4'].sets['EDGES'])


    if oneDiag or twoDiag or fullDiag:
        # DEFINING SECTION FOR THE DIAGONAL STRUTS
        mdb.models['Model-1'].CircularProfile(name='DIAGONAL', r=RDIAGONALS)
        mdb.models['Model-1'].BeamSection(consistentMassMatrix=False, integration=DURING_ANALYSIS, material='Material-1', name='DIAGONAL', poissonRatio=0.0,
                                          profile='DIAGONAL', temperatureVar=LINEAR)
        mdb.models['Model-1'].parts['Part-4'].SectionAssignment(offset=0.0,
                                                                offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models['Model-1'].parts['Part-4'].sets['DIAGONAL'], sectionName='DIAGONAL', thicknessAssignment=FROM_SECTION)
        mdb.models['Model-1'].parts['Part-2'].assignBeamSectionOrientation(method=N1_COSINES, n1=(
            1.0, 1.0, 2.0), region=mdb.models['Model-1'].parts['Part-4'].sets['DIAGONAL'])

    mdb.models['Model-1'].parts['Part-4'].assignBeamSectionOrientation(method=
        N1_COSINES, n1=(1.0, 50.0, 2.0), region=
        mdb.models['Model-1'].parts['Part-4'].sets['ALL-Edges'])

    mdb.models['Model-1'].rootAssembly.regenerate()

    # CREATE JOB AND RUN IT
    if oneDiag:
        JobName = "oneDiag"
    elif twoDiag:
        JobName = "twoDiag"
    elif fullDiag:
        JobName = "fullDiag"
    else:
        JobName = "noDiag"

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

    UValues = ExtractU('Part-4-1','Step-1','POINT-SET',JobName)
    Values = [NUMBEROFSIDES, NUMBEROFSYSTEMSPERSIDE/2., NUMBEROFVERTICALSYSTEMS ,LOAD] + UValues

    DeleteAbaqusFiles(JobName)

    FileWrite.write(CreateEString(7) % tuple(Values))
