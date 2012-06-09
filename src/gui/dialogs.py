'''
Created on Jan 30, 2011

@author: ben
'''
from Tkinter import *
from ttk import *
import tkMessageBox
import tkSimpleDialog
import tkFileDialog
import os

class Dialog(Toplevel):

    def __init__(self, parent, title = None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5, expand = 1, fill = BOTH)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override

class AccountFrame(Frame):
    """
    a frame for the account settings.
    """
    
    def __init__(self, master):
        '''
        class initializer
        '''
        Frame.__init__(self, master)
        self.control = StringVar()
        
        emailframe = Frame(self)
        Label(emailframe, text="Email Address:").pack(side=LEFT)
        self.email = Entry(emailframe)
        self.email.pack(side=LEFT)
        emailframe.pack(fill = X)
        
        inmailFrame = LabelFrame(self, text = "Incoming Server")
        
        intypeframe = Frame(inmailFrame)
        Label(intypeframe, text = "Incoming mail type:").pack(side=LEFT)
        self.r1 = Radiobutton(intypeframe, text = 'POP', variable = self.control, value = "POP",)
        self.r2 = Radiobutton(intypeframe, text = 'IMAP', variable = self.control, value = "IMAP",)
        self.r1.pack(side=LEFT)
        self.r2.pack(side=LEFT)
        intypeframe.pack(fill = X)
        
        inserverFrame = Frame(inmailFrame)
        Label(inserverFrame, text="Server:").pack(side=LEFT)
        self.inserver = Entry(inserverFrame)
        self.inserver.pack(side=LEFT)
        inserverFrame.pack(fill = X)
        
        inportFrame = Frame(inmailFrame)
        Label(inportFrame, text="Port:").pack(side=LEFT)        
        self.inport = Entry(inportFrame)        
        self.inport.pack(side=LEFT)
        inportFrame.pack(fill = X)
        
        inmailFrame.pack()
        
        smtpFrame = LabelFrame(self, text = 'Outgoing Server')
        
        sserverframe = Frame(smtpFrame)
        Label(sserverframe, text="Server:").pack(side=LEFT)
        self.sserver = Entry(sserverframe)
        self.sserver.pack(side=LEFT)
        sserverframe.pack()
        
        sportFrame = Frame(smtpFrame)
        Label(sportFrame, text="Port:").pack(side=LEFT)        
        self.sport = Entry(sportFrame)
        self.sport.pack(side=LEFT)
        sportFrame.pack()
        
        smtpFrame.pack()
        
class OptionsDialog(Dialog):
    
    def body(self, master):

        notebook = Notebook(master)    
        self.accountFrame = AccountFrame(notebook)
        notebook.add(self.accountFrame, text = 'Accounts')
        notebook.pack(side=TOP, fill=BOTH, expand = 1)
        
    def apply(self):
        '''
        Apply the items in the dialog.    
        '''
        self.email = self.accountFrame.email.get()
        self.type = self.accountFrame.control.get()
        print self.type
        self.server = self.accountFrame.inserver.get()
        self.port = self.accountFrame.inport.get()
        self.smtp_server = self.accountFrame.sserver.get()
        self.smtp_port = self.accountFrame.sport.get()
    



class WelcomeDialog(Dialog):
    """
    Class Documentation
    """
    
    def __init__(self):
        '''
        class initializer
        '''
        pass

        
class DialogManager(object):
    '''
    Class Documentation
    '''
    
    def __init__(self, master):
    
        '''
        Class initializer.
        
        '''
        self.master = master
        
    def warn(self, title, text):    
        tkMessageBox.showwarning(title, text)
        
    def askPassword(self):
        passw = tkSimpleDialog.askstring("Password?", "Please enter your email's password.", show = '*')
        return passw        
        
    def openfile(self, title):
        name = tkFileDialog.askopenfilename(defaultextension = "fqa", title = title)
        return name
        
    def settings(self):
        '''
        Opens the settings dialog.
        '''
        settings = OptionsDialog(self.master)
        return settings
    
    def savefile(self, title):
        '''
        Proxy for the Tk file saving dialog.
        '''
        name = tkFileDialog.asksaveasfilename(defaultextension = "fqa", title = title)
        return name
        
    def askString(self, title, text):
        '''
        Proxy for Tk string entry dialog.
        '''
        string = tkSimpleDialog.askstring(title,text)
        return string
    
    def error(self, title, text):
        '''
        Proxy for Tk error box.
        '''
        tkMessageBox.showerror(title, text)

    def new_account(self):
        return self.settings()

