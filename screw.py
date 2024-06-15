import Rhino
import Grasshopper.Kernel as gh
import Grasshopper.Kernel.Special as gh_special
import System
import clr

clr.AddReference("RhinoCommon")
from Rhino import Geometry, DocObjects
from System import Array, Guid
from System.Collections.Generic import List

def adjust_slider_by_name(slider_name, value):
    objects = ghenv.Component.OnPingDocument().Objects
    count = 0
    for obj in objects:
        if obj.NickName == slider_name:
            if isinstance(obj, gh_special.GH_NumberSlider):
                obj.Slider.Value = value
                obj.ExpireSolution(True)
                count += 1
                print("Adjusted slider '{}' to value {}".format(slider_name, value))
    return count

def set_selection_component_value(component_name, value):
    for obj in ghenv.Component.OnPingDocument().Objects:
        if obj.NickName == component_name:
            if isinstance(obj, gh_special.GH_ValueList):
                obj.SelectItem(value)
                print("Set selection component '{}' to value {}".format(component_name, value))
                return

def export_obj(filepath):
    geometries = []
    for obj in ghenv.Component.OnPingDocument().Objects:
        if obj.NickName.startswith('Export'):
            geo_list = List[Guid]()
            obj.BakeGeometry(Rhino.RhinoDoc.ActiveDoc, geo_list)
            for geo in geo_list:
                rhino_obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(geo)
                if rhino_obj:
                    geometry = rhino_obj.Geometry
                    if isinstance(geometry, Geometry.Mesh):
                        geometries.append(geometry)
                    else:
                        # Convert geometry to mesh if it's not already a mesh
                        meshes = Geometry.Mesh.CreateFromBrep(geometry) if isinstance(geometry, Geometry.Brep) else None
                        if meshes:
                            geometries.extend(meshes)

    rhino_meshes_clr = Array[Geometry.Mesh](geometries)

    # Set the export options
    write_options = Rhino.FileIO.FileWriteOptions()
    write_options.WriteSelectedObjectsOnly = True
    write_options.SuppressDialogBoxes = True
    options = Rhino.FileIO.FileObjWriteOptions(write_options)

    success = Rhino.FileIO.FileObj.Write(filepath, rhino_meshes_clr, options)
    if success:
        print("Successfully exported to {}".format(filepath))
    else:
        print("Failed to export OBJ to {}".format(filepath))

# Adjust sliders
adjust_slider_by_name("NUMBER OF TWISTS", 5)
adjust_slider_by_name("NUMBER OF POINTS", 100)
adjust_slider_by_name("CAP SIZE", 50)
adjust_slider_by_name("CAP HEIGHT", 50)
adjust_slider_by_name("TWIST SIZE", 5.0)
adjust_slider_by_name("TWIST SHAPE", 3.0)
adjust_slider_by_name("FILLET", 0.529)
adjust_slider_by_name("TWIST SCALE", 0.5)
adjust_slider_by_name("offset distance", 0.5)
adjust_slider_by_name("diameter", 24)
adjust_slider_by_name("scale1", 0.69)
adjust_slider_by_name("Height1", 50.0)
adjust_slider_by_name("RADIUS1", 30)
adjust_slider_by_name("segments1", 9)
adjust_slider_by_name("fillet radius1", 3)
adjust_slider_by_name("Factor", 5)
adjust_slider_by_name("radius", 38)
adjust_slider_by_name("Segment", 8)
adjust_slider_by_name("Fillet Radius", 10)
adjust_slider_by_name("Height", 10)
adjust_slider_by_name("Height2", 2.0)
adjust_slider_by_name("Scale", 1.59)
adjust_slider_by_name("Height3", 7)

# Set selection component value
set_selection_component_value("Selector", 3)

# Export to OBJ with absolute path
export_obj("/Users/zhangligao/file3.obj")

print("Completed")
