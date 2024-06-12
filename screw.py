import Rhino
import Grasshopper.Kernel as gh
import Grasshopper.Kernel.Special as gh_special
import System
import clr

clr.AddReference("RhinoCommon")
from Rhino import Geometry, DocObjects

def adjust_slider_by_name(slider_name, value):
    objects = ghenv.Component.OnPingDocument().Objects
    count = 0
    for obj in objects:
        if obj.NickName == slider_name:
            if isinstance(obj, gh_special.GH_NumberSlider):
                obj.Slider.Value = value
                obj.ExpireSolution(True)
                count += 1
    return count

def set_selection_component_value(component_name, value):
    # Iterate through all objects in the Grasshopper document
    for obj in ghenv.Component.OnPingDocument().Objects:
        if obj.NickName == component_name:
            if isinstance(obj, gh_special.GH_ValueList):
                obj.SelectItem(value)
                return

def export_obj(filepath):
    # Get all the Rhino geometry from the Grasshopper document
    rhino_guids = []
    for obj in ghenv.Component.OnPingDocument().Objects:
        if hasattr(obj, 'BakeGeometry'):
            geo_list = []
            obj.BakeGeometry(Rhino.RhinoDoc.ActiveDoc, geo_list)
            for geo in geo_list:
                rhino_guids.append(geo.Id)

    # Convert to System.Collections.Generic.List[System.Guid]
    rhino_guids_clr = System.Collections.Generic.List[System.Guid](rhino_guids)

    # Set the export options
    options = Rhino.FileIO.FileObjWriteOptions()
    options.WriteMaterial = False
    options.WriteTextureCoordinates = False
    options.WriteVertexNormals = False
    options.WriteOpenNURBS = False

    # Export the geometry to an OBJ file
    success = Rhino.FileIO.FileObjWrite(filepath, rhino_guids_clr, options)
    if success:
        print "Successfully exported to {}".format(filepath)
    else:
        print "Failed to export OBJ"

# Adjust sliders
count = adjust_slider_by_name("NUMBER OF TWISTS", 5)
count = adjust_slider_by_name("NUMBER OF POINTS", 100)
count = adjust_slider_by_name("CAP SIZE", 50)
count = adjust_slider_by_name("CAP HEIGHT", 50)
count = adjust_slider_by_name("TWIST SIZE", 5.0)
count = adjust_slider_by_name("TWIST SHAPE", 3.0)
count = adjust_slider_by_name("FILLET", 0.529)
count = adjust_slider_by_name("TWIST SCALE", 0.5)
count = adjust_slider_by_name("offset distance", 0.5)
count = adjust_slider_by_name("diameter", 24)
count = adjust_slider_by_name("scale1", 0.69)
count = adjust_slider_by_name("Height1", 50.0)
count = adjust_slider_by_name("RADIUS1", 30)
count = adjust_slider_by_name("segments1", 9)
count = adjust_slider_by_name("fillet radius1", 3)
count = adjust_slider_by_name("Factor", 5)
count = adjust_slider_by_name("radius", 38)
count = adjust_slider_by_name("Segment", 8)
count = adjust_slider_by_name("Fillet Radius", 10)
count = adjust_slider_by_name("Height", 10)
count = adjust_slider_by_name("Height2", 2.0)
count = adjust_slider_by_name("Scale", 1.59)
count = adjust_slider_by_name("Height3", 7)

# Set selection component value
set_selection_component_value("Selector", 3)

# Export to OBJ
export_obj("~/file.obj")

print "Completed"
