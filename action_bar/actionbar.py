'''Each ActionBar will have only one ActionView and many ContextualActionView.
ActionView has its own title, icon and previous_normal properties. ActionView will
emit on_previous event whenever icon and previous_normal ActionItems are clicked.
ActionView will have its own ActionItems, which can be ActionButton,
ActionToggleButton, ActionCheck and ActionSeparator. If ActionView's
use_separator is set to True, then there will be a ActionSeparator after
every ActionGroup. If user wants to manually, add an ActionSeparator then he
should set use_separator to False. ActionView has overflow_icon property to set
icon to be used for ActionView's overflow_action_item.
ActionGroup contains ActionItems.
ContextualActionView also contains an ok_icon property, which is used to set
icon for its ok_action_item. Whenever, ok_action_item is clicked, on_done event
is emitted.
ActionBar contains an action_view property to set the actionview.
ContextualActionView could be added by add_widget.
'''

__all__ = ('ActionBarException', 'ActionItem', 'ActionTitle',
           'ActionButton', 'ActionToggleButton', 'ActionCheck',
           'ActionSeparator', 'ActionGroup', 'ActionView', 
           'ContextualActionView', 'ActionBar')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, \
     BooleanProperty, StringProperty, ListProperty, OptionProperty
from kivy.uix.spinner import Spinner
from kivy.graphics import *
from kivy.graphics.instructions import *
from kivy.lang import *
from kivy.core.image import Image
from functools import *

Builder.load_string('''
<ActionBar>:
    canvas:
        Color:
            rgba: self.background_color
        BorderImage:
            pos: self.pos
            size: self.size
            source: self.background_image

<ActionView>:
    orientation: 'horizontal'
    padding: '2sp'
    canvas:
        Color:
            rgba: self.background_color
        BorderImage:
            pos: self.pos
            size: self.size
            source: self.background_image

<ActionSeparator>:
    size_hint_x: None
    minimum_width: '2sp'
    width: self.minimum_width
    canvas:
        Rectangle:
            pos: self.x, self.y+5
            size: self.width, self.height-10
            source: self.background_image

<ActionButton>:
    minimum_width: 50
    background_normal: './action_item.png'

<ActionToggleButton>:
    minimum_width: 50
    background_normal: './action_item.png'

<ActionCheck>:
    minimum_width: 50
    background_normal: './action_item.png'

<ActionPrevious>:
    previous_image_widget: _previous_image
    app_image_widget: _app_image
    title_widget: _title
    minimum_width: '200sp'
    width: self.minimum_width
    background_normal: './action_item.png'
    important: True
    BoxLayout:
        orientation: 'horizontal'
        pos: root.pos
        size: root.size
        padding: '2dp'
        Image:
            id: _previous_image
            source: root.previous_image
        Image:
            id: _app_image
            source: root.app_image
        Label:
            id: _title
            text: root.title
            text_size: self.size
            halign: 'right'
            valign: 'middle'

<ActionGroup>:
    background_normal: './action_group2.png'
    background_down: './action_group_down.png'
    background_disabled_normal: './action_spinner_disabled.png'
    border: 30,20,8,12
    ActionSeparator:
        pos: root.pos
        size: root.separator_width, root.height
        opacity: 1 if root.use_separator else 0
        background_image: root.separator_image

<ActionOverflow>:
    border: 0, 0, 0, 0
    background_normal: './overflow.png'
    background_down: './overflow_down.png'

<ActionDropDown>:
    auto_width: False

<ContextualActionView>:
''')

class ActionBarException(Exception):
    '''ActionBarException class
    '''

class ActionItem(Widget):
    '''An abstract class
    '''

    minimum_width = NumericProperty()
    '''Minimum Width required by an ActionItem.
    '''

    important = BooleanProperty(False)
    '''Determines if ActionItem is important or not.
    '''

    def __init__(self, **kwargs):
        super(ActionItem, self).__init__(**kwargs)

class ActionButton(Button, ActionItem):
    '''ActionButton class
    '''

    def __init__(self, **kwargs):
        super(ActionButton, self).__init__(**kwargs)

