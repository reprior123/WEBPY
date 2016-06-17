#!/usr/bin/env python
import gtk,os
#from gtk import *

from Check import *
from CBUtils import string_limit

class CheckbookWidget:
    def __init__(self,parent,title="PyCheckbook"):
        self.wire_funcs(parent)
        self.widget = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.widget.set_title(title)
        self.widget.connect("destroy",self.quit)

        self.vbox = gtk.VBox()
        self.widget.add(self.vbox)

        self.make_menu()
        self.make_toolbar()
        self.make_display()
        self.key_bindings()
        self.widget.show_all()
        return

    def wire_funcs(self,parent):
        self.quit = parent.quit
        self.load_file = parent.load_file
        self.save_file = parent.save_file
        self.save_as_file = parent.save_as_file
        self.import_file = parent.import_file
        self.close = parent.close
        self.newentry = parent.newentry
        self.markcleared = parent.markcleared
        self.editentry = parent.editentry
        self.voidentry = parent.voidentry
        self.deleteentry = parent.deleteentry
        self.reconcile = parent.reconcile
        self.previousentry = parent.previousentry
        self.nextentry = parent.nextentry
        return

    def mainloop(self):
        gtk.mainloop()

    def key_bindings(self):
        self.newbut.connect("clicked",self.newentry)
        self.edbut.connect("clicked",self.editentry)
        self.markbut.connect("clicked",self.markcleared)
        self.voidbut.connect("clicked",self.voidentry)
        self.recbut.connect("clicked",self.reconcile)
        return 

    def make_menu(self):
        self.accel_group = gtk.AccelGroup()
        self.item_factory = gtk.ItemFactory(gtk.MenuBar,"<main>",
                                            self.accel_group)

        self.item_factory.create_items([
            ('/File',None,None,0,"<Branch>"),
            ('/File/Open','<control>o',self.load_file,0,None),
            ('/File/Save','<control>s',self.save_file,0,None),
            ('/File/Save As...',None,self.save_as_file,0,None),
            ('/File/Import','<control>i',self.import_file,0,None),
            ('/File/Close','<control>c',self.close,0,None),
            ('/File/Quit','<control>q',self.quit,0,None),

            ('/Edit',None,None,0,"<Branch>"),
            ('/Edit/New Entry','<control>n',self.newentry,0,None),
            ('/Edit/Edit Entry','<control>e',self.editentry,0,None),
            ('/Edit/Mark Cleared','<control>m',self.markcleared,0,None),
            ('/Edit/Void Entry',None,self.voidentry,0,None),
            ('/Edit/Delete Entry',None,self.deleteentry,0,None),
            ('/Edit/Reconcile','<control>r',self.reconcile,0,None),

            ('/Help',None,None,0,"<Branch>"),
            ('/Help/About',None,self.about)
            ])
        self.widget.add_accel_group(self.accel_group)

        self.menubar = self.item_factory.get_widget("<main>")

        #self.menubar.add_entries()
        #self.widget.add_accel_group(self.menubar.accelerator)
        
        self.vbox.pack_start(self.menubar, gtk.FALSE, gtk.FALSE, 0)
        return

    def make_toolbar(self):
        self.toolbar = gtk.Toolbar()
        self.newbut = gtk.Button("New Entry")
        self.toolbar.add(self.newbut)
        self.edbut = gtk.Button("Edit Entry")
        self.toolbar.add(self.edbut)
        self.markbut = gtk.Button("Mark Entry")
        self.toolbar.add(self.markbut)
        self.voidbut = gtk.Button("Void Entry")
        self.toolbar.add(self.voidbut)
        self.recbut = gtk.Button("Reconcile")
        self.toolbar.add(self.recbut)
        self.vbox.pack_start(self.toolbar, gtk.FALSE, gtk.FALSE, 0)
        return

    def make_display(self):
        self.scroll = gtk.ScrolledWindow()
        self.titles = ['Date','Number','Transaction','X','Memo',
                  'Amount','Balance']
        self.display = gtk.CList(len(self.titles),self.titles)
        self.display.set_selection_mode(gtk.SELECTION_BROWSE)
        self.scroll.set_size_request(600,400)

        self.scroll.add(self.display)
        self.display.set_column_width(0,50) #date
        self.display.set_column_width(1,40) #num
        self.display.set_column_width(2,212)#payee
        self.display.set_column_width(3,8)  #cleared
        self.display.set_column_width(4,90) #memo
        self.display.set_column_width(5,50) #amount
        self.display.set_column_width(6,50) #balance
        self.vbox.pack_start(self.scroll, gtk.FALSE, gtk.FALSE, 0)
        return

    def set_display_font(self): return #still to do

    def about(self,args):
        showinfo("About: PyCheckbook",
                 "Python Checkbook Manager\n"
                 "Copyright (c) 2000,\nRichard P. Muller.\n"
                 "Released under the Gnu GPL\n"
                 )
        return

    def get_index(self):
        return self.display.selection[0]

    def goto_new_index(self,newindex=None,oldindex=None):
        if oldindex: self.display.unselect_row(oldindex,0)
        if not newindex: newindex = self.display.rows-1
        self.display.moveto(newindex,0,1.,0)
        self.display.select_row(newindex,0)
        return

    def display_size(self): return #still to do

    def append(self,datestr,number,payee,cleared,comment,memo,amount,balance):
        # I have deleted the comment from the display, since the extra space
        #  is useful for the memo, and since I never used the comment.
        if cleared:
            clearedstr = 'x'
        else:
            clearedstr = ' '
        if not comment: comment = ''
        if not memo: memo = ''
        if not number:
            numberstr = ''
        else:
            numberstr = '%d' % number
        self.display.append((datestr,numberstr,payee,
                             clearedstr,memo,
                             '%8.2f' % amount,
                             '%8.2f' % balance))

    def clear(self): self.display.clear()
    def main_quit(self): gtk.mainquit()
    def head(self): return self

