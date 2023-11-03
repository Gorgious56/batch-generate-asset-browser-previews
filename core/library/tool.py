from pathlib import Path
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.file.path import is_this_current_file
import bpy


def item_exists(name, _type):
    library = getattr(bpy.data, _type.lower() + "s")
    return library.get(name) is not None


def load_preview(filepath, asset=None):
    if asset is None:
        bpy.ops.ed.lib_id_load_custom_preview(filepath=str(filepath))
    else:
        if bpy.app.version >= (3, 2, 0):
            with bpy.context.temp_override(id=asset):
                bpy.ops.ed.lib_id_load_custom_preview(filepath=str(filepath))
        else:
            bpy.ops.ed.lib_id_load_custom_preview({"id": asset}, filepath=str(filepath))
    Logger.display(f"Loaded custom preview from '{filepath}' for asset '{asset.name or 'active asset'}'")


def get_directory_name(asset):
    name = type(asset).__name__.lower()
    if "nodetree" in name:
        name = "NodeTree"
    elif "texture" in name:
        name = "Texture"
    return name

def get_blend_data_name_from_directory(directory):
    name = directory.lower() + "s"
    if "nodetree" in name:
        name = "node_groups"
    elif "brush" in name:
        name = "brushes"
    elif "texture" in name:
        name = "textures"
    return name

def get_blend_data_name(asset):
    name = type(asset).__name__.lower() + "s"
    if "nodetree" in name:
        name = "node_groups"
    elif name == "brushs":
        name = "brushes"
    elif "texture" in name:
        name = "textures"
    return name


def get_files_in_folder(folder, recursive, extension="blend"):
    if isinstance(folder, str):
        folder = Path(folder)
    if recursive:
        return [fp for fp in folder.glob("**/*." + extension) if fp.is_file()]
    else:
        return [fp for fp in folder.glob("*." + extension) if fp.is_file()]


def sanitize_library_name(name):
    if "nodetree" in name:
        name = "node_groups"
    elif name == "brushs":
        name = "brushes"
    elif "texture" in name:
        name = "textures"
    if name.endswith("ss"):
        name = name[0:-1]
    return name


def link_asset(filepath, directory, filename, relative=False):
    return append_asset(filepath, directory, filename, link=True, relative=relative)


def append_asset(filepath, directory, filename, link=False, relative=False):
    if is_this_current_file(filepath):
        return
    # directory = sanitize_library_name(directory)
    blend_data_name = get_blend_data_name_from_directory(directory)
    # https://blender.stackexchange.com/a/33998/86891
    library = getattr(bpy.data, blend_data_name)
    with bpy.data.libraries.load(str(filepath), link=link, relative=relative) as (data_from, data_to):
        other_asset = library.get(filename)
        if other_asset is not None:  # If we don't change existing asset with same name, we can't append a new one.
            other_asset.name = "__ABU_TEMP_FOR_APPENDING_"
        library_to = getattr(data_to, blend_data_name)
        library_to.append(filename)

    asset = library.get(filename)
    if asset:
        if blend_data_name == "objects":
            bpy.context.scene.collection.objects.link(asset)
        elif blend_data_name == "collections":
            bpy.context.scene.collection.children.link(asset)
        else:
            asset.use_fake_user = True
    if other_asset is not None:
        other_asset.name = filename
    return asset


def iterate_over_all_containers():
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            for asset in container:
                yield asset
