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

import logging

logging.basicConfig(stream=sys.stdout, format="%(message)s")
log = logging.getLogger("PyAssimp-Test")

# Valid extensions for 3D model files ('assimp listext')
extensions = [
    ".3d",
    ".3ds",
    ".3mf",
    ".ac",
    ".ac3d",
    ".acc",
    ".amf",
    ".ase",
    ".ask",
    ".assbin",
    ".b3d",
    ".blend",
    ".bvh",
    ".cob",
    ".csm",
    ".dae",
    ".dxf",
    ".enff",
    ".fbx",
    ".glb",
    ".gltf",
    ".hmp",
    ".ifc",
    ".ifczip",
    ".irr",
    ".irrmesh",
    ".lwo",
    ".lws",
    ".lxo",
    ".md2",
    ".md3",
    ".md5anim",
    ".md5camera",
    ".md5mesh",
    ".mdc",
    ".mdl",
    ".mesh",
    ".mesh.xml",
    ".mot",
    ".ms3d",
    ".ndo",
    ".nff",
    ".obj",
    ".off",
    ".ogex",
    ".pk3",
    ".ply",
    ".pmx",
    ".prj",
    ".q3o",
    ".q3s",
    ".raw",
    ".scn",
    ".sib",
    ".smd",
    ".stl",
    ".stp",
    ".ter",
    ".uc",
    ".vta",
    ".x",
    ".x3d",
    ".x3db",
    ".xgl",
    ".xml",
    ".zae",
    ".zgl",
]

badfiles = [
    "/usr/share/assimp/models/invalid/OutOfMemory.off",
]


def recur_node(node, level=0):
    log.info("  " + "\t" * level + "- " + str(node))
    for child in node.children:
        recur_node(child, level + 1)


def load(filename=None):
    log.warning("trying: " + filename)

    scene = pyassimp.load(
        filename, processing=pyassimp.postprocess.aiProcess_Triangulate
    )

    # the model we load
    log.info("MODEL: " + filename)

    # write some statistics
    log.info("SCENE:")
    log.info("  meshes:" + str(len(scene.meshes)))
    log.info("  materials:" + str(len(scene.materials)))
    log.info("  textures:" + str(len(scene.textures)))

    log.info("NODES:")
    recur_node(scene.rootnode)

    log.info("MESHES:")
    for index, mesh in enumerate(scene.meshes):
        log.info("  MESH" + str(index + 1))
        log.info("    material id:" + str(mesh.materialindex + 1))
        log.info("    vertices:" + str(len(mesh.vertices)))
        log.info("    first 3 verts:\n" + str(mesh.vertices[:3]))
        if mesh.normals.any():
            log.info("    first 3 normals:\n" + str(mesh.normals[:3]))
        else:
            log.info("    no normals")
        log.info("    colors:" + str(len(mesh.colors)))
        tcs = mesh.texturecoords
        if tcs.any():
            for index, tc in enumerate(tcs):
                log.info(
                    "    texture-coords "
                    + str(index)
                    + ":"
                    + str(len(tcs[index]))
                    + "first3:"
                    + str(tcs[index][:3])
                )

        else:
            log.info("    no texture coordinates")
        log.info("    uv-component-count:" + str(len(mesh.numuvcomponents)))
        log.info(
            "    faces:" + str(len(mesh.faces)) + " -> first:\n" + str(mesh.faces[:3])
        )
        log.info(
            "    bones:"
            + str(len(mesh.bones))
            + " -> first:"
            + str([str(b) for b in mesh.bones[:3]])
        )

    log.info("MATERIALS:")
    for index, material in enumerate(scene.materials):
        log.info("  MATERIAL (id:" + str(index + 1) + ")")
        for key, value in material.properties.items():
            log.info("    %s: %s" % (key, value))

    log.info("TEXTURES:")
    for index, texture in enumerate(scene.textures):
        log.info("  TEXTURE" + str(index + 1))
        log.info("    width:" + str(texture.width))
        log.info("    height:" + str(texture.height))
        log.info("    hint:" + str(texture.achformathint))
        log.info("    data (size):" + str(len(texture.data)))

    # Finally release the model
    pyassimp.release(scene)
    log.info("====================================")


def run_tests(basepaths, excluded=[]):
    ok, err, bad = 0, 0, 0

    def do_load(filename, excluded, extensions):
        nonlocal ok
        nonlocal err
        nonlocal bad
        if filename in excluded:
            log.warning("Skipping '%s'" % (filename,))
            return
        _, ext = os.path.splitext(filename)
        if not ext in extensions:
            return
        try:
            load(filename)
            ok += 1
        except pyassimp.errors.AssimpError as error:
            # Assimp error is fine; this is a controlled case.
            log.exception("Error encountered while loading '%s'" % (filename,))
            err += 1
        except Exception as e:
            try:
                errtype = type(e).__name__
            except:
                errtype = ""
            log.exception(
                "Error<%s> encountered while loading '%s': %s" % (errtype, filename, e)
            )
            bad += 1

    for bpath in basepaths:
        for path in glob.glob(bpath):
            if os.path.isfile(path):
                do_load(path, excluded, extensions)
            else:
                log.warning("Looking for models in %s..." % path)
                for root, dirs, files in os.walk(path):
                    for afile in files:
                        do_load(os.path.join(root, afile), excluded, extensions)
    log.warning(
        "** Loaded %s models, got %s assimp errors and %s other errors" % (ok, err, bad)
    )
    return 0


def parseCmdlineArgs():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="count", help="raise verbosity", default=0
    )
    parser.add_argument(
        "-q", "--quiet", action="count", help="lower verbosity", default=0
    )

    parser.add_argument(
        "--extensions",
        action="append",
        help="only try loading models with that match the given (':'-delimited list of) extensions (DEFAULT: all known extensions)",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        action="append",
        metavar="file",
        help="exclude file from test",
    )
    parser.add_argument(
        "directory", nargs="+", help="directory to recursively search for models"
    )

    args = parser.parse_args()
    log.setLevel(
        max(0, min(logging.FATAL, logging.INFO + (args.quiet - args.verbose) * 10))
    )
    del args.quiet
    del args.verbose
    args.extensions = [
        ext for extensions in args.extensions or [] for ext in extensions.split(":")
    ]
    return args


if __name__ == "__main__":
    args = parseCmdlineArgs()
    extensions = args.extensions or extensions
    ret = run_tests(args.directory, args.exclude or badfiles)
    sys.exit(ret)
