"""Verify the packaged add-on loads in a clean Blender; no GPU claim."""
import sys
import tempfile
import zipfile
from pathlib import Path

import addon_utils
import bpy

assert bpy.app.version[:2] == (4, 5), bpy.app.version_string
assert sys.version_info[:2] == (3, 11), sys.version
archive, = Path("BlenderPkg/.build").glob("*.zip")
with tempfile.TemporaryDirectory() as directory:
    with zipfile.ZipFile(archive) as package:
        package.extractall(directory)
    sys.path.insert(0, directory)
    module = addon_utils.enable("rprblender", default_set=False, persistent=False)
    assert module is not None, "Add-on registration failed"
    assert addon_utils.check("rprblender")[1], "Add-on not enabled"
    bpy.context.scene.render.engine = "RPR"
    print("PASS: packaged Radeon ProRender registered in", bpy.app.version_string)
    addon_utils.disable("rprblender", default_set=False)
