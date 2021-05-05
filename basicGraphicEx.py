#Introduction to Computer Graphics exercise 1

from tkinter import (Button, Canvas, Entry, Label, PhotoImage, StringVar, Tk, colorchooser, Frame, Scale, Checkbutton, IntVar)
import numpy as np

#window size
width = 900
height = 600

#tkinter global vals
window = Tk()
window.title("Exercise 1: Lines, Circles, Curves")
bg_color_text = StringVar()
bg_color_text.set("#000000")
canvas = Canvas(window, width = width, height = height, bg=bg_color_text.get())
img = PhotoImage(width = width, height = height)
canvas.create_image((width // 2, height // 2), image = img, state="normal")
line_color_text = StringVar()
line_color_text.set("#ffffff")
curve_guide = IntVar()

#global drawing vals
mode = "line"
close_flag = False
points = [[0,0], [0,0], [0,0], [0,0]]
point_index = 0

#close program properly
def close_prog():
    global window, close_flag
    window.destroy()
    close_flag = True

#get mouse coordinets
def mouse_click(event):
    global point_index, points, mode, line_color_text
    points[point_index] = [event.x, event.y]
    point_index += 1
    my_circle([event.x, event.y], [event.x+3, event.y+3], line_color_text.get())
    

    #starts drawing, based on points num and mode
    if (point_index > 1 and mode != "curve") or (point_index > 3 and mode == "curve"):
        point_index = 0
        draw()


#initilize drawing
def init_draw():
    global point_index, mode
    mode_label['text'] = "Drawing Mode : " + mode
    point_index = 0

#button functions
def set_line():
    global mode
    mode = "line"
    init_draw()

def set_circle():
    global mode
    mode = "circle"
    init_draw()


def set_curve():
    global mode
    mode = "curve"
    init_draw()


def clear():
    global canvas, img
    canvas.delete(img)
    img = PhotoImage(width = width, height = height)
    canvas.create_image((width // 2, height // 2), image = img, state="normal")
    init_draw()

def set_line_colour():
    global line_color_text
    temp_color = {}
    temp_color['rgb'], temp_color['hex'] = colorchooser.askcolor()
    if temp_color['hex'] == None:
        return
    line_color_text.set(temp_color['hex'])
    line_color_label['text'] = line_color_text.get()
    line_color_label['bg'] = line_color_text.get()
    
def set_bg_colour():
    global bg_color_text, canvas
    temp_color = {}
    temp_color['rgb'], temp_color['hex'] = colorchooser.askcolor()
    if temp_color['hex'] == None:
        return
    bg_color_text.set(temp_color['hex'])
    canvas['bg'] = temp_color['hex']

#GUI buttons
button_frame = Frame(window)
mode_frame = Frame(window)
options_frame = Frame(mode_frame)
line_button = Button(button_frame, text="Line", width=16, command=set_line, activebackground = "#e3c3d7")
circle_button = Button(button_frame, text="Circle", width=16, command=set_circle, activebackground = "#e3c3d7")
curve_button = Button(button_frame, text="Curve", width=16, command=set_curve, activebackground = "#e3c3d7")
clear_button = Button(button_frame, text="Clear Art", width=16, command=clear, activebackground = "#e3c3d7")
line_color_sett = Button(button_frame, text="Line Color", width=16, command=set_line_colour, activebackground = "#e3c3d7")
line_color_label = Label(button_frame, text = line_color_text.get())
mode_label = Label(mode_frame, text= "Drawing Mode : " + mode, bg=line_color_text.get())
bg_color_sett = Button(options_frame, text="Background Color", width=16, command=set_bg_colour, activebackground = "#e3c3d7")
curve_n_label = Label(options_frame, text= "Curve Flow")
curve_n = Scale(options_frame, from_=4, to=75, orient="horizontal")
curve_guide_label = Label(options_frame, text = "show curve guide?")
curve_guide_check = Checkbutton(options_frame, variable=curve_guide)
curve_n.set(50)
options_frame.pack( side = "bottom" )
mode_frame.pack( side = "bottom" )
button_frame.pack( side = "bottom")
line_button.pack( side = "left" )
circle_button.pack( side = "left" )
curve_button.pack( side = "left" )
clear_button.pack( side = "left" )
line_color_sett.pack( side = "left" )
line_color_label.pack( side = "left" )
mode_label.pack()
bg_color_sett.pack( side = "left" )
curve_n_label.pack(side = "left" )
curve_n.pack( side = "left" )
curve_guide_label.pack( side = "left" )
curve_guide_check.pack(side = "left")


#close window
window.protocol("WM_DELETE_WINDOW", close_prog)
#mouse clicks
canvas.bind("<Button-1>", mouse_click)
canvas.pack()


#single pixel drawing
def put_pixel(x, y, color):
    global canvas, img

    if x < 0 or y < 0:
        return
    img.put(color, (x,y))


#full bresenheim line algorithm
def my_line(point1, point2, color):
    x1, y1 = point1
    x2, y2 = point2

    if((abs(x1-x2) >= abs(y1-y2) and x1 > x2) or (abs(y1-y2) > abs(x1-x2) and y1 > y2 )):
        x1, x2, y1, y2 = x2, x1, y2, y1
    
    dx = x2 - x1
    dy = y2 - y1

    offset_x = 1 if dx >= 0 else -1
    offset_y = 1 if dy >= 0 else -1

    dir = 'x' if abs(dx) >= abs(dy) else 'y'
    errp = abs(2 * dy - dx) if dir =='x' else abs(2* dx - dy)
    x = x1
    y = y1

    for i in range(abs(dx) if dir == 'x' else abs(dy)):
        put_pixel(x, y, color)

        if dir == 'x':
            if errp > 0:
                y = y + offset_y
                put_pixel(x, y, color)
                errp = errp - abs(2 * dx)
            x = x + 1
            errp = errp + abs(2 * dy)

        else:
            if errp > 0:
                x = x + offset_x
                put_pixel(x, y, color)
                errp = errp - abs(2 * dy)
            y = y + 1
            errp = errp + abs (2 * dx) 


#1/8 circle pixels algorithm
def put_circle_pix(x_center, y_center, x, y, color):
    put_pixel(x_center + x, y_center + y, color)
    put_pixel(x_center + x, y_center - y, color)
    put_pixel(x_center + y, y_center + x, color)
    put_pixel(x_center + y, y_center - x, color)
    put_pixel(x_center - x, y_center + y, color)
    put_pixel(x_center - x, y_center - y, color)
    put_pixel(x_center - y, y_center + x, color)
    put_pixel(x_center - y, y_center - x, color)

#full circle algorithm
def my_circle(point1, point2, color):
    x1, y1 = point1
    x2, y2 = point2
    x = 0
    
    radius = int(np.sqrt((x2 - x1) ** 2 + (y2 - y1) **2))
    y = radius
    p = 3 - 2 * radius

    while x < y :
        put_circle_pix(x1, y1, x, y, color)
        if p < 0:
            p = p + 4 * x + 6
        
        else:
            put_circle_pix(x1, y1, x + 1 ,y, color)
            p = p+ 4*(x-y) + 10
            y = y-1
        
        x = x +1
    
    if x == y:
        put_circle_pix(x1, y1, x, y, color)


#full curve algorithm
def my_curve(points, color):
    global curve_n, curve_guide
    x1 ,y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    x4, y4 = points[3]
    curr_x = x1
    curr_y = y1
    guide_color = '#00ff00'
    mb = [[-1,3,-3,1],
        [3, -6, 3, 0],
        [-3, 3, 0,0],
        [1, 0, 0, 0]]
    mx = [[x1],[x2],[x3],[x4]]
    my = [[y1],[y2],[y3],[y4]]

    if curve_guide.get() == 1:
        my_line(points[0], points[1], guide_color)
        my_line(points[2], points[3], guide_color)
    #calculate x & y matrix
     

    # loops through
    for i in range(curve_n.get()):
        t = i / curve_n.get()
        mt = [t**3, t**2, t, 1]
        mtb = np.dot(mt, mb)
        x = int(np.dot(mtb, mx))
        y = int(np.dot(mtb, my))

        my_line([x,y], [curr_x, curr_y], color)
        # updates initial values
        curr_x = x
        curr_y = y
    my_line([curr_x, curr_y], [x4, y4], color)


#initiate drawing on screen
def draw():
        if mode == 'line':
            my_line(points[0], points[1], line_color_text.get())
        elif mode == 'circle':
            my_circle(points[0], points[1], line_color_text.get())
        elif mode == 'curve':
            my_curve(points, line_color_text.get())


#program main
def main():
    window.mainloop()

if __name__ == '__main__':
    main()
