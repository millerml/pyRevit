'''
Copyright (c) 2014-2016 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
'''

import clr
import StringIO
from Autodesk.Revit.DB import *
outputs = StringIO.StringIO()
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

def report(message):
	outputs.write(message)
	outputs.write('\n')

def reportAndPrint(message):
	print(message)
	outputs.write(message)
	outputs.write('\n')

def reportError( elId = 0 ):
	print('< ERROR DELETING ELEMENT ID: {0}>'.format( elId ))

report('PRINTING FULL REPORT -------------------------------------------------------------------\n')

def removeAllConstraints():
	t = Transaction(doc, 'Remove All Constraints') 
	t.Start()
	reportAndPrint('------------------------------- REMOVING ALL CONSTRAINTS -------------------------------\n')
	cl = FilteredElementCollector(doc)
	clconst = list( cl.OfCategory( BuiltInCategory.OST_Constraints ).WhereElementIsNotElementType() )
	for cnst in clconst:
		try:
			doc.Delete(cnst.Id)
		except:
			continue
	t.Commit()

def explodeAndRemoveAllGroups():
	t = Transaction(doc, 'Remove All Groups') 
	t.Start()
	reportAndPrint('---------------------------- EXPLODING AND REMOVING GROUPS -----------------------------\n')
	cl = FilteredElementCollector( doc )
	grpTypes = list( cl.OfClass( clr.GetClrType( GroupType )).ToElements() )
	grps = []
	attachedGrps = []
	for gt in grpTypes:
		for grp in gt.Groups:
			grps.append( grp )
	for g in grps:
		if g.LookupParameter('Attached to'):
			attachedGrps.append( g.GroupType )
		g.UngroupMembers()
	for agt in attachedGrps:
		doc.Delete( agt.Id )
	for gt in grpTypes:
		try:
			doc.Delete( gt.Id )
		except:
			continue
	t.Commit()

def removeAllExternalLinks():
	t = Transaction(doc, 'Remove All External Links') 
	t.Start()
	reportAndPrint('------------------------------ REMOVE ALL EXTERNAL LINKS -------------------------------\n')
	location = doc.PathName
	modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath( location )
	transData = TransmissionData.ReadTransmissionData( modelPath )
	externalReferences = transData.GetAllExternalFileReferenceIds()
	cl = FilteredElementCollector( doc )
	impInstances = list( cl.OfClass( clr.GetClrType( ImportInstance )).ToElements() )
	imported = []
	for refId in externalReferences:
		try:
			lnk = doc.GetElement( refId )
			if isinstance( lnk, RevitLinkType) or isinstance( lnk, CADLinkType ):
				doc.Delete( refId )
		except:
			report('no')
			continue
	t.Commit()

def removeAllSheets():
	t = Transaction(doc, 'Remove All Sheets') 
	t.Start()
	reportAndPrint('----------------------------------- REMOVING SHEETS ------------------------------------\n')
	cl = FilteredElementCollector(doc)
	sheets = cl.OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
	for s in sheets:
		if 'Open_Close' in s.Parameter['Sheet Name'].AsString():
			uidoc.ActiveView = s
			continue
		try:
			report('{2}{0}{1}'.format(
				s.Parameter['Sheet Number'].AsString().rjust(10),
				s.Parameter['Sheet Name'].AsString().ljust(50),
				s.Id,
				))
			doc.Delete( s.Id )
		except:
			reportError()
			continue
	t.Commit()

def removeAllRooms():
	t = Transaction(doc, 'Remove All Rooms') 
	t.Start()
	reportAndPrint('----------------------------------- REMOVING ROOMS -------------------------------------\n')
	cl = FilteredElementCollector(doc)
	rooms = cl.OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()
	for r in rooms:
		try:
			report('{2}{1}{0}'.format(
				r.Parameter['Name'].AsString().ljust(30),
				r.Parameter['Number'].AsString().ljust(20),
				r.Id
				))
			doc.Delete( r.Id )
		except:
			reportError()
			continue
	t.Commit()

def removeAllAreas():
	t = Transaction(doc, 'Remove All Areas') 
	t.Start()
	reportAndPrint('----------------------------------- REMOVING AREAS -------------------------------------\n')
	cl = FilteredElementCollector(doc)
	areas = cl.OfCategory(BuiltInCategory.OST_Areas).WhereElementIsNotElementType().ToElements()
	for a in areas:
		try:
			report('{2}{1}{0}'.format(
				a.ParametersMap['Name'].AsString().ljust(30),
				a.ParametersMap['Number'].AsString().ljust(10),
				a.Id))
			doc.Delete( a.Id )
		except:
			reportError()
			continue
	t.Commit()

def removeAllRoomSeparationLines():
	t = Transaction(doc, 'Remove All Room Separation Lines') 
	t.Start()
	reportAndPrint('------------------------- REMOVING ROOM SEPARATIONS LINES ------------------------------\n')
	cl = FilteredElementCollector(doc)
	rslines = cl.OfCategory(BuiltInCategory.OST_RoomSeparationLines).WhereElementIsNotElementType().ToElements()
	for line in rslines:
		try:
			report('ID: {0}'.format( line.Id ))
			doc.Delete( line.Id )
		except:
			reportError()
			continue
	t.Commit()

