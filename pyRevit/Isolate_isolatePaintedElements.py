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

__window__.Close()
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, BuiltInCategory, ElementId, Wall
from System.Collections.Generic import List

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

set = []
curview = uidoc.ActiveGraphicalView
elements = FilteredElementCollector( doc, curview.Id ).WhereElementIsNotElementType().ToElementIds()
for elId in elements:
	el = doc.GetElement( elId )
	if len( list( el.GetMaterialIds(True))) > 0:
		set.append( elId )
	elif isinstance(el, Wall) and el.IsStackedWall:
		memberWalls = el.GetStackedWallMemberIds()
		for mwid in memberWalls:
			mw = doc.GetElement( mwid )
			if len( list( mw.GetMaterialIds(True))) > 0:
				set.append( elId )

t = Transaction(doc, 'Isolate painted Elements') 
t.Start()

curview.IsolateElementsTemporary( List[ElementId]( set ) )

t.Commit()