class ActionPrevious(ActionButton):
    '''ActionPrevious class
    '''

    app_image = StringProperty(
        './kivy/kivy/data/logo/kivy-icon-32.png')
    '''Application icon for the ActionView.
    '''

    previous_image = StringProperty(
        './previous_normal.png')
    '''Image for 'previous' ActionButton for default graphical representation.
    '''

    title = StringProperty('')
    '''Title for ActionView
    '''

    previous_image_widget = ObjectProperty(None)
    '''Widget displaying previous_image, defaults to Image
    '''

    app_image_widget = ObjectProperty(None)
    '''Widget displaying app_image, defaults to Image
    '''

    title_widget = ObjectProperty(None)
    '''Widget displaying title_widget, defaults to Label
    '''

    def __init__(self, **kwargs):
        super(ActionPrevious, self).__init__(**kwargs)

        self.previous_image_widget.bind(texture = self.on_child_texture)
        self.app_image_widget.bind(texture = self.on_child_texture)
        self.title_widget.bind(texture = self.on_child_texture)

    def on_child_texture(self, instance, value):
        if value is None:
            return

        instance.size_hint_x = None
        instance.width = value.width

class ActionToggleButton(ActionItem, ToggleButton):
    '''ActionToggleButton class
    '''

    def __init__(self, **kwargs):
        super(ActionToggleButton, self).__init__(**kwargs)

class ActionCheck(ActionItem, CheckBox):
    '''ActionCheck class
    '''

    def __init__(self, **kwargs):
        super(ActionCheck, self).__init__(**kwargs)

class ActionSeparator(ActionItem):
    '''ActionSeparator class
    '''

    background_image = StringProperty(
        './separator.png')
    '''Background to display when this is disabled
    '''

    def __init__(self, **kwargs):
        super(ActionSeparator, self).__init__(**kwargs)

class ActionDropDown(DropDown):
    '''ActionDropDown class
    '''

    def __init__(self, **kwargs):
        super(ActionDropDown, self).__init__(**kwargs)

class ActionGroup(Spinner, ActionItem):
    '''ActionGroup class
    '''

    use_separator = BooleanProperty(False)
    '''Whether to use separator after every element or not
    '''

    separator_image = StringProperty(
        './separator.png')
    '''Image for ActionSeparator in ActionView.
    '''

    separator_width = NumericProperty(1)
    '''Width of ActionSeparator
    '''

    mode = OptionProperty('normal', options=('normal', 'spinner'))
    '''
    '''

    def __init__(self, **kwargs):
        self.list_action_item = []
        super(ActionGroup, self).__init__(**kwargs)
        self.dropdown_cls = ActionDropDown

    def add_widget(self, item):
        if isinstance(item, ActionSeparator):
            super(ActionGroup, self).add_widget(item)
            return
        if not isinstance(item, ActionItem):
            raise ActionBarException('ActionView only accepts ActionItem')

        self.list_action_item.append(item)

    def show_group(self):
        self.clear_widgets()
        for item in self.list_action_item:
            item.size_hint_y = None
            self._dropdown.add_widget(item)

    def _build_dropdown(self, *largs):
        if self._dropdown:
            self._dropdown.dismiss()
            self._dropdown = None
        self._dropdown = self.dropdown_cls()

    def _update_dropdown(self, *largs):
        pass

    def clear_widgets(self):
        self._dropdown.clear_widgets()

class ActionOverflow(ActionGroup):
    '''ActionOverflow class
    '''

