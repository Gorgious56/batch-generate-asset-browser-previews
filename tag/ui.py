from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_tags(Menu):
    bl_label = "Tags"

    def draw(self, context):
        layout = self.layout
        library_type = LibraryType.get_library_type_from_context(context)
        add_tags_op = layout.operator("asset.batch_add_tags", text="Add", icon="ADD")
        add_tags_op.library_settings.library_type = library_type
        remove_tags_op = layout.operator("asset.batch_remove_tags", text="Remove", icon="REMOVE")
        remove_tags_op.library_settings.library_type = library_type
