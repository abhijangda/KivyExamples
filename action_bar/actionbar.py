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
     BooleanProperty, StringProperty, ListProperty
from kivy.uix.spinner import Spinner
from kivy.graphics import *
from kivy.graphics.instructions import *
from kivy.lang import *
from kivy.core.image import Image

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
    canvas:
        Color:
            rgba: self.background_color
        BorderImage:
            pos: self.pos
            size: self.size
            source: self.background_image

<ActionSeparator>:
    canvas:
        Rectangle:
            pos: self.x, self.y+5
            size: self.width, self.height-10
            source: self.background_image

<ActionTitle>:
    minimum_width: 100
    important: True

<ActionButton>:
    minimum_width: 50
    background_normal: './action_item.png'

<ActionToggleButton>:
    minimum_width: 50
    background_normal: './action_item.png'

<ActionCheck>:
    minimum_width: 50
    background_normal: './action_item.png'

<ActionDropDown>:
    auto_width: False

<ActionGroup>:
    background_normal: './action_group2.png'
    background_down: './action_group_down.png'
    background_disabled_normal: './action_spinner_disabled.png'
    border: 0,0,0,0

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

class ActionTitle(ActionItem, Label):
    '''ActionTitle class
    '''

    def __init__(self, **kwargs):
        super(ActionTitle, self).__init__(**kwargs)

class ActionButton(Button, ActionItem):
    '''ActionButton class
    '''

    def __init__(self, **kwargs):
        super(ActionButton, self).__init__(**kwargs)
        print self.background_down

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

    def __init__(self, *args):
        super(ActionDropDown, self).__init__(*args)
    
class ActionGroup(Spinner, ActionItem):
    '''ActionGroup class
    '''

    def __init__(self, **kwargs):
        super(ActionGroup, self).__init__(**kwargs)
        self.list_action_item = []
        self.dropdown_cls = ActionDropDown

    def add_widget(self, item):
        if not isinstance(item, ActionItem):
            raise ActionBarException('ActionView only accepts ActionItem')

        self.list_action_item.append(item)

    def show_group(self):
        self.clear_widgets()
        for item in self.list_action_item:
            item.size_hint = (None, None)
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

