from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDBottomAppBar
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.config import Config
import controller
from kivy.core.window import Window
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Window.size = (400, 620)

class Tab(MDFloatLayout, MDTabsBase):
    pass

class ShowAllContacts(MDBoxLayout):
    list_contacts: ObjectProperty()
    text_field: ObjectProperty()
    button_magnify: ObjectProperty()

class ShowContact(MDBoxLayout):
    name: ObjectProperty()
    telephone: ObjectProperty()
    comment: ObjectProperty()

class ChangeContact(BoxLayout):
    name: StringProperty()
    telephone: StringProperty()
    comment: StringProperty()

class Topappbar(MDBottomAppBar):
    action_button: ObjectProperty()

class Container(MDBoxLayout):
    action_button = ObjectProperty()
    list_contacts = ObjectProperty()
    contain = ObjectProperty()
    app_bar = ObjectProperty()
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw_coontain()

    def show_alert_dialog_delete_contact(self, instance):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Удалить контакт?",
                buttons=[
                    MDFlatButton(
                        text="НЕТ",
                        theme_text_color="Custom",
                        on_release= self.dialog_close,
                    ),
                    MDFlatButton(
                        text="ДА",
                        theme_text_color="Custom",
                        on_release= lambda x: self.delete_contact(instance),
                    ),
                ],
            )
        self.dialog.open()
        
    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)
    
    def delete_contact(self, instance):
        self.dialog_close()
        controller.delеtе_contact(int(instance.id))
        self.draw_coontain()

    def search_item_by_index(self, index):
        contact = controller.search_contact_by_id(index)
        return contact

    index_contact = 0
    def change_main_icon_action_button(self, instance):
        self.index_contact = int(instance.id)
        self.action_button.icon = "pencil"
        self.change_widget(self.index_contact)
        self.action_button.left_action_items= [["arrow-left", lambda x: self.draw_coontain()]]
    
    def change_icon_action_button(self):
        if self.action_button.icon == "pencil":
            self.action_button.icon = "check"
            self.change_widget(self.index_contact)
        elif self.action_button.icon == "check":
            if self.change_contact != None and self.change_contact.name.text != "" and self.change_contact.telephone.text != "" and self.change_contact.telephone.text.isdigit():
                self.save_change_contact()
                self.draw_coontain()
                self.action_button.icon = "plus"
            elif self.new_contact != None:
                self.save_new_contact()
                self.draw_coontain()
                self.action_button.icon = "plus"
        elif self.action_button.icon == "plus":
            self.change_widget(self.index_contact)
            self.action_button.left_action_items= [["arrow-left", lambda x: self.draw_coontain()]]
            self.action_button.icon = "check"
            

    change_contact = None
    new_contact = None
    def change_widget(self, index):
        if self.action_button.icon == "pencil":
            item_contact = self.search_item_by_index(index)
            self.contain.clear_widgets()
            show_contact = ShowContact(orientation= 'vertical')
            show_contact.name.text = item_contact.name
            show_contact.telephone.text += item_contact.telephone
            show_contact.comment.text += item_contact.comment
            self.contain.add_widget(show_contact)
        elif self.action_button.icon == "check":
            item_contact = self.search_item_by_index(index)
            self.contain.clear_widgets()
            self.change_contact = ChangeContact(orientation= 'vertical')
            self.change_contact.name.text += item_contact.name
            self.change_contact.telephone.text += item_contact.telephone
            self.change_contact.comment.text += f"\n{item_contact.comment}"
            self.contain.add_widget(self.change_contact)
        elif self.action_button.icon == "plus":
            self.contain.clear_widgets()
            self.new_contact = ChangeContact(orientation= 'vertical')
            self.new_contact.name.text += ""
            self.new_contact.telephone.text += "" 
            self.new_contact.comment.text += ""
            self.contain.add_widget(self.new_contact)
    
    
    def save_change_contact(self):
        name = self.change_contact.name.text
        telephone = self.change_contact.telephone.text
        comment = self.change_contact.comment.text
        controller.change_contact(self.index_contact, name, telephone, comment)
        self.change_contact = None
    
    def save_new_contact(self):
        name = self.new_contact.name.text
        telephone = self.new_contact.telephone.text
        comment = self.new_contact.comment.text
        controller.input_contact(name, telephone, comment)
        self.new_contact = None

    all_contact = None
    def draw_coontain(self): 
        self.contain.clear_widgets()
        self.action_button.left_action_items= [["", lambda x: x]]
        self.all_contact = ShowAllContacts(orientation= 'vertical')
        self.all_contact.button_magnify.on_release = self.draw_item_contact
        self.contain.add_widget(self.all_contact)
        self.draw_item_contact()
    
    def draw_item_contact(self):
        self.all_contact.list_contacts.clear_widgets()
        lst = self.search_contact()
        for index, contact in enumerate(lst):
            self.all_contact.list_contacts.add_widget(
                TwoLineAvatarIconListItem(
                    IconRightWidget(
                        id= str(index),
                        icon="delete",
                        icon_size= "15sp",
                        on_press= self.show_alert_dialog_delete_contact
                    ),
                    IconLeftWidget(
                        icon="account",
                        icon_size= "19sp"
                    ),
                    text= contact.name,
                    secondary_text= contact.telephone,
                    id= str(index),
                    on_release= self.change_main_icon_action_button
                )
            )
        
    def search_contact(self):
        lst = list()
        if self.all_contact.text_field.text == "":
            lst = controller.show_phonebook()
        else:
            string = self.all_contact.text_field.text
            lst = controller.search_contact(string)
        return lst  
            