from asset_browser_utilities.module.author.set import AuthorSetOperatorProperties
from asset_browser_utilities.module.catalog.operator.move_from_a_to_b import CatalogMoveFromAToBOperatorProperties
from asset_browser_utilities.module.catalog.operator.move_to import CatalogMoveOperatorProperties
from asset_browser_utilities.module.catalog.operator.remove_from import CatalogRemoveFromOperatorProperties
from asset_browser_utilities.core.operator.operation import OperationSettings
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.module.description.set import DescriptionSetOperatorProperties
from asset_browser_utilities.module.preview.operator.generate import PreviewGenerateOperatorProperties
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.module.catalog.prop import CatalogExportSettings

from asset_browser_utilities.module.asset.operator.mark import AssetMarkOperatorProperties
from asset_browser_utilities.module.asset.export.operator import AssetExportOperatorProperties
from asset_browser_utilities.module.asset.operator.copy import AssetCopyOperatorProperties
from asset_browser_utilities.module.tag.operator.tool import TagAddOrRemoveOperatorProperties
from asset_browser_utilities.module.tag.operator.add_smart import TagAddSmartOperatorProperties
from asset_browser_utilities.module.custom_property.operator.set import CustomPropertySetOperatorProperties
from asset_browser_utilities.module.custom_property.operator.remove import RemoveCustomPropertyOperatorProperties
from asset_browser_utilities.module.asset.prop import SelectedAssetFiles
from asset_browser_utilities.module.material.operator.merge import MaterialMergeOperatorProperties


class Cache(PropertyGroup):
    library_settings: PointerProperty(type=LibraryExportSettings)
    operation_settings: PointerProperty(type=OperationSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    catalog_settings: PointerProperty(type=CatalogExportSettings)
    
    current_op: PointerProperty(type=CurrentOperatorProperty)
    mark_op: PointerProperty(type=AssetMarkOperatorProperties)
    copy_op: PointerProperty(type=AssetCopyOperatorProperties)
    export_op: PointerProperty(type=AssetExportOperatorProperties)
    smart_tag_op: PointerProperty(type=TagAddSmartOperatorProperties)
    add_or_remove_tag_op: PointerProperty(type=TagAddOrRemoveOperatorProperties)
    custom_prop_set_op: PointerProperty(type=CustomPropertySetOperatorProperties)
    custom_prop_remove_op: PointerProperty(type=RemoveCustomPropertyOperatorProperties)
    preview_generate_op: PointerProperty(type=PreviewGenerateOperatorProperties)
    catalog_move_from_a_to_b_op: PointerProperty(type=CatalogMoveFromAToBOperatorProperties)
    catalog_move_op: PointerProperty(type=CatalogMoveOperatorProperties)
    catalog_remove_op: PointerProperty(type=CatalogRemoveFromOperatorProperties)
    author_set_op: PointerProperty(type=AuthorSetOperatorProperties)
    description_set_op: PointerProperty(type=DescriptionSetOperatorProperties)
    material_merge_op: PointerProperty(type=MaterialMergeOperatorProperties)
    
    selected_assets: PointerProperty(type=SelectedAssetFiles)

    show: BoolProperty()

    def get(self, _type):
        for prop_name in self.__annotations__:
            prop = getattr(self, prop_name)
            if isinstance(prop, _type):
                return prop
    
    def draw(self, layout, context, header=None, rename=False):
        if header is None:
            header = self.name
        row = layout.row(align=True)
        if rename:
            row.prop(self, "name")
        row.prop(self, "show", toggle=True, text=header)
        if self.show:
            for attr in self.__annotations__:
                default_setting = getattr(self, attr)
                if hasattr(default_setting, "draw"):
                    default_setting.draw(layout, context)
        
