import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import numpy as np
from sympy import symbols, diff, integrate
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning, showinfo

class FunctionPlotter:
    def __init__(self, window):
        self.window = window
        self.window.title("Graphy")
        self.window.geometry("1366x768")

        # Frame pour les paramètres
        self.fr1 = Frame(window, highlightbackground="DarkOrange1", highlightthickness=2, bd=5)
        self.fr1.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

        # Frame pour le graphique
        self.fr2 = Frame(window, highlightbackground="black", highlightthickness=2, bd=5)
        self.fr2.grid(row=1, column=1, padx=10, pady=10)

        # Variables pour les fonctions et l'intervalle
        self.func_txt = StringVar(value="Expressions (une par ligne) :")
        self.label_func = Label(self.fr1, textvariable=self.func_txt, justify=RIGHT, height=4, font=("Arial", 12))
        self.label_func.grid(row=1, column=0)
        self.func_entry = Text(self.fr1, borderwidth=3, bg="white", height=10, width=30)
        self.func_entry.grid(row=1, column=1, columnspan=3)

        self.a_txt = StringVar(value="A:")
        self.label_a = Label(self.fr1, textvariable=self.a_txt, justify=RIGHT, anchor="w", height=4, font=("Arial", 12))
        self.label_a.grid(sticky=E, row=2, column=0)
        self.a_entry = Entry(self.fr1, width=10, borderwidth=3, bg="powder blue")
        self.a_entry.grid(sticky=W, row=2, column=1)

        self.b_txt = StringVar(value="B:")
        self.label_b = Label(self.fr1, textvariable=self.b_txt, justify=RIGHT, anchor="w", height=4, font=("Arial", 12))
        self.label_b.grid(sticky=E, row=3, column=0)
        self.b_entry = Entry(self.fr1, width=10, borderwidth=3, bg="powder blue")
        self.b_entry.grid(sticky=W, row=3, column=1)

        # Style
        self.style_txt = StringVar(value="Style")
        self.label_style = Label(self.fr1, textvariable=self.style_txt, justify=RIGHT, anchor="w", height=4, font=("Arial", 12))
        self.label_style.grid(sticky=E, row=4, column=0)
        self.style_combo = ttk.Combobox(self.fr1, values=["-", "--", "-.", ":"], state="readonly", width=8)
        self.style_combo.grid(sticky=W, row=4, column=1)
        self.style_combo.set("-")

        # Couleur
        self.color_txt = StringVar(value="Couleur")
        self.label_color = Label(self.fr1, textvariable=self.color_txt, justify=RIGHT, anchor="w", height=4, font=("Arial", 12))
        self.label_color.grid(sticky=E, row=5, column=0)
        self.color_combo = ttk.Combobox(self.fr1, values=["red", "blue", "green", "black", "orange","purple"], state="readonly", width=8)
        self.color_combo.grid(sticky=W, row=5, column=1)
        self.color_combo.set("blue")

        # Dérivée
        self.diriv_txt = StringVar(value="Dérivée:")
        self.label_diriv = Label(self.fr1, textvariable=self.diriv_txt, justify=RIGHT, anchor="w", height=4, font=("Arial", 12))
        self.label_diriv.grid(sticky=E, row=6, column=0)
        self.res_txt = StringVar()
        self.res_diriv = Label(self.fr1, textvariable=self.res_txt, justify=RIGHT, anchor="w", width=10, borderwidth=3, bg="powder blue")
        self.res_diriv.grid(sticky=W, row=6, column=1)

        # Slider pour le dérivée
        self.s_txt = StringVar(value="Ordre du Dérivée:")
        self.label_s = Label(self.fr1, textvariable=self.s_txt, justify=RIGHT, anchor="w", height=4, font=("Arial", 12))
        self.label_s.grid(sticky=E, row=7, column=0)
        self.slider = Scale(self.fr1, from_=1, to=5, orient=HORIZONTAL)
        self.slider.grid(sticky=W, row=7, column=1)

        # Primitive
        self.pri_txt = StringVar(value="Primitive:")
        self.label_pri = Label(self.fr1, textvariable=self.pri_txt, justify=RIGHT, anchor="w", font=("Arial", 12))
        self.label_pri.grid(sticky=E, row=8, column=0)
        self.resp_txt = StringVar()
        self.res_prim = Label(self.fr1, textvariable=self.resp_txt, justify=RIGHT, anchor="w", width=10, borderwidth=3, bg="powder blue")
        self.res_prim.grid(sticky=W, row=8, column=1)

        # Bouton principal pour tracer les graphes
        self.plot_button = Button(self.fr1, width=15, text="Afficher", bg="powder blue", command=self.plot, font=("Arial", 12))
        self.plot_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Check buttons
        self.chbd_txt = StringVar(value="Afficher le dérivé")
        self.label_chbd = Label(self.fr1, textvariable=self.chbd_txt, justify=RIGHT, anchor="w", font=("Arial", 12))
        self.label_chbd.grid(sticky=E, row=10, column=0)
        self.chbd = BooleanVar()
        self.chbd.set(False)
        self.res_chbd = Checkbutton(self.fr1, var=self.chbd, justify=RIGHT, anchor="w", width=10, borderwidth=3, command=self.update_plot,activebackground="green")
        self.res_chbd.grid(sticky=W, row=10, column=1)

        self.chbp_txt = StringVar(value="Afficher le primitive")
        self.label_chbp = Label(self.fr1, textvariable=self.chbp_txt, justify=RIGHT, anchor="w", font=("Arial", 12))
        self.label_chbp.grid(sticky=E, row=11, column=0)
        self.chbp = BooleanVar()
        self.res_chbp = Checkbutton(self.fr1, var=self.chbp, justify=RIGHT, anchor="w", width=10, borderwidth=3, command=self.update_plot,activebackground="red")
        self.res_chbp.grid(sticky=W, row=11, column=1)


        # Initialisation du graphique
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Graphe de f", fontsize=16)
        self.ax.set_ylabel("y", fontsize=14)
        self.ax.set_xlabel("x", fontsize=14)
        self.ax.set_facecolor("white")
        self.ax.grid(True)

        # Pan/Zoom
        self.ax.callbacks.connect('xlim_changed', self.update_plot)
        self.ax.callbacks.connect('ylim_changed', self.update_plot)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.fr2)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.draw()

        self.x = symbols('x')
        self.lines = [] # Stocker toutes les courbes

    def plot(self):
        # Récupérer les informations
        try:
            func_strings = [line.strip().lower() for line in self.func_entry.get("1.0", "end").splitlines() if line.strip()]
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            style = self.style_combo.get()
            color = self.color_combo.get()
            deriv_order = self.slider.get()
        except ValueError:
            showwarning("Erreur", "Veuillez vérifier les valeurs entrées")
            return

        self.ax.cla()
        self.ax.grid(True)
        self.ax.set_title("Graphe de f", fontsize=16)
        self.ax.set_ylabel("y", fontsize=14)
        self.ax.set_xlabel("x", fontsize=14)

        # Préparation de l'intervalle
        self.t = np.linspace(a, b, 1001)

        # Stocker la dernière fonction tracé
        last_func = None
        self.lines = []
        for func_str in func_strings:
            try:
                # Remplacer les fonctions mathématiques par celles de numpy
                func_str_np = func_str.replace("sin", "np.sin")
                func_str_np = func_str_np.replace("cos", "np.cos")
                func_str_np = func_str_np.replace("tan", "np.tan")
                func_str_np = func_str_np.replace("exp", "np.exp")
                func_str_np = func_str_np.replace("sqrt", "np.sqrt")
                func_str_np = func_str_np.replace("log", "np.log")
                func_str_np = func_str_np.replace("pi", "np.pi")

                f = lambda x: eval(func_str_np)
                pp = np.vectorize(f)

                # Tracé de la fonction
                line, = self.ax.plot(self.t, pp(self.t), label=func_str, linestyle=style, color=color)
                self.lines.append(line)

                # Stock la dernière fonction
                last_func = func_str
            except Exception as e:
                showwarning("Erreur", f"Erreur d'évaluation de l'expression : {e}")
                continue

            # Calcul de la dérivée
            if self.chbd.get() and last_func:
                try :
                    p = last_func.replace("np.","")
                    D = diff(p, self.x, deriv_order)
                    d = lambda x: eval(str(D).replace("np.", ""))
                    d_vect = np.vectorize(d)

                    deriv_line, = self.ax.plot(self.t, d_vect(self.t), color="green", label=f"Dérivée de {last_func}", linestyle="--")
                    self.lines.append(deriv_line)
                    self.res_txt.set(D)
                except :
                    showwarning("Erreur", f"Erreur de calcule du dérivé")

            # Calcul de la primitive
            if self.chbp.get() and last_func:
                try :
                    p = last_func.replace("np.","")
                    I = integrate(p, self.x)
                    i = lambda x: eval(str(I).replace("np.", ""))
                    i_vect = np.vectorize(i)
                    primitive_line, = self.ax.plot(self.t, i_vect(self.t), color="red", label=f"Primitive de {last_func}", linestyle="-.")
                    self.lines.append(primitive_line)
                    self.resp_txt.set(I)
                except :
                    showwarning("Erreur", f"Erreur de calcule de la primitive")

        self.ax.legend()
        self.canvas.draw()

    def update_plot(self, *args):
        """Mettre a jours le graph en cas de modification du graphe(pan, zoom,...)"""
        self.canvas.draw()
    
if __name__ == '__main__':
    window = Tk()
    plotter = FunctionPlotter(window)
    window.mainloop()