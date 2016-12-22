import bpy
from bpy_extras.io_utils import ExportHelper
import sys
import struct

filepath = 'c:/temp/mai.uv'

with open(filepath,"wb") as fid:
    fid.write(b"ExtendedStl")
    fid.write(struct.pack("I",0))

    for ob in bpy.context.scene.objects:
        print(ob)

        if not (ob.type == "MESH"):
            continue

        for face in ob.data.polygons:
            for vert, loop in zip(face.vertices, face.loop_indices):
                for item in ob.data.vertices[vert].normal:  # normal
                    fid.write(struct.pack("f",item))
                for item in ob.data.vertices[vert].co:  # vertex
                    fid.write(struct.pack("f",item))
                for item in (ob.data.uv_layers.active.data[loop].uv if ob.data.uv_layers.active is not None else (0.0, 0.0)):  # uv
                    fid.write(struct.pack("f",item))
