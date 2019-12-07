#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Note: this is not an exhaustive test suite, it does not check the
data structures in detail. It just verifies whether basic
loading and querying of 3d models using pyassimp works.
"""

import os
import sys
import glob

import pyassimp
import pyassimp.postprocess

# Valid extensions for 3D model files.
extensions = [
    ".3ds",
    ".x",
    ".lwo",
    ".obj",
    ".md5mesh",
    ".dxf",
    ".ply",
    ".stl",
    ".dae",
    ".md5anim",
    ".lws",
    ".irrmesh",
    ".nff",
    ".off",
    ".blend",
]
datadirs = [
    "/usr/share/assimp/models/",
    "/usr/share/VTKData/",  # 3DS,OBJ,PLY,STL
    "/usr/share/games/cube2/packages/models",  # OBJ,MD5ANIM,MD5MESH
    "/usr/share/camitk-*/testdata/",  # OBJ,STL,OFF
    "/usr/share/morse/data/",  # DAE,BLEND; there's a crashy blend-file in there!
    "/usr/share/games/lordsawar",  # LWS, but fail to load
    "/usr/share/gdal/",  # DXF, but fail to load
]

badfiles = [
    "/usr/share/assimp/models/invalid/OutOfMemory.off",
]


def myprint(s=""):
    # return
    print(s)


def recur_node(node, level=0):
    myprint("  " + "\t" * level + "- " + str(node))
    for child in node.children:
        recur_node(child, level + 1)


def load(filename=None):
    myprint()
    myprint("trying: " + filename)

    scene = pyassimp.load(
        filename, processing=pyassimp.postprocess.aiProcess_Triangulate
    )

    # the model we load
    print("MODEL: " + filename)

    # write some statistics
    myprint("SCENE:")
    myprint("  meshes:" + str(len(scene.meshes)))
    myprint("  materials:" + str(len(scene.materials)))
    myprint("  textures:" + str(len(scene.textures)))

    myprint("NODES:")
    recur_node(scene.rootnode)

    myprint("MESHES:")
    for index, mesh in enumerate(scene.meshes):
        myprint("  MESH" + str(index + 1))
        myprint("    material id:" + str(mesh.materialindex + 1))
        myprint("    vertices:" + str(len(mesh.vertices)))
        myprint("    first 3 verts:\n" + str(mesh.vertices[:3]))
        if mesh.normals.any():
            myprint("    first 3 normals:\n" + str(mesh.normals[:3]))
        else:
            myprint("    no normals")
        myprint("    colors:" + str(len(mesh.colors)))
        tcs = mesh.texturecoords
        if tcs.any():
            for index, tc in enumerate(tcs):
                myprint(
                    "    texture-coords "
                    + str(index)
                    + ":"
                    + str(len(tcs[index]))
                    + "first3:"
                    + str(tcs[index][:3])
                )

        else:
            myprint("    no texture coordinates")
        myprint("    uv-component-count:" + str(len(mesh.numuvcomponents)))
        myprint(
            "    faces:" + str(len(mesh.faces)) + " -> first:\n" + str(mesh.faces[:3])
        )
        myprint(
            "    bones:"
            + str(len(mesh.bones))
            + " -> first:"
            + str([str(b) for b in mesh.bones[:3]])
        )

    myprint("MATERIALS:")
    for index, material in enumerate(scene.materials):
        myprint("  MATERIAL (id:" + str(index + 1) + ")")
        for key, value in material.properties.items():
            myprint("    %s: %s" % (key, value))

    myprint("TEXTURES:")
    for index, texture in enumerate(scene.textures):
        myprint("  TEXTURE" + str(index + 1))
        myprint("    width:" + str(texture.width))
        myprint("    height:" + str(texture.height))
        myprint("    hint:" + str(texture.achformathint))
        myprint("    data (size):" + str(len(texture.data)))

    # Finally release the model
    pyassimp.release(scene)


def run_tests(basepaths):
    ok, err, bad = 0, 0, 0
    for bpath in basepaths:
        for path in glob.glob(bpath):
            myprint("Looking for models in %s..." % path)
            for root, dirs, files in os.walk(path):
                for afile in files:
                    base, ext = os.path.splitext(afile)
                    if ext in extensions:
                        filename = os.path.join(root, afile)
                        if filename in badfiles:
                            print("Skipping '%s'" % (filename,))
                            continue
                        try:
                            load(filename)
                            ok += 1
                        except pyassimp.errors.AssimpError as error:
                            # Assimp error is fine; this is a controlled case.
                            myprint(error)
                            err += 1
                        except Exception:
                            print(
                                "Error encountered while loading <%s>"
                                % filename
                            )
                            bad += 1
    myprint("** Loaded %s models, got controlled errors for %s files" % (ok, err))
    return bad


if __name__ == "__main__":
    ret = run_tests(sys.argv[1:] or datadirs)
    sys.exit(ret)
