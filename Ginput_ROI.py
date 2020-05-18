#!/usr/bin/env python
# coding: utf-8



import matplotlib
matplotlib.use('GTK3Cairo')  # or ''
import matplotlib.pyplot as plt

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pydicom
import numpy as np

PATH = "D:\\下載\\gLymph test-20200429T121458Z-001\\gLymph test\\S5010 T2\\"


img = pydicom.read_file(PATH+'I110').pixel_array

fig, ax = plt.subplots()
plt.imshow(img, cmap = plt.cm.bone)
manager = fig.canvas.manager
# you can access the window or vbox attributes this way
toolbar = manager.toolbar
vbox = manager.vbox

# now let's add a button to the toolbar
# button = Gtk.Button(label='Click me')
# button.show()
# button.connect('clicked', lambda button: print('hi mom'))

# toolitem = Gtk.ToolItem()
# toolitem.show()
# toolitem.set_tooltip_text('Click me for fun and profit')
# toolitem.add(button)

# pos = 8  # where to insert this in the mpl toolbar
# toolbar.insert(toolitem, pos)

# now let's add a widget to the vbox
label = Gtk.Label()
label.set_markup('Drag mouse over axes for position')
label.show()
vbox.pack_start(label, False, False, 0)
vbox.reorder_child(toolbar, -1)
position = []
def on_press(event):
    motion = str(event.button)
    x_position = int(event.xdata)
    y_position = int(event.ydata)
    if motion == "MouseButton.LEFT":
        print("store your position ", x_position, y_position)
        position.append([x_position, y_position])
        ax.plot(np.array(position)[:, 0], np.array(position)[:, 1], 'r')
        
    elif motion == "MouseButton.RIGHT":
        print("remove your position ", x_position, y_position)
        try:
            position.remove([x_position, y_position])
        except:
            print("please retry")
            
    if (len(position)>1) & (motion == "MouseButton.LEFT") & (position[0] == [x_position, y_position]):
        print("finished")
        

cid = fig.canvas.mpl_connect('button_press_event', on_press)

plt.show()