class CheckWidget:
    def __init__(self,master,check=None):
        self.widget = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.make_widgets()

        if check:
            self.load_check(check)
            self.check = check
        else:
            self.check = Check()
            
        self.widget.show_all()
        gtk.mainloop()
        return

    def load_check(self,check):
        self.dateentry.set_text(check.date.formatUS())
        if check.number: self.number.set_text(str(check.number))
        if check.payee: self.payee.set_text(check.payee)
        if check.memo: self.memo.set_text(check.memo)
        if check.amount: self.amount.set_text("%.2f" % check.amount)
        if check.cleared: self.cleared.set_active(1)
        return

    def get_check_from_form(self):
        str = self.dateentry.get_text()
        self.check.date.parse_datestring(str)

        str = get_string_from_entry(self.number)
        self.check.amount = get_float_from_entry(self.amount)
        self.check.payee = get_string_from_entry(self.payee)
        self.check.memo = get_string_from_entry(self.memo)
        self.check.cleared = self.cleared.get_active()
        return

    def make_widgets(self):
        self.widget.set_title("Check Edit")
        self.widget.connect("destroy",gtk.mainquit)

        self.vbox = gtk.VBox()
        self.widget.add(self.vbox)


        #Number/Date Row
        self.numberrow = gtk.HBox()
        self.vbox.pack_start(self.numberrow)
        self.numberrow.pack_start(gtk.Label("Number"))
        self.number = gtk.Entry()
        self.numberrow.pack_start(self.number)
        self.numberrow.pack_start(gtk.Label("Date"))
        self.dateentry = gtk.Entry()
        self.numberrow.pack_start(self.dateentry)

        #Transaction Row
        self.transactionrow = gtk.HBox()
        self.vbox.pack_start(self.transactionrow)
        self.transactionrow.pack_start(gtk.Label("Transaction"))
        self.payee = gtk.Entry()
        self.transactionrow.pack_start(self.payee)

        #Amount/Cleared Row
        self.amountrow = gtk.HBox()
        self.vbox.pack_start(self.amountrow)
        self.amountrow.pack_start(gtk.Label("Amount"))
        self.amount = gtk.Entry()
        self.amountrow.pack_start(self.amount)
        self.cleared = gtk.CheckButton("Cleared")
        self.amountrow.pack_start(self.cleared)

        #Memo/Button Row
        self.buttonrow = gtk.HBox()
        self.vbox.pack_start(self.buttonrow)
        self.buttonrow.pack_start(gtk.Label("Memo"))
        self.memo = gtk.Entry()
        self.buttonrow.pack_start(self.memo)
        self.okbutton = gtk.Button("Ok")
        self.buttonrow.pack_start(self.okbutton)
        self.okbutton.connect("clicked",self.save)
        self.cancelbutton = gtk.Button("Cancel")
        self.buttonrow.pack_start(self.cancelbutton)
        self.cancelbutton.connect("clicked",self.cancel)

        return

    def save(self,args):
        self.get_check_from_form()
        self.widget.destroy()
        return

    def cancel(self,args):
        self.check = None
        self.widget.destroy()
        return

