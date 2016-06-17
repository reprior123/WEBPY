from Tkinter import *
from tkFileDialog import *
from tkMessageBox import askquestion,showinfo
from tkSimpleDialog import askfloat

from Check import *
from CBUtils import string_limit

def make_checkstring(datestr,number,payee,cleared,comment,memo,amount,balance):
    str = "%10s " % datestr
    if number:
        str = str + "%5d " % number
    else:
        str = str + "      "
    str = str + "%-20s " % string_limit(payee,20)
    if cleared:
        str = str + "x "
    else:
        str = str + "  "
    if comment:
        str = str + "%-10s " % string_limit(comment,10)
    else:
        str = str + "           "
    if memo:
        str = str + "%-10s " % string_limit(memo,10)
    else:
        str = str + "           "
    str = str + "%8.2f " % amount
    str = str + "%8.2f " % balance
    return str        

class CheckbookWidget:
    def __init__(self,parent,title="PyCheckbook"):
        self.top = Tk()
        self.top.title(title)
        self.wire_funcs(parent)
        self.set_display_font()
        self.make_menu()
        self.make_toolbar()
        self.make_display()
        self.key_bindings()
        self.top.protocol("WM_DELETE_WINDOW",self.quit)
        return

    def wire_funcs(self,parent):
        # There is probably a smarter way of doing this...
        self.quit = parent.quit
        self.load_file = parent.load_file
        self.save_file = parent.save_file
        self.save_as_file = parent.save_as_file
        self.import_file = parent.import_file
        self.export_text = parent.export_text
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
        self.top.mainloop()
        return

    def key_bindings(self):
        #Menu items
        self.top.bind("<Control-q>",self.quit)
        self.top.bind("<Control-o>",self.load_file)
        self.top.bind("<Control-s>",self.save_file)
        self.top.bind("<Control-i>",self.import_file)
        self.top.bind("<Control-w>",self.close)
        self.top.bind("<Control-n>",self.newentry) 
        self.top.bind("<Control-m>",self.markcleared)
        self.top.bind("<Control-e>",self.editentry) 
        self.top.bind("<Control-v>",self.voidentry)
        self.top.bind("<Delete>",self.deleteentry) 
        self.top.bind("<Control-r>",self.reconcile)

        #Other convenience functions
        self.display.bind("<Double-Button-1>",self.editentry)
        self.top.bind("<Up>",self.previousentry)
        self.top.bind("<Down>",self.nextentry)
        self.top.bind("<Return>",self.editentry)

        return

    def make_menu(self):
        self.menu = Frame(self.top,relief=RAISED,
                          borderwidth=2)
        self.filemenubutton = Menubutton(self.menu,text="File")
        self.filemenubutton.pack(side=LEFT)
        self.filemenu = Menu(self.filemenubutton,
                             tearoff=0)
        self.filemenu.add_command(label="Open     Ctrl+o",
                                  command=self.load_file)
        self.filemenu.add_command(label="Save     Ctrl+s",
                                  command=self.save_file)
        self.filemenu.add_command(label="Save As",
                                  command=self.save_as_file)
        self.filemenu.add_command(label="Import   Ctrl+i",
                                  command=self.import_file)
        self.filemenu.add_command(label="Export",
                                  command=self.export_text)
        self.filemenu.add_command(label="Close    Ctrl+w",
                                  command=self.close)
        self.filemenu.add_command(label="Quit     Ctrl+q",
                                  command=self.quit)
        self.filemenubutton["menu"] = self.filemenu

        self.editmenubutton = Menubutton(self.menu,text="Edit")
        self.editmenubutton.pack(side=LEFT)
        self.editmenu = Menu(self.editmenubutton,tearoff=0)
        self.editmenu.add_command(label="New Entry     Ctrl+n",
                                  command=self.newentry)
        self.editmenu.add_command(label="Mark Cleared  Ctrl+m",
                                  command=self.markcleared)
        self.editmenu.add_command(label="Edit Entry    Ctrl+e",
                                  command=self.editentry)
        self.editmenu.add_command(label="Void Entry    Ctrl+v",
                                  command=self.voidentry)
        self.editmenu.add_command(label="Delete Entry  Del",
                                  command=self.deleteentry)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Reconcile     Ctrl+r",
                                    command=self.reconcile)
        self.editmenubutton["menu"] = self.editmenu

        self.helpmenubutton = Menubutton(self.menu,text="Help")
        self.helpmenubutton.pack(side=RIGHT)
        self.helpmenu = Menu(self.helpmenubutton,
                             tearoff=0)
        self.helpmenu.add_command(label="About",command=self.about)
        self.helpmenubutton["menu"] = self.helpmenu
        
        self.menu.pack(side=TOP,fill=X)
        return

    def make_toolbar(self):
        self.toolbar = Frame(self.top)
        self.toolbar.pack(side=TOP,fill=X)

        self.newbutton = Button(self.toolbar,
                                text="New Entry",
                                command=self.newentry)
        self.newbutton.pack(side=LEFT)

        self.editbutton = Button(self.toolbar,
                                 text="Edit Entry",
                                 command=self.editentry)
        self.editbutton.pack(side=LEFT)

        self.markbutton = Button(self.toolbar,
                                 text="Mark Cleared",
                                 command=self.markcleared)
        self.markbutton.pack(side=LEFT)

        self.deletebutton = Button(self.toolbar,
                                   text="Void Entry",
                                   command=self.voidentry)
        self.deletebutton.pack(side=LEFT)

        self.reconcilebutton=Button(self.toolbar,
                                    text="Reconcile",
                                    command=self.reconcile)
        self.reconcilebutton.pack(side=LEFT)

        self.quitbutton = Button(self.toolbar,
                                 text="Quit",
                                 command=self.quit)
        self.quitbutton.pack(side=LEFT)
        
        return
    
    def make_display(self):
        self.displayframe = Frame(self.top,border=10)
        self.display = Listbox(self.displayframe,
                               font=self.displayfont,
                               height=20,
                               width=80,
                               background="white")
        self.displayscroll = Scrollbar(self.displayframe,
                                       command=self.display.yview,
                                       bg="#004444",
                                       activebackground="#005555")
        self.display.configure(yscrollcommand=self.displayscroll.set)
        self.display.pack(side=LEFT)
        self.displayscroll.pack(side=RIGHT,fill=Y)
        self.displayframe.pack()
        return

    def set_display_font(self):
        # A hack to make sure that fonts look consistent across
        # platforms
        if sys.platform == 'win32':
            self.displayfont = ("Courier",8)
        else:
            self.displayfont = "Courier"
        return
    
    def about(self):
        showinfo("About: PyCheckbook",
                 "Python Checkbook Manager\n"
                 "Copyright (c) 2000,\nRichard P. Muller.\n"
                 "Released under the Gnu GPL\n"
                 )
        return

    def get_index(self):
        return int(self.display.curselection()[0])

    def goto_new_index(self,newindex=None,oldindex=None):
        if oldindex: self.display.selection_clear(oldindex)
        if not newindex: newindex = END
        self.display.selection_set(newindex)
        self.display.see(newindex)
        return

    def display_size(self): return self.display.size()

    def clear(self):
        self.display.delete(0,END)
        return

    #def append(self,datestr,number,payee,cleared,comment,memo,amount,balance):
    #    self.display.append((datestr,number,payee,cleared,comment,
    #                         memo,amount,balance))

    def append(self,datestr,number,payee,cleared,comment,memo,amount,balance):
        checkstring = make_checkstring(datestr,number,payee,cleared,
                                       comment,memo,amount,balance)
        self.display.insert(END,checkstring)

    def main_quit(self): self.top.quit()
    def head(self): return self.top
    