class ActionView(BoxLayout):
    '''ActionView class
    '''

    action_previous = ObjectProperty(None)
    '''Title for ActionView
    '''

    background_color = ListProperty([1, 1, 1, 1])
    '''Background color, in the format (r, g, b, a).
    '''

    background_image = StringProperty(
        './action_view.png')
    '''Background image of ActionView for default graphical represenation.
    '''

    use_separator = BooleanProperty(False)
    '''Whether to use separator after every element or not
    '''

    overflow_group = ObjectProperty(None)
    '''Widget to be used for overflow.
       Defaults to ActionOverflow's instance.
    '''

    def __init__(self, **kwargs):
        self._list_action_items = []
        self._list_action_group = []
        super(ActionView, self).__init__(**kwargs)
        self._state = ''
        self.overflow_group = ActionOverflow(use_separator=self.use_separator)
    
    def on_action_previous(self, instance, value):
        self._list_action_items.insert(0, value)

    def add_widget(self, action_item, index=0):
        if not isinstance(action_item, ActionItem):
            raise ActionBarException('ActionView only accepts ActionItem')
        
        elif isinstance(action_item, ActionOverflow):
            #action_item is an ActionOverflow
            self.overflow_group = action_item
            action_item.use_separator = self.use_separator

        elif isinstance(action_item, ActionGroup):
            #action_item is an ActionGroup
            self._list_action_group.append(action_item)
            action_item.use_separator = self.use_separator

        elif isinstance(action_item, ActionPrevious):
            #action_item is ActionPrevious
            self.action_previous = action_item
        else:
            #otherwise its an ActionItem only
            super(ActionView, self).add_widget(action_item, index)
            if index == 0:
                index = len(self._list_action_items)
            self._list_action_items.insert(index, action_item)

    def on_use_separator(self, instance, value):
        for group in self._list_action_group:
            group.use_separator = value

    def _clear_all(self):
        self.clear_widgets()
        for group in self._list_action_group:
            group.clear_widgets()
        
        self.overflow_group.clear_widgets()
        self.overflow_group.list_action_item = []

    def on_width(self, width, *args):
        total_width = 0
        for child in self._list_action_items:
            total_width += child.minimum_width

        for group in self._list_action_group:
            for child in group.list_action_item:
                total_width += child.minimum_width

        #First check if ActionView could display all ActionItems
        if total_width <= self.width:
            if self._state == 'all':
                return

            self._state = 'all'
            self._clear_all()
            #If yes, then display them
            for child in self._list_action_items:
                child.size_hint_y = 1
                super(ActionView, self).add_widget(child)

            for group in self._list_action_group:
                if group.mode == 'spinner':
                    super(ActionView, self).add_widget(group)
                    group.show_group()
                else:
                    if group.list_action_item != []:
                        super(ActionView, self).add_widget(ActionSeparator())                       
                    for child in group.list_action_item:
                        child.size_hint_y = 1
                        super(ActionView, self).add_widget(child)

        else:
            #If no, then check if all ActionItems could be displayed
            #using ActionGroup
            total_width = 0
            for child in self._list_action_items:
                total_width += child.minimum_width
            for group in self._list_action_group:
                total_width += group.minimum_width

            if total_width < self.width:
                if self._state == 'group':
                    return

                self._state = 'group'
                self._clear_all()
                #If yes, then display them using ActionGroup
                for child in self._list_action_items:
                    super(ActionView, self).add_widget(child)

                for group in self._list_action_group:
                    super(ActionView, self).add_widget(group)
                    group.show_group()

            else:
                #If no, then display as many ActionItem having 'important'
                #set to true
                self._clear_all()
                hidden_items = []
                hidden_groups = []
                total_width = 0

                width = self.width - self.overflow_group.minimum_width
                for child in self._list_action_items:
                    if child.important == True:
                        if child.minimum_width + total_width < width:
                            super(ActionView, self).add_widget(child)
                            total_width += child.minimum_width
                        else:
                            hidden_items.append(child)
                    else:
                        hidden_items.append(child)

                #If space is left then display other ActionItems
                if total_width < self.width:
                    for child in hidden_items:
                        if child.minimum_width + total_width < width:
                            super(ActionView, self).add_widget(child)
                            total_width += child.minimum_width
                            hidden_items.remove(child)

                #If space is left then display ActionItem inside
                #their ActionGroup
                if total_width < self.width:
                    for group in self._list_action_group:
                        if group.minimum_width + total_width + group.separator_width \
                           < width:
                            super(ActionView, self).add_widget(group)
                            group.show_group()
                            total_width += group.minimum_width + group.separator_width
                        else:
                            hidden_groups.append(group)

                #For all the left ActionItems and ActionItems
                #with in ActionGroups, Display them inside overflow_group
                for child in hidden_items:
                    self.overflow_group.add_widget(child)

                for group in hidden_groups:
                    for child in group.list_action_item:
                        self.overflow_group.add_widget(child)
                
                self.overflow_group.show_group()
                super(ActionView, self).add_widget(self.overflow_group)

