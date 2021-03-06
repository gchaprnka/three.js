# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# To support reload properly, try to access a package var, if it's there, reload everything
if "bpy" in locals():
    import sys
    reload(sys.modules.get("io_mesh_threejs.export_threejs", sys))


import bpy
from bpy.props import *
from io_utils import ExportHelper


class ExportTHREEJS(bpy.types.Operator, ExportHelper):
    '''Export selected object for Three.js (ASCII JSON format).'''
    bl_idname = "export.threejs"
    bl_label = "Export Three.js"

    filename_ext = ".js"

    use_modifiers = BoolProperty(name="Apply Modifiers", description="Apply modifiers to the exported mesh", default=True)
    use_normals = BoolProperty(name="Normals", description="Export normals", default=True)
    use_colors = BoolProperty(name="Colors", description="Export vertex colors", default=True)
    use_uv_coords = BoolProperty(name="UVs", description="Export texture coordinates", default=True)

    align_types = [("None","None","None"), ("Center","Center","Center"), ("Bottom","Bottom","Bottom"), ("Top","Top","Top")]
    align_model = EnumProperty(name="Align model", description="Align model", items=align_types, default="Center")

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        print("Selected: " + context.active_object.name)

        if not self.properties.filepath:
            raise Exception("filename not set")

        filepath = self.filepath
        import io_mesh_threejs.export_threejs
        return io_mesh_threejs.export_threejs.save(self, context, **self.properties)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self.properties, "use_modifiers")
        row = layout.row()
        row.prop(self.properties, "use_normals")
        row = layout.row()
        row.prop(self.properties, "use_colors")
        row = layout.row()
        row.prop(self.properties, "use_uv_coords")
        row = layout.row()
        row.prop(self.properties, "align_model")


def menu_func(self, context):
    default_path = bpy.data.filepath.replace(".blend", ".js")
    self.layout.operator(ExportTHREEJS.bl_idname, text="Three.js (.js)").filepath = default_path


def register():
    bpy.types.INFO_MT_file_export.append(menu_func)


def unregister():
    bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