class CheckWidget(Toplevel):
    def __init__(self,master,check=None):
        Toplevel.__init__(self, master)
        self.transient(master)
        self.master = master
        self.make_widgets()
        if check:
            self.load_check(check)
            self.check = check
        else:
            self.check = Check()
        self.protocol("WM_DELETE_WINDOW",self.cancel)
        self.wait_window(self)
        self.result = 0
        return

    def load_check(self,check):
        self.date.insert(END,check.date.formatUS())
        if check.number:
            self.number.insert(END,check.number)
        if check.amount:
            self.amount.insert(END,"%.2f" % check.amount)
        if check.cleared:
            self.cleared.select()
        if check.payee:
            self.payee.insert(END,check.payee)
        if check.memo:
            self.memo.insert(END,check.memo)
        return

    def get_check_from_form(self):
        str = get_string_from_entry(self.date)
        self.check.date.parse_datestring(str)

        self.check.number = get_val_from_entry(self.number)
        self.check.amount = get_val_from_entry(self.amount)
        self.check.payee = get_string_from_entry(self.payee)
        self.check.memo = get_string_from_entry(self.memo)
        self.check.cleared = self.cleared_val.get()
        return

    def make_widgets(self):
        Label(self,text="PyCheckbook Check Editor"
              ).grid(row=1,column=1,columnspan=3)
        
        Label(self,text="Number: ").grid(row=1,column=4,sticky=W)
        self.number = Entry(self,width=8)
        self.number.grid(row=1,column=5)

        Label(self,text="Date: ").grid(row=2,column=4,sticky=W)
        self.date = Entry(self,width=8)
        self.date.grid(row=2,column=5)

        Label(self,text="Payee: ").grid(row=3,column=1)
        self.payee = Entry(self,width=20)
        self.payee.grid(row=3,column=2,columnspan=2)

        Label(self,text="Amount: $").grid(row=3,column=4,sticky=W)
        self.amount = Entry(self,width=8)
        self.amount.grid(row=3,column=5)

        Label(self,text="Memo: ").grid(row=4,column=1)
        self.memo = Entry(self,width=20)
        self.memo.grid(row=4,column=2,columnspan=2)

        self.cleared_val = IntVar()
        self.cleared = Checkbutton(self,
            text="Cleared",variable=self.cleared_val)
        self.cleared.grid(row=4,column=5)

        self.savebutton = Button(self,
                                 text="Save",
                                 command=self.save)
        self.savebutton.grid(row=5,column=2)
        self.cancelbutton = Button(self,
                                   text="Cancel",
                                   command=self.cancel)
        self.cancelbutton.grid(row=5,column=3)

        return

    def save(self):
        self.get_check_from_form()
        self.master.focus_set()
        self.destroy()
        return

    def cancel(self):
        self.check = None
        self.master.focus_set()
        self.destroy()
        return


def get_string_from_entry(entryname):
    str = entryname.get()
    str = string.strip(str)
    if not str:
        str = ''
    return str

def get_val_from_entry(entryname):
    str = get_string_from_entry(entryname)
    try:
        val = eval(str)
    except:
        val = 0
    return val