def askquestion(title,message):
    import string
    val = message_box(title,message,["Yes","No"])
    return string.lower(val)

def askfloat(title,message):
    import string
    val = input_box(title,message)
    if val:
        return float(val)
    return 0.

def askopenfilename(filetypes):
    filename = FileSelect('Open')
    return filename

def asksaveasfilename(filetypes):
    filename = FileSelect('Close')
    return filename

def showinfo(title,message):
    bs = message_box(title,message,["Ok"])
    return

# These functions may look extraneous, but they make it much easier
# to get the info out of the entries in a safe way

def get_string_from_entry(entryname):
    str = entryname.get_text()
    str = string.strip(str)
    if not str:
        str = ''
    return str

def get_int_from_entry(entryname):
    str = get_string_from_entry(entryname)
    try:
        val = int(str)
    except:
        val = 0
    return val

def get_float_from_entry(entryname):
    str = get_string_from_entry(entryname)
    try:
        val = float(str)
    except:
        val = 0
    return val

# Trying to replace the GtkExtra calls so we don't have to include
# that library, which can be hard to build...

class FileSelection(gtk.FileSelection):
    "Taken from pygtk, and made better"
    def __init__(self, title='Open', modal=gtk.FALSE, file_required=1):
        gtk.FileSelection.__init__(self)
        self.file_required = file_required
        self.set_title(title)
        self.connect('destroy', self.quit)
        self.connect('delete_event', self.quit)
        #if modal: gtk.grab_add(self)
        self.cancel_button.connect('clicked', self.quit)
        self.ok_button.connect('clicked', self.ok)
        self.return_filename = None
 
    def quit(self, *args):
        self.hide()
        self.destroy()
        gtk.mainquit()
 
    def ok(self, *args):
        filename = self.get_filename()
        filename = os.path.normpath(filename)
        if self.file_required and os.path.isdir(filename):
            if filename[-1:] != '/': filename += '/'
            self.set_filename(filename)
        else:
            self.return_filename = filename
            self.quit()

def FileSelect(title='Open', modal=gtk.FALSE):
    "Taken from pygtk and made better"
    win = FileSelection(title, modal, 1)
    win.show()
    gtk.mainloop()
    return win.return_filename

class MessageBox(gtk.Dialog):
    def __init__(self,title,options):
        gtk.Dialog.__init__(self,'Dialog')
        label = gtk.Label(title)
        self.vbox.pack_start(label,gtk.TRUE,gtk.TRUE,0)
        label.show()
        self.value = None
        self.buttons = []
        for item in options:
            button = gtk.Button(item)
            button.value = item
            self.buttons.append(button)
            self.action_area.pack_start(button,gtk.TRUE,gtk.TRUE,0)
            button.connect('clicked', self.getvalue)
            button.show()
        return

    def getvalue(self, button):
        self.value = button.value
        self.quit()

    def quit(self, *args):
        self.hide()
        self.destroy()
        gtk.mainquit()
        return

def message_box(title,options):
    win = MessageBox(title,options)
    win.show()
    gtk.mainloop()
    return win.value

class InputBox(gtk.Dialog):
    def __init__(self,message):
        gtk.Dialog.__init__(self,'Dialog')
        label = gtk.Label(message)
        self.vbox.pack_start(label,gtk.TRUE,gtk.TRUE,0)
        label.show()
        self.entry = gtk.Entry(max=20)
        self.vbox.pack_start(self.entry,gtk.TRUE,gtk.TRUE,0)
        self.entry.show()
        button = gtk.Button('Ok')
        self.action_area.pack_start(button,gtk.TRUE,gtk.TRUE,0)
        button.connect('clicked',self.ok)
        button.show()
        self.value = None

    def ok(self, *args):
        self.value = self.entry.get_text()
        self.quit()

    def quit(self, *args):
        self.hide()
        self.destroy()
        gtk.mainquit()
        return

def input_box(message):
    win = InputBox(message)
    win.show()
    gtk.mainloop()
    return win.value


def test():
    filename = FileSelect('testing file selection')
    print filename, ' was selected'
    print message_box('Testing message box',['1','2'])
    print input_box('Testing input box, enter value')
    return

if __name__ == '__main__': test()
