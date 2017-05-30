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
import time

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

execfile('Functions.py')

TOL=10E-6
spacing=1.
Strain_Y=-0.1
rr=0.1
YoungsModulus=1.0
PoissonsRatio=0.0
JobName="ParametrizedDiag"

SeparationAll=np.array([0.001,0.25/2.,0.25,0.25*3/2.,0.5])*spacing

ct=-1
for Separation in SeparationAll:
    Mdb()
    ct+=1
    file = open(JobName+str(ct)+'_D_Output.txt', 'w')
    file2 = open(JobName+str(ct)+'_RF_Output.txt', 'w')
    #CREATING THE MAIN UNICEL
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)

    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, spacing/2.), point2=(
        2.*spacing, spacing/2.))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, 3.*spacing/2.), point2=(
        2.*spacing, 3.*spacing/2.))

    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(spacing/2., 0), point2=(
        spacing/2., 2.*spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(3.*spacing/2., 0), point2=(
        3.*spacing/2., 2.*spacing))

    # CREATING UNICEL FOR THE TWO DIAGONAL PART

    shift=(spacing/2.-Separation);

    sp1=spacing/2.+shift;
    sp2=spacing+spacing/2.-shift;

    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, sp1), point2=(
        sp1, 0))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, sp2), point2=(
        sp2, 0))

    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(sp2, 0), point2=(
        2*spacing, sp1))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(sp1,0), point2=(
        2*spacing, sp2))

    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(2*spacing, sp1), point2=(
        sp1, 2*spacing))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(2*spacing,sp2), point2=(
        sp2, 2*spacing))

    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(sp2, 2*spacing), point2=(
        0, sp1))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(sp1, 2*spacing), point2=(
        0, sp2))

    mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Part-1'].BaseWire(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']

    #CREATING INSTANCE AND MESHING
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    Instant_Full=mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1',
        part=mdb.models['Model-1'].parts['Part-1'])
    mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1,
        minSizeFactor=0.1, size=0.1)
    # mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1,
    #     minSizeFactor=1., size=1.)
    mdb.models['Model-1'].parts['Part-1'].Set(name='ALL',edges=mdb.models['Model-1'].parts['Part-1'].edges[:])
    mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
        elemCode=B22, elemLibrary=STANDARD), ), regions=mdb.models['Model-1'].parts['Part-1'].sets['ALL'])
    mdb.models['Model-1'].parts['Part-1'].generateMesh()

    #CREATING STEP
    mdb.models['Model-1'].StaticStep(maxNumInc=1000, name='Step-1', previous=
        'Initial')

    #CREATING SETS
    Part_Full = mdb.models['Model-1'].parts['Part-1']

    Part_Full.Set(name='Mid_SingleNode', nodes=
    	Part_Full.nodes.getByBoundingBox(spacing/2. - TOL, spacing/2. - TOL, -TOL, spacing/2. + TOL, spacing/2. + TOL, TOL) )
    Part_Full.Set(name='Down_Nodes', nodes=
    	Part_Full.nodes.getByBoundingBox(0 - TOL, 0 - TOL, -TOL, 2*spacing - TOL, 0 + TOL, TOL) )
    Part_Full.Set(name='Up_Nodes', nodes=
    	Part_Full.nodes.getByBoundingBox(0 - TOL, 2*spacing - TOL, -TOL, 2*spacing - TOL, 2*spacing + TOL, TOL) )
    Part_Full.Set(name='Left_Nodes', nodes=
    	Part_Full.nodes.getByBoundingBox(0 - TOL, 0 - TOL, -TOL, 0 + TOL, 2*spacing - TOL, TOL) )
    Part_Full.Set(name='Right_Nodes', nodes=
    	Part_Full.nodes.getByBoundingBox(2*spacing - TOL, 0 - TOL, -TOL, 2*spacing + TOL, 2*spacing - TOL, TOL) )

    mdb.models['Model-1'].rootAssembly.regenerate()
    Instance_Full = mdb.models['Model-1'].rootAssembly.instances['Part-1-1']

    mdb.models['Model-1'].rootAssembly.Set(name='Mid_SingleNode', nodes=
    	Instance_Full.nodes.getByBoundingBox(spacing/2. - TOL, spacing/2. - TOL, -TOL, spacing/2. + TOL, spacing/2. + TOL, TOL) )
    mdb.models['Model-1'].rootAssembly.Set(name='Down_Nodes', nodes=
    	Instance_Full.nodes.getByBoundingBox(0 - TOL, 0 - TOL, -TOL, 2*spacing - TOL, 0 + TOL, TOL) )
    mdb.models['Model-1'].rootAssembly.Set(name='Up_Nodes', nodes=
    	Instance_Full.nodes.getByBoundingBox(0 - TOL, 2*spacing - TOL, -TOL, 2*spacing - TOL, 2*spacing + TOL, TOL) )
    mdb.models['Model-1'].rootAssembly.Set(name='Left_Nodes', nodes=
    	Instance_Full.nodes.getByBoundingBox(0 - TOL, 0 - TOL, -TOL, 0 + TOL, 2*spacing - TOL, TOL) )
    mdb.models['Model-1'].rootAssembly.Set(name='Right_Nodes', nodes=
    	Instance_Full.nodes.getByBoundingBox(2*spacing - TOL, 0 - TOL, -TOL, 2*spacing + TOL, 2*spacing - TOL, TOL) )

    mdb.models['Model-1'].rootAssembly.Set(name='AllEdgeNode', nodes=[
        Instance_Full.nodes.getByBoundingBox(0 - TOL, 0 - TOL, -TOL, 2*spacing - TOL, 0 + TOL, TOL),
        Instance_Full.nodes.getByBoundingBox(0 - TOL, 2*spacing - TOL, -TOL, 2*spacing + TOL, 2*spacing + TOL, TOL),
        Instance_Full.nodes.getByBoundingBox(0 - TOL, 0 - TOL, -TOL, 0 + TOL, 2*spacing + TOL, TOL),
        Instance_Full.nodes.getByBoundingBox(2*spacing - TOL, 0 - TOL, -TOL, 2*spacing + TOL, 2*spacing + TOL, TOL)
        ])

    mdb.models['Model-1'].rootAssembly.Set(name='AllNode', nodes=
        Instance_Full.nodes.getByBoundingBox(-3*spacing - TOL, -3*spacing - TOL, -TOL, 3*spacing - TOL, 3*spacing + TOL, TOL))

    edgeIndex=[]
    diagIndex=[]
    for ii in range(len(Part_Full.edges)):
        pointOnX=Part_Full.edges[ii].pointOn[0][0]
        pointOnY=Part_Full.edges[ii].pointOn[0][1]
        if pointOnX==spacing/2. or pointOnX==3.*spacing/2. or pointOnY==spacing/2. or pointOnY==3.*spacing/2.:
            edgeIndex.append(Part_Full.edges[ii:ii+1])
        else:
            diagIndex.append(Part_Full.edges[ii:ii+1])
    edgeIndex=tuple(edgeIndex)
    diagIndex=tuple(diagIndex)

    Part_Full.Set(name='DIAGONAL', edges=diagIndex)
    Part_Full.Set(name='EDGES', edges=edgeIndex)

    (NameRef1, NameRef2, repConst)=PeriodicBound2D(mdb,'Model-1','AllEdgeNode',[(2.0*spacing,0.0),(0.0,2.0*spacing)])

    #CREATE NODE SETS IN THE VIRTUAL POINT NODES TO EXTRACT THE REACTION FORCE
    mdb.models['Model-1'].parts[NameRef1].Set(name='Set-1', referencePoints=(
        mdb.models['Model-1'].parts[NameRef1].referencePoints[1], ))

    #CREATE NODE SETS IN THE VIRTUAL POINT NODES TO EXTRACT THE REACTION FORCE
    mdb.models['Model-1'].parts[NameRef2].Set(name='Set-1', referencePoints=(
        mdb.models['Model-1'].parts[NameRef2].referencePoints[1], ))

    # DEFINING MATERIAL PROPERTIES AND SECTION PROPERTIES
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((YoungsModulus, PoissonsRatio), ))

    REDGES=rr
    RDIAGONALS=rr/2.

    # DEFINING SECTION FOR EDGE STRUTS (NON-DIAGONAL)
    mdb.models['Model-1'].CircularProfile(name='EDGES', r=REDGES)
    mdb.models['Model-1'].BeamSection(consistentMassMatrix=False, integration=
        DURING_ANALYSIS, material='Material-1', name='EDGES', poissonRatio=0.0,
        profile='EDGES', temperatureVar=LINEAR)
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0,
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part-1'].sets['EDGES'], sectionName=
        'EDGES', thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['Part-1'].assignBeamSectionOrientation(method=
        N1_COSINES, n1=(0.0, 0.0, -1.0), region=
        mdb.models['Model-1'].parts['Part-1'].sets['EDGES'])

    # DEFINING SECTION FOR THE DIAGONAL STRUTS
    mdb.models['Model-1'].CircularProfile(name='DIAGONAL', r=RDIAGONALS)
    mdb.models['Model-1'].BeamSection(consistentMassMatrix=False, integration=
        DURING_ANALYSIS, material='Material-1', name='DIAGONAL', poissonRatio=0.0,
        profile='DIAGONAL', temperatureVar=LINEAR)
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0,
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part-1'].sets['DIAGONAL'], sectionName=
        'DIAGONAL', thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['Part-1'].assignBeamSectionOrientation(method=
        N1_COSINES, n1=(0.0, 0.0, -1.0), region=
        mdb.models['Model-1'].parts['Part-1'].sets['DIAGONAL'])


    #APPLY BC
    #Apply boundary conditions on reference nodes
    THETAALL=np.linspace(0,1,30)*90.

    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1',
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-FIXNODE', region=Region(
        nodes=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].nodes.getByBoundingSphere(center=(spacing/2.,spacing/2.,0), radius=TOL)),
        u1=0.0, u2=0.0, ur3=0.0)

    for THETA in THETAALL:
        # mdb.models['Model-1'].ConcentratedForce(cf1=UNSET,cf2=10 ,createStepName='Step-1',
     #        distributionType=UNIFORM, field='', localCsys=None, name='Load-Ref-2', region=
     #        Region(referencePoints=(mdb.models['Model-1'].rootAssembly.instances[NameRef2].referencePoints[1],)))

        mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1',
            distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
            'BC-REF-1', region=Region(referencePoints=(
            mdb.models['Model-1'].rootAssembly.instances[NameRef1].referencePoints[1],
            )), u1=UNSET, u2=UNSET, ur3=UNSET)

        mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1',
            distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
            'BC-REF-2', region=Region(referencePoints=(
            mdb.models['Model-1'].rootAssembly.instances[NameRef2].referencePoints[1],
            )), u1=UNSET, u2=Strain_Y, ur3=UNSET)

        mdb.models['Model-1'].rootAssembly.rotate(angle=THETA, axisDirection=(0.0, 0.0,
            1.0), axisPoint=(spacing, spacing, 0.0), instanceList=('Part-1-1', ))

        UpdatePeriodicBound2D(mdb,'Model-1',NameRef1,NameRef2,repConst)

        mdb.models['Model-1'].Equation(name='RefPoint-Couple1', terms=((1.0,NameRef1, 2),(-1.0, NameRef2, 1)))

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


        time.sleep(10)

        [Time,DXX,DXY]=ExtractVirtualPointU(NameRef1,'Step-1','Set-1',JobName)
        [Time,DYX,DYY]=ExtractVirtualPointU(NameRef2,'Step-1','Set-1',JobName)

        [TimeS,SXX,SXY]=ExtractVirtualPointRF(NameRef1,'Step-1','Set-1',JobName)
        [TimeS,SYX,SYY]=ExtractVirtualPointRF(NameRef2,'Step-1','Set-1',JobName)


        file.write('%e %e %e %e %e %e %e\r\n' % (Time, Separation/spacing, THETA, DXX, DXY, DYX, DYY))
        file2.write('%e %e %e %e %e %e %e\r\n' % (TimeS, Separation/spacing, THETA, SXX, SXY, SYX, SYY))

        mdb.models['Model-1'].rootAssembly.rotate(angle=-THETA, axisDirection=(0.0, 0.0,
            1.0), axisPoint=(spacing, spacing, 0.0), instanceList=('Part-1-1', ))

        DeleteAbaqusFilesButODB(JobName)

    file.close()
    file2.close()
