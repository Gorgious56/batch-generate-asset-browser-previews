import os
from pathlib import Path
from asset_browser_utilities.library.helper import get_blend_library_name
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty, PointerProperty

from asset_browser_utilities.core.operator.helper import FilterLibraryOperator
from asset_browser_utilities.console.builder import CommandBuilder
from asset_browser_utilities.file.path import is_this_current_file
from asset_browser_utilities.file.save import save_if_possible_and_necessary
from .helper import BatchExecute
from .prop import ExportProperties


class ASSET_OT_batch_export(Operator, ExportHelper, FilterLibraryOperator):
    "Export Assets"
    bl_idname = "asset.batch_export"
    bl_label = "Export Assets"

    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    filename_ext = ".blend"

    operator_settings: PointerProperty(type=ExportProperties)

    def invoke(self, context, event):
        self.asset_filter_settings.init(filter_selection=True, filter_assets=True)
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        if is_this_current_file(self.filepath):
            return {"FINISHED"}
        self.populate_asset_and_asset_names()
        if self.operator_settings.open_in_new_blender_instance:
            self.execute_in_new_blender_instance()
        else:
            self.execute_in_this_instance()
        return {"FINISHED"}

    def populate_asset_and_asset_names(self):
        assets = self.asset_filter_settings.get_objects_that_satisfy_filters()
        self.asset_names = [a.name for a in assets]
        self.asset_types = [get_blend_library_name(a) for a in assets]

    def execute_in_new_blender_instance(self):
        caller = CommandBuilder(Path(os.path.realpath(__file__)))
        for name in self.asset_names:
            caller.add_arg_value("asset_names", name)
        for _type in self.asset_types:
            caller.add_arg_value("asset_types", _type)
        caller.add_arg_value("source_file", bpy.data.filepath)
        caller.add_arg_value("filepath", self.filepath)
        caller.add_arg_value("remove_backup", self.library_settings.remove_backup)
        caller.add_arg_value("overwrite", self.operator_settings.overwrite)
        caller.add_arg_value("individual_files", self.operator_settings.individual_files)
        caller.call()

    def execute_in_this_instance(self):
        save_if_possible_and_necessary()
        operator_logic = BatchExecute(
            self.asset_names,
            self.asset_types,
            bpy.data.filepath,
            self.filepath,
            self.library_settings.remove_backup,
            self.operator_settings.overwrite,
            self.operator_settings.individual_files,
        )
        operator_logic.execute()

    def draw(self, context):
        layout = self.layout
        self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout)
