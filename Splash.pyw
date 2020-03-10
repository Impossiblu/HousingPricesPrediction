import tkinter as tk
root = tk.Tk()
root.overrideredirect(True)
width = 425
height = 425
posR = int(root.winfo_screenwidth()/2 - 425/2)
posL = int(root.winfo_screenheight()/2 - 425/2)
root.geometry("+{}+{}".format(posR,posL))
image_file = "SplashScreen.gif"
image = tk.PhotoImage(file=image_file)
canvas = tk.Canvas(root, height=height*1, width=width*1, bg="darkgrey")
canvas.create_image(width*1/2, height*1/2, image=image)
canvas.pack()
root.after(5000, root.destroy)
root.mainloop()


import gui


