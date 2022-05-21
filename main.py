from tkinter import W, Label
import numpy as np


def main(cheat):
    import tkinter as tk


    class NumberEntry(tk.Frame):
        def __init__(self, parent):
            super().__init__(self, parent)

            def validate():
                try:
                    n = float(self.number)
                    self.number = n;
                except ValueError:
                    self.number = None

            self.ent = tk.Entry(self, textvariable=self.number, validate="focusout", validatecommand= validate)
            self.ent.pack()

            self.number

        def getNumber(self):
            return self.number

    def createEntryMatrix(parent, row, col, entryWidth = 4, pad = 5):
        t = []
        for i in range(row):
            t.append([])
            for j in range(col):
                ent = tk.Entry(parent, width=entryWidth)
                t[i].append(ent)
                ent.grid(row=i, column=j, padx=pad, pady=pad)
        return t

    class App(tk.Tk):
        def __init__(self, lpresult, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)
            self.geometry("600x400")

            self._container = tk.Frame(self)
            self._container.pack(fill=tk.BOTH)

            self._nbQuality = 0
            self._nbMill = 0

            self._prod = []
            self._cost = []
            self._stock_order = []
            self._stock_init = []
            self._stock_secu = []

            if not lpresult:
                stage = FirstPage(self._container, self)
                stage.pack(fill=tk.BOTH)
            else:
                import numpy as np
                self._nbQuality = 4
                self._nbMill = 3
                self._prod = np.array([[50,50,30,30],[60,50,50,40],[80,80,80,70]])
                self._cost = np.array([[80,120,120,80],[100,150,100,120],[150,140,150,130]])
                self._stock_order = np.array([[7000],[2000],[8000],[2000]])
                self._stock_init = np.array([[2000],[0],[2000],[1000]])
                self._stock_secu = np.array([[1000],[1000],[2000],[1000]])
                ResultPage(self._container, self)
        
        def container(self, e = None):
            if e == None:
                return self._container
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

    class FirstPage(tk.Frame):
        def __init__(self, parent, app : App):
            super().__init__(parent)
            self.app = app

            self._container = tk.Frame(self)
            self._container.grid(row=0, column=1)
            self.columnconfigure([0,1], weight=1)

            self.ent_nbQuality = tk.Entry(self._container)
            lbl_nbQuality = tk.Label(self._container, text="Nombre de qualité de béton : ")
            lbl_nbQuality.grid(row=0,column=0, sticky="w")
            self.ent_nbQuality.grid(row=0, column=1, sticky="e")

            self.ent_nbMill = tk.Entry(self._container)
            lbl_nbMill = tk.Label(self._container, text="Nombre de broyeur à béton : ")
            lbl_nbMill.grid(row=1,column=0, sticky="w")
            self.ent_nbMill.grid(row=1, column=1, sticky="e")

            self._btn_next = tk.Button(self._container, text="Suivant", command=self.next)
            self._btn_next.grid(row=3, column=1)

            
        def next(self):
            try:
                n = int(self.ent_nbQuality.get())
                self.app.nbQuality(n)

                n = int(self.ent_nbMill.get())
                self.app.nbMill(n)
            except ValueError:
                return False

            self.destroy()

            stage = SecondPage(self.app.container(), self.app)
            stage.pack()
        
    class SecondPage(tk.Frame):
        def __init__(self, parent, app : App):
            super().__init__(parent)
            self.app = app

            self._container = tk.Frame(self)
            self._container.grid(row=0, column=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=2)

            lbl_prod = tk.Label(self._container, text="Production")
            lbl_prod.grid(row=0,column=0, sticky="nswe")

            lbl_quality = tk.Label(self._container, text="qualité")
            lbl_quality.grid(row=0,column=1, sticky="we")

            lbl_mill = tk.Label(self._container, text="broyeur")
            lbl_mill.grid(row=1,column=0, sticky="ns")

            frm_matrix = tk.Frame(self._container)
            frm_matrix.grid(row=1, column=1)
            self.ents = createEntryMatrix(frm_matrix, app.nbMill(), app.nbQuality())

            self._btn_next = tk.Button(self._container, text="Suivant", command=self.next)
            self._btn_next.grid(row=3, column=1)

        def next(self):
            try:
                t = []

                for i in range(self.app.nbMill()):
                    t.append([])
                    for j in range(self.app.nbQuality()):
                        n = int(self.ents[i][j].get())
                        t[i].append(n)
                self.app.prod(t)
            except ValueError:
                return False
            
            self.destroy()

            stage = ThirdPage(self.app.container(), self.app)
            stage.pack()
        
    class ThirdPage(tk.Frame):
        def __init__(self, parent, app : App):
            super().__init__(parent)
            self.app = app

            self._container = tk.Frame(self)
            self._container.grid(row=0, column=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=2)

            lbl_cost = tk.Label(self._container, text="Cout par production")
            lbl_cost.grid(row=0,column=0, sticky="nswe")

            lbl_quality = tk.Label(self._container, text="qualité")
            lbl_quality.grid(row=0,column=1, sticky="we")

            lbl_mill = tk.Label(self._container, text="broyeur")
            lbl_mill.grid(row=1,column=0, sticky="ns")

            frm_matrix = tk.Frame(self._container)
            frm_matrix.grid(row=1, column=1)
            self.ents = createEntryMatrix(frm_matrix, app.nbMill(), app.nbQuality())

            self._btn_next = tk.Button(self._container, text="Suivant", command=self.next)
            self._btn_next.grid(row=3, column=1)

        def next(self):
            try:
                t = []

                for i in range(self.app.nbMill()):
                    t.append([])
                    for j in range(self.app.nbQuality()):
                        n = int(self.ents[i][j].get())
                        t[i].append(n)
                self.app.cost(t)
            except ValueError:
                return False
            
            self.destroy()

            stage = FourthPage(self.app.container(), self.app)
            stage.pack()
    
    class FourthPage(tk.Frame):
        def __init__(self, parent, app : App):
            super().__init__(parent)
            self.app = app

            self._container = tk.Frame(self)
            self._container.grid(row=0, column=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=2)

            lbl_stck = tk.Label(self._container, text="Stocks")
            lbl_stck.grid(row=0,column=0, sticky="nswe")

            lbl_quality = tk.Label(self._container, text="qualité")
            lbl_quality.grid(row=0,column=1, sticky="we")

            lbl_stcki = tk.Label(self._container, text="Stock initial")
            lbl_stcki.grid(row=1,column=0, sticky="nswe")
            frm_matrix1 = tk.Frame(self._container)
            frm_matrix1.grid(row=1, column=1)
            self.ents1 = createEntryMatrix(frm_matrix1, 1, app.nbQuality())
            
            lbl_stcko = tk.Label(self._container, text="Stock commandé")
            lbl_stcko.grid(row=2,column=0, sticky="nswe")
            frm_matrix2 = tk.Frame(self._container)
            frm_matrix2.grid(row=2, column=1)
            self.ents2 = createEntryMatrix(frm_matrix2, 1, app.nbQuality())
            
            lbl_stcks = tk.Label(self._container, text="Stock de secu")
            lbl_stcks.grid(row=3,column=0, sticky="nswe")
            frm_matrix3 = tk.Frame(self._container)
            frm_matrix3.grid(row=3, column=1)
            self.ents3 = createEntryMatrix(frm_matrix3, 1, app.nbQuality())

            self._btn_next = tk.Button(self._container, text="Suivant", command=self.next)
            self._btn_next.grid(row=5, column=1)

        def next(self):
            try:
                t = []

                for j in range(self.app.nbQuality()):
                    n = int(self.ents1[0][j].get())
                    t.append(n)
                self.app.stock_init(t)

                t = []

                for j in range(self.app.nbQuality()):
                    n = int(self.ents2[0][j].get())
                    t.append(n)
                self.app.stock_order(t)

                t = []

                for j in range(self.app.nbQuality()):
                    n = int(self.ents3[0][j].get())
                    t.append(n)
                self.app.stock_secu(t)
            except ValueError:
                return False
            
            self.destroy()

            ResultPage(self.app.container(), self.app)


    class ResultPage(tk.Frame):
        def __init__(self, parent, app : App):
            tk.Frame.__init__(self, parent)
            self.pack()

            self.app = app

            from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpStatus
            import numpy as np

            model = LpProblem(sense=LpMinimize)

            prod = np.array(self.app.prod())
            print(prod)
            cost = np.array(self.app.cost())

            stock_init = np.array(self.app.stock_init())
            stock_order = np.array(self.app.stock_order())
            stock_secu = np.array(self.app.stock_secu())

            T = []
            for i in range(self.app.nbMill()):
                Ti = []
                for j in range(self.app.nbQuality()):
                    Ti.append(LpVariable(name=f"X{i}_{j}", lowBound=0, upBound=144))
                T.append(Ti)
            T = np.array(T)

            for i in range(self.app.nbQuality()):
                model += lpSum(T[:, i] * prod[:, i]) >= stock_secu[i] - stock_init[i] + stock_order[i]
           
            model += lpSum(0.1 * T * prod * cost)

            model.solve()

            finalCost = model.objective.value()

            lbl_feasible = Label(self, text=f"Status : {LpStatus[model.status]}")
            lbl_feasible.pack()
            lbl_cost = Label(self, text=f"Cout finale : {finalCost}€")
            lbl_cost.pack()

            frm_sols = tk.Frame(self)
            print(model.variables())
            for i,j in enumerate(model.variables()):
                lbl_name = tk.Label(frm_sols, text=j.name)
                lbl_name.grid(row=0, column=i)
                lbl_sol = tk.Label(frm_sols, text=j.value())
                lbl_sol.grid(row=1, column=i)
            frm_sols.pack()

    app = App(lpresult = cheat)
    app.mainloop()

if __name__ == "__main__":
    import sys

    cheat = False
    if len(sys.argv) > 1:
        cheat = True
    main(cheat)

