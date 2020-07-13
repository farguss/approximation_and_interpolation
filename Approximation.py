#!/usr/bin/python
# coding: utf8
import scipy as sp
import matplotlib.pyplot as plt
#import pandas as pd
import matplotlib.lines as lines
from matplotlib.widgets import CheckButtons

from tkinter import *
from tkinter import messagebox

def createplot(x,y):
    #fig, ax3 = plt.subplots()
    #fig.canvas.set_window_title('Approximation')
    #plt.ion()
    fig = plt.figure('Approximation')
    plt.clf()
    ax3 = fig.add_subplot(1,1,1)
    ax3.clear()
    mnk(x,y,ax3,fig)


def mnk(x,y,ax3,fig):
              #fig, ax3 = plt.subplots()
              #fig.canvas.set_window_title('Approximation')
              # plt.title("Aproximation")
              d = 1 # степень полинома
              fp, residuals, rank, sv, rcond = sp.polyfit(x, y, d, full=True) # Модель
              f = sp.poly1d(fp) # аппроксимирующая функция
              print('MNK 1')
              print('Коэффициент -- a %s  '%round(fp[0],4))
              print('Коэффициент-- b %s  '%round(fp[1],4))

              y1=[fp[0]*x[i]+fp[1] for i in range(0,len(x))] # значения функции a*x+b
              so=round(sum([abs(y[i]-y1[i]) for i in range(0,len(x))])/(len(x)*sum(y))*100,4) # средняя ошибка
              print('Average quadratic deviation '+str(so))

              fx = sp.linspace(x[0], x[-1] + 1, len(x)) # можно установить вместо len(x) большее число для интерполяции

              ax3.plot(x, y, 'o', label='Original data', markersize=10, picker = 5)
              l0, = ax3.plot(fx, f(fx), color='r', label='MNK 1', linewidth=2)


              d = 2  # степень полинома
              fp, residuals, rank, sv, rcond = sp.polyfit(x, y, d, full=True)  # Модель
              f = sp.poly1d(fp)  # аппроксимирующая функция
              print('MNK 2')
              print('Коэффициент -- a %s  ' % round(fp[0], 4))
              print('Коэффициент-- b %s  ' % round(fp[1], 4))
              print('Коэффициент -- c %s  ' % round(fp[2], 4))

              y1 = [fp[0] * x[i] ** 2 + fp[1] * x[i] + fp[2] for i in range(0, len(x))]  # значения функции a*x**2+b*x+c
              so = round(sum([abs(y[i] - y1[i]) for i in range(0, len(x))]) / (len(x) * sum(y)) * 100,
                         4)  # средняя ошибка
              print('Average quadratic deviation ' + str(so))

              fx2 = sp.linspace(x[0], x[-1] + 1, 40)  # можно установить вместо len(x) большее число для интерполяции

              l1, = ax3.plot(fx2, f(fx2), color='g', label='MNK 2', linewidth=2)


              ax3.set_visible(True)

              ax3.grid(True)



              plt.subplots_adjust(left=0.21)
              lines = [l0, l1]
              # Make checkbuttons with all plotted lines with correct visibility
              rax = plt.axes([0.05, 0.5, 0.1, 0.15])
              labels = [str(line.get_label()) for line in lines]
              visibility = [line.get_visible() for line in lines]
              check = CheckButtons(rax, labels, visibility)

              def func(label):
                  index = labels.index(label)
                  lines[index].set_visible(not lines[index].get_visible())
                  if(lines[index].get_label() != '_nolegend_'):
                      lines[index].set_label('_nolegend_')
                  else:
                      if(index == 0):
                          lines[index].set_label('MNK 1')
                      else:
                          lines[index].set_label('MNK 2')

                  ax3.legend()
                  plt.draw()

              check.on_clicked(func)

              def on_pick(event):
                  line = event.artist
                  ind = event.ind
                  xdata = line.get_xdata()
                  ydata = line.get_ydata()
                  #print('on pick line:', xdata[ind], ydata[ind])
                  j = 0
                  for i in lbox.get(0,END):
                      if('['+ i + ']' == str(xdata[ind]).replace('.]', '') + ',' + str(str(ydata[ind]).replace('[', '').replace('.]',']')) ):
                          lbox.selection_set(j)
                          j = j + 1
                      else:
                          j = j + 1
              fig.canvas.mpl_connect('pick_event', on_pick)

              ax3.legend()
              plt.show()

