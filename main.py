from tkinter import *
from glob import glob
from tkinter.messagebox import askyesno, showwarning, showinfo
from tkinter.colorchooser import askcolor
import subprocess


Size = (640, 480)


class PyPlot(Frame):
    def __init__(self, parent=None, picdir='.', size=Size, **args):
        """Констуктор главного окна программы.

        """
        Frame.__init__(self, parent, **args)
        self.size = size
        self.makeWidgets()
        self.pack(expand=YES, fill=BOTH)
        self.opens = picdir
        self.drawn = None

    def setBgColor(self):
        """Функция, отвечающая за изменение заднего фона

        Использует messagebox(askcolor) встроенный в tkinter.
        """
        (triple, hexstr) = askcolor()
        if hexstr:
            print(hexstr)
            self.config(bg=hexstr)

    def OnEntry(self, input_str):
        '''Функция, которая выполняет свою работу после того как пользователь нажал на кнопку Entry или на Enter

        Используется модуль subprocess. Для того что бы передать модулю plotter ввод пользователя. В свою очередь
        plotter создаст файл plot.png.
        Если plotter.py выдаст исключение, то функция OnEntry используя messagebox (showwarning) покажет диалоговое
        окно пользователю.
        '''
        a = subprocess.check_output(
            ["python3", "plotter.py", input_str], universal_newlines=True)

        if a:
            showwarning('WARNING', a)


    def makeWidgets(self):
        """Функция , которая строит виджеты

        Строятся виджеты. Настраиваются обработчики.
        """
        ent = Entry(relief=SUNKEN, width=50)
        ent.insert(0, 'Type function here')
        ent.focus()
        ent.bind('<Return>', (lambda event: self.OnEntry()))  # on enter key
        ent.pack()
        Button(text='Entry', command=lambda: self.OnEntry(ent.get())).pack()
        height, width = self.size
        self.canvas = Canvas(self, bg='white', height=height, width=width)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        Button(self, text='Plot', command=self.onPlot).pack(fill=X)
        Button(
            self,
            text="set Background collor",
            command=self.setBgColor).pack(
            fill=X)
        Button(self, text='Help', command=self.onHelp).pack(fill=X)
        Button(self, text='Quit', command=self.onQuit).pack(fill=X)

    def onHelp(self):
        """Функция, которая сработает если нажать на кнопку Help

        Является функцией справки. Открывает файл help.txt. И помещает информацию на диалоговое окно showinfo
        """
        win = Toplevel()
        help = open('help.txt')
        help_mess = help.read()
        help.close()
        #showinfo('Help', help_mess)
        msg = Message(win, text=help_mess)
        msg.config(font=('times',16,'italic'))
        msg.pack(fill=X, expand=YES)
        win.mainloop()

    def onPlot(self):
        """Отрисовывает график введенной фунции.

        """
        name = './plot.png'
        if self.drawn:
            self.canvas.delete(self.drawn)
        img = PhotoImage(file=name)
        self.canvas.config(height=img.height(), width=img.width())
        self.drawn = self.canvas.create_image(2, 2, image=img, anchor=NW)
        self.image = name, img

    def onQuit(self):
        """Функция , которая сработает при нажатии на кнопку Quit

        Функция, использует диалоговое окно askyesno
        Используя встроенный метод класса Frame завершает работу программы.
        """
        self.update()
        if askyesno('PyView', 'Really quit now?'):
            self.quit()


if __name__ == '__main__':
    root = Tk()
    root.geometry('800x560')
    root.title('PyPlotter 1.0')
    root.resizable(width=False, height=False)
    Label(root, text="Python Graph Plotter").pack()
    PyPlot(root, bd=3, relief=SUNKEN)
    root.mainloop()