def removeAllAreaSeparationLines():
	t = Transaction(doc, 'Remove All Area Separation Lines') 
	t.Start()
	reportAndPrint('------------------------- REMOVING AREA SEPARATIONS LINES ------------------------------\n')
	cl = FilteredElementCollector(doc)
	aslines = cl.OfCategory(BuiltInCategory.OST_AreaSchemeLines).WhereElementIsNotElementType().ToElements()
	for line in aslines:
		try:
			report('ID: {0}'.format( line.Id ))
			doc.Delete( line.Id )
		except:
			reportError()
			continue
	t.Commit()

def removeAllScopeBoxes():
	t = Transaction(doc, 'Remove All ScopeBoxes') 
	t.Start()
	reportAndPrint('------------------------------- REMOVING SCOPE BOXES -----------------------------------\n')
	cl = FilteredElementCollector(doc)
	scopeboxes = cl.OfCategory(BuiltInCategory.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()
	for s in scopeboxes:
		try:
			report('ID: {0}'.format( s.Id ))
			doc.Delete( s.Id )
		except:
			reportError()
			continue
	t.Commit()

def removeAllMaterials():
	t = Transaction(doc, 'Remove All Materials') 
	t.Start()
	reportAndPrint('-------------------------------- REMOVING MATERIALS ------------------------------------\n')
	cl = FilteredElementCollector(doc)
	mats = cl.OfCategory(BuiltInCategory.OST_Materials).WhereElementIsNotElementType().ToElements()
	for m in mats:
		if 'poche' in m.Name.lower():
			continue
		try:
			report('ID: {0}'.format( m.Id ))
			doc.Delete( m.Id )
		except:
			reportError()
			continue
	t.Commit()

def removeAllViews():
	t = Transaction(doc, 'Remove All Views') 
	t.Start()
	reportAndPrint('---------------------- REMOVING VIEWS / LEGENDS / SCHEDULES ----------------------------\n')
	cl = FilteredElementCollector(doc)
	views = set( cl.OfClass( View ).WhereElementIsNotElementType().ToElementIds() )
	for vid in views:
		v = doc.GetElement( vid )
		if isinstance( v, View ):
			if v.ViewType in [	ViewType.ProjectBrowser,
								ViewType.SystemBrowser,
								ViewType.Undefined,
								ViewType.DrawingSheet,
								ViewType.Internal,
								]:
				continue
			if ViewType.ThreeD == v.ViewType and '{3D}' == v.ViewName:
				continue
			if '<' in v.ViewName or  v.IsTemplate: 
				continue
			report('{2}{1}{0}'.format(
				v.ViewName.ljust(50),
				str(v.ViewType).ljust(15),
				str(v.Id).ljust(10),
				))
			doc.Delete( v.Id )
	t.Commit()

def removeAllViewTemplates():
	t = Transaction(doc, 'Remove All View Templates') 
	t.Start()
	reportAndPrint('---------------------------- REMOVING VIEW TEMPLATES -----------------------------------\n')
	cl = FilteredElementCollector(doc)
	views = set( cl.OfClass( View ).WhereElementIsNotElementType().ToElementIds() )
	for vid in views:
		v = doc.GetElement( vid )
		if isinstance( v, View ):
			if v.ViewType in [	ViewType.ProjectBrowser,
								ViewType.SystemBrowser,
								ViewType.Undefined,
								ViewType.DrawingSheet,
								ViewType.Internal,
								]:
				continue
			if v.IsTemplate: 
				report('{2}{1}{0}'.format(
					v.ViewName.ljust(50),
					str(v.ViewType).ljust(15),
					str(v.Id).ljust(10),
					))
			doc.Delete( v.Id )
	t.Commit()

def removeAllElevationMarkers():
	t = Transaction(doc, 'Remove All Elevation Markers') 
	t.Start()
	reportAndPrint('---------------------------- REMOVING ELEVATION MARKERS --------------------------------\n')
	cl = FilteredElementCollector(doc)
	elevMarkers = cl.OfClass(ElevationMarker).WhereElementIsNotElementType().ToElements()
	for em in elevMarkers:
		try:
			report('ID: {0}'.format( em.Id ))
			doc.Delete( em.Id )
		except:
			reportError()
			continue
	t.Commit()

def removeAllFilters():
	t = Transaction(doc, 'Remove All Filters') 
	t.Start()
	reportAndPrint('------------------------------- REMOVING ALL FILTERS -----------------------------------\n')
	cl = FilteredElementCollector(doc)
	filters = cl.OfClass(FilterElement).WhereElementIsNotElementType().ToElements()
	for f in filters:
		try:
			report('ID: {0}'.format( f.Id ))
			doc.Delete( f.Id )
		except:
			reportError()
			continue
	t.Commit()

def callPurgeCommand():
	from Autodesk.Revit.UI import PostableCommand as pc
	from Autodesk.Revit.UI import RevitCommandId as rcid
	cid_PurgeUnused = rcid.LookupPostableCommandId( pc.PurgeUnused )
	__revit__.PostCommand( cid_PurgeUnused )

tg = TransactionGroup( doc, "Purge Model for GC")
tg.Start()

removeAllExternalLinks()
explodeAndRemoveAllGroups()
removeAllConstraints()
# removeAllRooms()
# removeAllRoomSeparationLines()
removeAllAreas()
removeAllAreaSeparationLines()
removeAllScopeBoxes()
removeAllSheets()
removeAllViews()
removeAllElevationMarkers()
removeAllViewTemplates()
removeAllFilters()
removeAllMaterials()

tg.Commit()

callPurgeCommand()

print( outputs.getvalue() )