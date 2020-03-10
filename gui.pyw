import csv
import tkinter
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.filedialog import FileDialog
from tkinter.ttk import *
import shutil
import os.path
from Main import MainPredict 


def get_prediction(trn, tst):
    try:
        shutil.copyfile(trn, "train.csv")  # Moves test and train to location where main can use it
        shutil.copyfile(tst, "test.csv")
    except:
        pass

    MainPredict(trn, tst)

    lb3 = Label(window, text="Predicted Data: ", font=("Arial", 10), anchor='e')
    lb3.grid(column=1, row=5, sticky="ew")

    #dsp = Entry(font=("bold", 10))
    #sva = Button(text="Save As")
    #dsp.grid(column=2, row=5,)
    #sva.grid(column=3, row=5)
    #sva.bind("<Button-1>", lambda e: save_as())

    listbox = Listbox(window)
    listbox.grid(column=2,row =5, sticky="ew")

    scrollbar = Scrollbar(window)
    scrollbar.grid(column=2, row=5, sticky="ns",padx=200)

    listbox.config(xscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.xview)

    # bind listbox to scrollbar
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    with open("submission.csv", newline="") as file:
        reader = csv.reader(file)
        c = True
        for row in reader:
            for col in row:
                c = not c
                if c:
                    listbox.insert(END,row)


"""def save_as():
    dire = filedialog.askdirectory(parent=window)
    shutil.copyfile("submission.csv", dire + "/submission.csv")

"""
class Browse(Frame):
    def __init__(self, master, text):
        super().__init__(master)
        self.filepath = StringVar()
        self.text = text
        self.initaldir = 'C:/'
        self.filetypes = (('Comma Separated Values', '*.csv'),
                          ("All files", "*.*"))
        self.create_widgets()

    def create_widgets(self):
        self.ent = Entry(self, textvariable=self.filepath, font=("bold", 10))
        a = self.ent
        self.bt = Button(self, text=self.text, command=self.browse)
        self.ent.pack(fill='x', expand=TRUE, side=LEFT)
        self.bt.pack(side=LEFT)

    def get_filename(self):
        try:
            open(self.ent.get(), "r")
        except:
            messagebox.showerror(title="Error: File not Found.", message="The file you entered does not exist.")
        return self.ent.get().replace('/', '//')

    def browse(self):
        self.filepath.set(filedialog.askopenfilename(initialdir=self.initaldir, filetypes=self.filetypes))


window = tkinter.Tk()
s = ttk.Style()
# print(s.theme_names())
s.theme_use('xpnative')  # clam

window.title("House Price Predictor")
window.geometry('600x500')
window.resizable(False, False)

window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=3)
window.grid_columnconfigure(3, weight=1)

lb0 = tkinter.Label(window, text="   House Prices Prediction", justify='center', font=("Arial", 20))
lbt = tkinter.Label(window, text="Team 45", justify='center', font=("Arial", 13))


lbl = tkinter.Label(window, text="Training Data: ", font=("Arial", 10), anchor='e')
lb2 = tkinter.Label(window, text="Test Data: ", font=("Arial", 10), anchor='e')

ftrn = Browse(window, "Browse")
ftst = Browse(window, "Browse")

btd = tkinter.Button(window, text="Calculate")
btd.bind("<Button-1>", lambda e: get_prediction(ftrn.get_filename(), ftst.get_filename()))

lb0.grid(column=0, row=0, columnspan=4)
lbt.grid(column=0, row=1, columnspan=4, ipady=20, ipadx=20)
lbl.grid(column=1, row=2, sticky="ew", ipady=5, ipadx=20)
lb2.grid(column=1, row=3, sticky="ew", ipady=5, ipadx=20)

ftrn.grid(column=2, row=2, sticky="ew", ipady=5, ipadx=20)
ftst.grid(column=2, row=3, sticky="ew", ipady=5, ipadx=20)

btd.grid(column=0, row=4, columnspan=4, ipady=40, ipadx=50)

#This code is for changing the screen to blue mode
"""
window.configure(bg='#1252b8')
lb0.configure(bg='#1252b8')
lbt.configure(bg='#1252b8')
lbl.configure(bg='#1252b8')
lb2.configure(bg='#1252b8')
"""

window.mainloop()