#x=[10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78, 82, 86]
#y=[0.1, 0.0714, 0.0556, 0.0455, 0.0385, 0.0333, 0.0294, 0.0263, 0.0238, 0.0217,
   #0.02, 0.0185, 0.0172, 0.0161, 0.0152, 0.0143, 0.0135, 0.0128, 0.0122,
   #0.0116] # данные для проверки по функции y=1/x

#x=[0, 1, 2, 4, 5]
#y=[2.1, 2.4, 2.6, 2.8, 3.0]
x=[]
y=[]

def additem():
    lbox.insert(END, entry.get())
    entry.delete(0, END)


def dellist():
    select = list(lbox.curselection())
    select.reverse()
    for i in select:
        lbox.delete(i)

def editlist():
    select = list(lbox.curselection())
    if(len(select) > 1):
        messagebox.showerror("Error", "Can not edit multiple fields")
    else:
        lbox.delete(select[0])
        lbox.insert(select[0], entry.get())
        entry.delete(0, END)

def updateplot():
    x.clear()
    y.clear()
    k = 0
    for i in lbox.get(0,END):
        j = 0
        while j < len(i):
            if(i[j] == ','):
                break
            else:
                j = j + 1
#        x.append(float(i[:j]))
 #       y.append(float(i[j+1:]))
#    createplot(x,y)
#    plt.draw()
        while True:
            try:
                x.append(float(i[:j]))
                y.append(float(i[j + 1:]))
                break
            except ValueError as e:
                    if(format(e) == 'could not convert string to float: '):
                        k = 1
                    if(format(e) != 'could not convert string to float: '):
                        k = 2
                    break
    if (k == 1):
        MsgBox = messagebox.askquestion('Warning', 'There are blank fields in the list. Are you sure you want to update the plot?',
                                       icon='warning')
        if MsgBox == 'yes':
            createplot(x, y)
            plt.draw()
        else:
            pass
    if (k == 2):
        messagebox.showerror("Error", "Error in some fields")
    if (k == 0):
        createplot(x, y)
        plt.draw()

root = Tk()

root.title("Approximation app")

root.geometry('350x200')

lbox = Listbox(selectmode=MULTIPLE)
lbox.pack(side=LEFT)
scroll = Scrollbar(command=lbox.yview)
scroll.pack(side=LEFT, fill=Y)
lbox.config(yscrollcommand=scroll.set)

f = Frame()
f.pack(side=LEFT, padx=10)
entry = Entry(f)
entry.pack(anchor=N)
badd = Button(f, text="Add", command=additem)
badd.pack(fill=X)
bdel = Button(f, text="Delete", command=dellist)
bdel.pack(fill=X)
bdel = Button(f, text="Edit", command=editlist)
bdel.pack(fill=X)


def clicked():
    k = 0
    for i in lbox.get(0,END):
        j = 0
        while j < len(i):
            if(i[j] == ','):
                break
            else:
                j = j + 1
        while True:
            try:
                x.append(float(i[:j]))
                y.append(float(i[j + 1:]))
                break
            except ValueError as e:
                    if(format(e) == 'could not convert string to float: '):
                        k = 1
                    if(format(e) != 'could not convert string to float: '):
                        k = 2
                    break
    if (k == 1):
        MsgBox = messagebox.askquestion('Warning', 'There are blank fields in the list. Are you sure you want to build the plot?',
                                       icon='warning')
        if MsgBox == 'yes':
            createplot(x, y)
        else:
            pass
    if (k == 2):
        messagebox.showerror("Error", "Error in some fields")
    if (k == 0):
        createplot(x, y)

btn = Button(f, text="Build", command=clicked)

btn.pack(fill=X)

bdel = Button(f, text="Update", command=updateplot)
bdel.pack(fill=X)

root.mainloop()
