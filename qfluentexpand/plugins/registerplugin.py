# coding:utf-8
import traceback
from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

from basic_input_plugin import *
from container_plugin import *
from date_time_plugin import *
from navigation_plugin import *
from status_info_plugin import *
from label_plugin import *
from text_plugin import *
from view_plugin import *
from toolbar_plugin import *


# basic input plugins
QPyDesignerCustomWidgetCollection.addCustomWidget(CheckBoxPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(ComboBoxPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(EditableComboBoxPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(HyperlinkButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(DropDownPushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PrimaryPushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SplitPushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(ToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PrimaryToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(DropDownToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PrimaryDropDownPushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PrimaryDropDownToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SplitToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PrimarySplitPushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PrimarySplitToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TransparentPushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PillPushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PillToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TransparentToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TransparentDropDownPushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TransparentDropDownToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TransparentTogglePushButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TransparentToggleToolButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(RadioButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SwitchButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(ToggleButtonPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(HorizontalSeparatorPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(VerticalSeparatorPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SliderPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(IconWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PixmapLabelPlugin())

# container plugins
QPyDesignerCustomWidgetCollection.addCustomWidget(ScrollAreaPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SmoothScrollAreaPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SingleDirectionScrollAreaPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(OpacityAniStackedWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PopUpAniStackedWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(CardWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(HeaderCardWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(CardGroupWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(GroupHeaderCardWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SimpleCardWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(ElevatedCardWidgetPlugin())

# date time plugins
QPyDesignerCustomWidgetCollection.addCustomWidget(DatePickerPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(ZhDatePickerPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TimePickerPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(AMTimePickerPlugin())

# label plugin
QPyDesignerCustomWidgetCollection.addCustomWidget(CaptionLabelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(BodyLabelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(StrongBodyLabelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SubtitleLabelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TitleLabelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(LargeTitleLabelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(DisplayLabelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(HyperlinkLabelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(ImageLabelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(AvatarPlugin())

# navigation plugins
QPyDesignerCustomWidgetCollection.addCustomWidget(NavigationInterfacePlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(NavigationPanelPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(NavigationBarPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PivotPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SegmentedWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SegmentedToolWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SegmentedToggleToolWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TabBarPlugin())

# status info plugins
QPyDesignerCustomWidgetCollection.addCustomWidget(InfoBarPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(IndeterminateProgressBarPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(IndeterminateProgressRingPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(ProgressBarPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(ProgressRingPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(StateToolTipPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(InfoBadgePlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(DotInfoBadgePlugin())

# text plugins
QPyDesignerCustomWidgetCollection.addCustomWidget(LineEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PasswordLineEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SearchLineEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TextEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(PlainTextEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(DateEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(DateTimeEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(DoubleSpinBoxPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(SpinBoxPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TimeEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(CompactDateEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(CompactDateTimeEditPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(CompactDoubleSpinBoxPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(CompactSpinBoxPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(CompactTimeEditPlugin())

# view plugins
QPyDesignerCustomWidgetCollection.addCustomWidget(ListWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(ListViewPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TableWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TableViewPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TreeWidgetPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(TreeViewPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(HorizontalFlipViewPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(VerticalFlipViewPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(HorizontalPipsPagerPlugin())
QPyDesignerCustomWidgetCollection.addCustomWidget(VerticalPipsPagerPlugin())

# tool bar plugin
QPyDesignerCustomWidgetCollection.addCustomWidget(CommandBarPlugin())