class ContextualActionView(ActionView):
    '''ContextualActionView class
    '''

class ActionBar(BoxLayout):

    action_view = ObjectProperty(None)
    '''ActionView of ActionBar. One ActionBar can only have one ActionView
    '''

    background_color = ListProperty([1, 1, 1, 1])
    '''Background color, in the format (r, g, b, a).
    '''

    background_image = StringProperty(
        './action_bar.png')
    '''Background image of ActionView for default graphical represenation.
    '''

    def __init__(self, **kwargs):
        super(ActionBar, self).__init__(**kwargs)
        self.register_event_type('on_previous')
        self._stack_cont_action_view = []
        self._emit_previous = partial(self.dispatch, 'on_previous')

    def add_widget(self, view):
        if isinstance(view, ContextualActionView):
            self._stack_cont_action_view.append(view)
            view.action_view.unbind(on_release=self._emit_previous)
            view.action_view.bind(on_release=self._emit_previous)
            self.clear_widgets()
            super(ActionBar, self).add_widget(view)

        elif isinstance(view, ActionView):
            self.action_view = view
            super(ActionBar, self).add_widget(view)

        else:
            raise ActionBarException(
                'ActionBar can only add ContextualActionView or ActionView')

    def on_previous(self, *args):
        self._pop_contextual_action_view()

    def _pop_contextual_action_view(self):
        '''Remove the current ContextualActionView and display either the
           previous one or the ActionView
        '''
        self._stack_cont_action_view.pop()
        self.clear_widgets()
        if self._stack_cont_action_view == []:
            super(ActionBar, self).add_widget(self.action_view)
        else:
            super(ActionBar, self).add_widget(self._stack_cont_action_view[-1])

    
if __name__ == "__main__":
    from kivy.base import runTouchApp
    from kivy.uix.floatlayout import FloatLayout
    from kivy.clock import Clock

    float_layout = FloatLayout()
    overflow_group = ActionOverflow()
    action_previous = ActionPrevious(title='AppTitle')
    action_view = ActionView(use_separator=True,
                             action_previous=action_previous,
                             overflow_group=overflow_group)
    action_bar = ActionBar(size_hint=(1,0.1),
                           pos_hint={'top':1, 'y':1})
    action_bar.add_widget(action_view)
    

    list_action_btn = []
    for i in xrange(10):
        action_btn = ActionButton(text='Btn%d'%i)
        list_action_btn.append(action_btn)
    for i in xrange(5):
        action_view.add_widget(list_action_btn[i])

    action_grp_1 = ActionGroup(text='Group1',mode='normal')
    for i in xrange(5, 9):
        action_grp_1.add_widget(list_action_btn[i])
    action_view.add_widget(action_grp_1)

##    list_cont_view = []
##    def push_cont_view(btn):
##        index = int(btn.text[-1])
##        action_bar.add_widget(list_cont_view[index])
##
##    for i in range(2):
##        btn1 = Button(text='Add Contextual View %d'%(i), size_hint=(0.20,0.15),
##                            pos_hint={'top':0.5, 'y': 0.3, 'x':0.21*i})
##        float_layout.add_widget(btn1)
##        btn1.bind(on_release=push_cont_view)
##
##    for j in range(2):
##        cont_action_previous = ActionPrevious()
##        cont = ContextualActionView(action_previous=cont_action_previous)
##        for i in range(3):
##            action_btn = ActionButton(text='CAV%d Btn%d'%(j,i))
##            cont.add_widget(action_btn)
##        action_grp = ActionGroup(text='CAV%d Group1'%j)
##        for i in range(3, 6):
##            action_btn = ActionButton(text='CAV%d Btn%d'%(j,i))
##            action_grp.add_widget(action_btn)
##        cont.add_widget(action_grp)
##        list_cont_view.append(cont)

    float_layout.add_widget(action_bar)
    runTouchApp(float_layout)
