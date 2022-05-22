from tkinter import BOTH, CENTER, GROOVE, LEFT, RIGHT, SUNKEN, X, Button, Label, Tk, Entry, Frame
from tkinter.font import Font
import math

class NumberEntry(Entry):
    def __init__(self, parent, width = None, callback = None):
        if max != None:
            super().__init__(parent, width=width)
        else:
            super().__init__(parent)
        self._number = None;

        def validate(event):
            try:
                value = float(self.get())
                self._number = value;
                
            except ValueError:
                self._number = None
                if callback:
                    callback()

        self.bind("<KeyRelease>", validate)

    def getNumber(self):
        return self._number

class SecuredNumberEntry(Frame):
    def _init__(self, parent, min = None, max = None):
        super().__init__(parent)
        self._max = max
        self._min = min

        frm_main = Frame(self)
        frm_main.pack(fill=X, expand=True)
        lbl_error = Label(self, text="", fg='red')



        if max:
            self._entry = NumberEntry(frm_main, width=math.ceil(math.log10(max+1))+1)
        else:
            self._entry = NumberEntry(frm_main)

        #TODO: msg and color



class Stage(Frame):
    def __init__(self, parent, app):
        super().__init__(parent);
        self._parent = parent
        self._app = app

    def getApp(self):
        return self._app;
    
    def getParent(self):
        return self._parent

class Solve1Stage(Stage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.columnconfigure([0,1], weight=1)
        self.rowconfigure(0, weight=1)

        frm_container = Frame(self, borderwidth=5, relief=GROOVE)
        frm_container.grid(row=0, column=1, sticky="nsew")
        
        frm_container.rowconfigure(1, weight=1)
        frm_container.rowconfigure([0,2], weight=0, minsize=40)
        frm_container.columnconfigure(0, weight=1)

        frm_content = Frame(frm_container)
        frm_content.grid(row=1, column=0, sticky="nesw")

        frm_content.rowconfigure([0,1], weight=1)
        frm_content.columnconfigure(0, weight=1)
        frm_content.columnconfigure(1, weight=1)

        ent_nbQuality = NumberEntry(frm_content)
        ent_nbMill = NumberEntry(frm_content)
        lbl_nbQuality = Label(frm_content, text="Nombre de qualité de béton : ")
        lbl_nbMill = Label(frm_content, text="Nombre de broyeur à béton : ")
        lbl_nbQuality.grid(row=0, column=0, sticky="es")
        lbl_nbMill.grid(row=1, column=0, sticky="en")
        ent_nbQuality.grid(row=0, column=1, sticky="ws")
        ent_nbMill.grid(row=1, column=1, sticky="wn")

        frm_bottom = Frame(frm_container)
        frm_bottom.grid(row=2, column=0, sticky="nesw")

        def next():
            nbQuality = ent_nbQuality.getNumber()
            nbMill = ent_nbMill.getNumber()

            if (nbQuality != None and nbMill != None):
                self.getApp().nbQuality(nbQuality)
                self.getApp().nbMill(nbMill)
                
                self.destroy()

                stage = Solve2Stage(self.getParent(), self.getApp())
                stage.pack(fill=BOTH, expand=True)

        btn_next = Button(frm_bottom, text="Suivant", command=next, font=Font(size=12))
        btn_next.place(x=0, y=0)

class Solve2Stage(Stage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        frm_container = Frame(self, borderwidth=5, relief=GROOVE)
        frm_container.grid(row=0, column=1, sticky="nsew")

        frm_bottom = Frame(frm_container)
        frm_bottom.grid(row=2, column=0, sticky="nesw")

        def next():
            nbQuality = ent_nbQuality.getNumber()
            nbMill = ent_nbMill.getNumber()

            if (nbQuality != None and nbMill != None):
                self.getApp().nbQuality(nbQuality)
                self.getApp().nbMill(nbMill)
                self.destroy()

                stage = Solve2Stage(self.getParent(), self.getApp())
                stage.pack(fill=BOTH, expand=True)

        btn_next = Button(frm_bottom, text="Suivant", command=next, font=Font(size=12))
        btn_next.pack(side=RIGHT, padx=5)



class App():
    def __init__(self) -> None:
        window = Tk()
        self.window = window

        window.geometry("600x400")
        window.resizable(False, False)
        window.title("Optimizer")

        stage = Solve1Stage(self.window, self)
        stage.pack(fill=BOTH, expand=True)

        self.window.mainloop()
        
    def nbQuality(self, n = None):
        if n == None:
            return self._nbQuality
        self._nbQuality = n
    def nbMill(self, n = None):
        if n == None:
            return self._nbMill
        self._nbMill = n
    def prod(self, t = None):
        if t == None:
            return self._prod
        self._prod = t;
    def cost(self, t = None):
        if t == None:
            return self._cost
        self._cost = t;
    def stock_order(self, t = None):
        if t == None:
            return self._stock_order
        self._stock_order = t;
    def stock_init(self, t = None):
        if t == None:
            return self._stock_init
        self._stock_init = t;
    def stock_secu(self, t = None):
        if t == None:
            return self._stock_secu
        self._stock_secu = t;



app = App()