class ActionView(BoxLayout):
    '''ActionView class
    '''

    action_title = ObjectProperty(None)
    '''Title for ActionView
    '''

    background_color = ListProperty([1, 1, 1, 1])
    '''Background color, in the format (r, g, b, a).
    '''

    background_image = StringProperty(
        './action_view.png')
    '''Background image of ActionView for default graphical represenation.
    '''

    app_icon = StringProperty(
        './action_item.png')
    '''Application icon for the ActionView.
    '''

    previous_normal = StringProperty(
        './previous_normal.png')
    '''Image for 'previous' ActionButton for default graphical representation.
    '''

    separator_image = StringProperty(
        './separator.png')
    '''Image for ActionSeparator in ActionView.
    '''

    use_separator = BooleanProperty(False)
    '''Whether to use separator after every element or not
    '''

    separator_width = NumericProperty(1)
    '''Width of ActionSeparator
    '''

    overflow_normal = StringProperty(
        './overflow.png')
    '''Image for Overflow ActionGroup for default graphical representation.
    '''

    overflow_down = StringProperty(
        './overflow_down.png')
    '''Image for Overflow ActionGroup when pressed,
       for default graphical representation
    '''

    def __init__(self, **kwargs):
        super(ActionView, self).__init__(**kwargs)
        self.register_event_type('on_previous')

        self._overflow_group = ActionGroup()
        self._overflow_group.background_normal = self.overflow_normal
        self._overflow_group.background_down = self.overflow_down

        self._app_action_item = ActionButton(
            background_normal=self.app_icon)
        self._app_action_item.background_normal = self.app_icon
        self._app_action_item.important = True
        self._app_action_item.bind(on_release=self._emit_on_previous)

        self._previous_action_item = ActionButton()
        self._previous_action_item.important = True
        self._previous_action_item.bind(pos=self.previous_draw)
        self._previous_action_item.bind(size=self.previous_draw)
        self._previous_action_item.bind(on_press=self.previous_draw)
        self._previous_action_item.bind(on_release=self.previous_draw)
        
        self._list_action_group = []
        self._list_action_items = [self._previous_action_item,
                                   self._app_action_item]

    def previous_draw(self, *args):

        self._previous_action_item.canvas.clear()
        with self._previous_action_item.canvas:
            if self._previous_action_item.state == 'normal':
                texture = Image(self.previous_normal) 
                Rectangle(source=self.previous_normal,
                      pos=(self._previous_action_item.center_x-texture.width/2, self._previous_action_item.center_y-texture.height/2),
                      size=texture.size)
            elif self._previous_action_item.state == 'down':
                Rectangle(source=self._previous_action_item.background_down,
                      pos=self._previous_action_item.pos,
                      size=self._previous_action_item.size)
                texture = Image(self.previous_normal) 
                Rectangle(source=self.previous_normal,
                      pos=(self._previous_action_item.center_x-texture.width/2, self._previous_action_item.center_y-texture.height/2),
                      size=texture.size)
                
    def on_previous(self):
        pass

    def _emit_on_previous(self, *args):
        self.dispatch('on_previous')

    def on_overflow_normal(self, action_bar, icon):
        self._overflow_group.background_normal = icon

    def on_overflow_down(self, action_bar, icon):
        self._overflow_group.background_down = icon

    def add_widget(self, action_item, index=0):
        if not isinstance(action_item, ActionItem):
            raise ActionBarException('ActionView only accepts ActionItem')

        if isinstance(action_item, ActionTitle):
            #action_item is an ActionView
            super(ActionView, self).add_widget(action_item, 1)
            self.action_title = action_item
    
        elif isinstance(action_item, ActionGroup):
            #action_item is an ActionGroup
            self._list_action_group.append(action_item)

        else:
            #otherwise its an ActionItem only
            super(ActionView, self).add_widget(action_item, index)
            if index == 0:
                index = len(self._list_action_items)
            self._list_action_items.insert(index, action_item)

    def on_action_title(self, action_view, *args):
        self._list_action_items.insert(2, args[0])

    def _create_separator(self):
        sep = ActionSeparator(
            background_image=self.separator_image)
        sep.size_hint_x = None
        sep.width = 1
        return sep

    def _add_widget_with_separator(self, child):
        super(ActionView, self).add_widget(child)
        if self.use_separator == True:
            super(ActionView, self).add_widget(self._create_separator())

    def on_width(self, width, *args):
        total_width = 0
        self.clear_widgets()
        for child in self._list_action_items:
            total_width += child.minimum_width

        for group in self._list_action_group:
            group.clear_widgets()
            for child in group.list_action_item:
                total_width += child.minimum_width
        self._overflow_group.clear_widgets()
        self._overflow_group.list_action_item = []

        #First check if ActionView could display all ActionItems
        if total_width <= self.width:
            #If yes, then display them
            for child in self._list_action_items:
                super(ActionView, self).add_widget(child)
                
            for group in self._list_action_group:
                for child in group.list_action_item:
                    group.clear_widgets()
                    super(ActionView, self).add_widget(child)

            if self.use_separator==True:
                self.remove_widget(self.children[0])
        else:
            #If no, then check if all ActionItems could be displayed
            #using ActionGroup
            total_width = 0
            for child in self._list_action_items:
                total_width += child.minimum_width
            for group in self._list_action_group:
                total_width += group.minimum_width

            if total_width < self.width:
                #If yes, then display them using ActionGroup
                for child in self._list_action_items:
                    super(ActionView, self).add_widget(child)

                for group in self._list_action_group:
                    self._add_widget_with_separator(group)
                    group.show_group()

                if self.use_separator==True:
                    self.remove_widget(self.children[0])
            else:
                #If no, then display as many ActionItem having 'important'
                #set to true
                hidden_items = []
                hidden_groups = []
                total_width = 0

                width = self.width - self._overflow_group.minimum_width
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
                        if group.minimum_width + total_width + self.separator_width \
                           < width:
                            self._add_widget_with_separator(group)
                            group.show_group()
                            total_width += group.minimum_width + self.separator_width
                        else:
                            hidden_groups.append(group)

                #For all the left ActionItems and ActionItems
                #with in ActionGroups, Display them inside _overflow_group
                for child in hidden_items:
                    self._overflow_group.add_widget(child)

                for group in hidden_groups:
                    for child in group.list_action_item:
                        self._overflow_group.add_widget(child)
                
                self._overflow_group.show_group()
                super(ActionView, self).add_widget(self._overflow_group)

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

        if 'action_view' in kwargs:
            self.action_view = kwargs['action_view']
            super(ActionBar, self).add_widget(self.action_view)

        self._stack_cont_action_view = []

    def add_widget(self, view):
        if not isinstance(view, ContextualActionView):
            raise ActionBarException(
                'ActionBar can only add ContextualActionView')

        self._stack_cont_action_view.append(view)
        view.unbind(on_done=self._pop_contextual_action_view,
                    on_previous=self._pop_contextual_action_view)
        view.bind(on_done=self._pop_contextual_action_view,
                  on_previous=self._pop_contextual_action_view)
        self.clear_widgets()
        super(ActionBar, self).add_widget(view)

    def _pop_contextual_action_view(self, view):
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
    action_view = ActionView(use_separator=True)
    action_bar = ActionBar(action_view=action_view, size_hint=(1,0.1),
                           pos_hint={'top':1, 'y':1})
    

    action_title = ActionTitle(text='view')
    action_view.add_widget(action_title)
    

    list_action_btn = []
    for i in xrange(10):
        action_btn = ActionButton(text='Btn%d'%i)
        list_action_btn.append(action_btn)
    for i in xrange(5):
        action_view.add_widget(list_action_btn[i])

    action_grp_1 = ActionGroup(text='Group1')
    for i in xrange(5, 9):
        action_grp_1.add_widget(list_action_btn[i])
    action_view.add_widget(action_grp_1)

    list_cont_view = []
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
##        cont = ContextualActionView()
##        cont_title = ActionTitle(text='ContextualActionView%d'%j)
##        cont.add_widget(cont_title)
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
