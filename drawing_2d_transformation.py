#Introduction to Computer Graphics exercise 2

from tkinter import (Button, Canvas, Entry, Label, PhotoImage, StringVar, Tk, colorchooser, Frame, Scale, Checkbutton, IntVar, Radiobutton)
import numpy as np
from numpy.lib.financial import mirr
import json

#window size
width = 900
height = 600

#open JSON file
f = open('example.JSON')
data = json.load(f)
f.close()


#draw from file
def draw_data():
    color = '#ffffff'
    for i in data['lines']:
        point = i['point']
        color = i['color']
        my_line([point[0][0],point[0][1]],[point[1][0],point[1][1]],color)
    for i in data['circles']:
        point = i['point']
        color = i['color']
        my_circle([point[0][0],point[0][1]],[point[1][0],point[1][1]],color)
    for i in data['curves']:
        point = i['point']
        color = i['color']
        my_curve([[point[0][0],point[0][1]],[point[1][0],point[1][1]],[point[2][0],point[2][1]],[point[3][0],point[3][1]]],color)



#tkinter global vals
window = Tk()
window.title("Exercise 2: 2D Transformations")
bg_color_text = StringVar()
bg_color_text.set("#000000")
canvas = Canvas(window, width = width, height = height, bg=bg_color_text.get())
img = PhotoImage(width = width, height = height)
canvas.create_image((width // 2, height // 2), image = img, state="normal")
line_color_text = StringVar()
line_color_text.set("#ffffff")
curve_guide = IntVar()
click_circle = IntVar()
mirror_axis = StringVar()
mirror_axis.set('x')


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
    if(click_circle.get()):
        my_circle([event.x, event.y], [event.x+3, event.y+3], line_color_text.get())
    

    #starts drawing, based on points num and mode
    if( mode == "mirror" and point_index == 1):
        point_index = 0
        draw()
    elif (mode == "rotate" and point_index == 3):
        point_index = 0
        draw()
    elif (point_index > 1 and mode != "curve" and mode != "rotate") or (point_index > 3 and mode == "curve"):
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
    help_text['text'] = "Tip! Click on 2 points on the screen to make a line"
    init_draw()

def set_circle():
    global mode
    mode = "circle"
    init_draw()
    help_text['text'] = "Tip! Click on 2 points on the screen to make a circle. 1st is the center, second is on the radius"


def set_curve():
    global mode
    mode = "curve"
    help_text['text'] = "Tip! Click on 4 points on the screen to make a curve. 1st and 4th are the start and end, 2nd and 3rd decide the curvature"
    init_draw()

def set_trans():
    global mode
    mode = "trans"
    help_text['text'] = "Tip! Click on 2 points on the screen to make the drawing in the direction and distance"
    init_draw()

def set_scale_big():
    global mode
    mode = "scale big"
    help_text['text'] = "Tip! Click on 2 points on the screen to make the drawing bigger"
    init_draw()

def set_scale_small():
    global mode
    mode = "scale small"
    help_text['text'] = "Tip! Click on 2 points on the screen to make the drawing smaller"
    init_draw()

def set_mirror():
    global mode
    mode = "mirror"
    help_text['text'] = "Tip! Click on the screen to mirror the drawing. You can change the mirror axis in the options"
    init_draw()

def set_shearing():
    global mode
    mode = "shearing"
    init_draw()

def set_rotate():
    global mode
    mode = "rotate"
    help_text['text'] = "Tip! Click on 3 points on the screen to make a line. The first line is the origin, and the other 2 decide the angle"
    init_draw()

def clear():
    global canvas, img
    canvas.delete(img)
    img = PhotoImage(width = width, height = height)
    canvas.create_image((width // 2, height // 2), image = img, state="normal")
    init_draw()

def clear_data():
    global data
    data = {"lines" : [], "circles": [], "curves": []}
    clear()

def save_file():
    with open ('output.JSON', 'w') as outfile:
        json.dump(data,outfile)

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

def load_example():
    global data
    clear()
    with open ('example.JSON') as example:
        data = json.load(example)
    draw_data()

def load2_example():
    global data
    clear()
    with open ('example2.JSON') as example:
        data = json.load(example)
    draw_data()



#GUI buttons

#Frames
#Create
button_frame = Frame(window)
mode_frame = Frame(window)
mode1_frame = Frame(window)
options_frame = Frame(window)
save_load_frame = Frame(options_frame)
help_frame = Frame(window)
#Set in GUI
help_frame.pack(side = "top")
mode1_frame.pack( side = "bottom" )
save_load_frame.pack( side = "left" )
options_frame.pack( side = "bottom" )
button_frame.pack( side = "bottom")
mode_frame.pack( side = "bottom" )
#1st line Buttons - Line, Circle, Curve, Clear, Line Colour
#Create
line_button = Button(button_frame, text="Line", width=16, command=set_line, activebackground = "#e3c3d7")
circle_button = Button(button_frame, text="Circle", width=16, command=set_circle, activebackground = "#e3c3d7")
curve_button = Button(button_frame, text="Curve", width=16, command=set_curve, activebackground = "#e3c3d7")
clear_button = Button(button_frame, text="Clear Art", width=16, command=clear_data, activebackground = "#e3c3d7")
line_color_sett = Button(button_frame, text="Line Color", width=16, command=set_line_colour, activebackground = "#e3c3d7")
line_color_label = Label(button_frame, text = line_color_text.get())
#Set in GUI
line_button.pack( side = "left" )
circle_button.pack( side = "left" )
curve_button.pack( side = "left" )
clear_button.pack( side = "left" )
line_color_sett.pack( side = "left" )
line_color_label.pack( side = "left" )

#Mode Label
mode_label = Label(mode_frame, text= "Drawing Mode : " + mode, bg=line_color_text.get())
mode_label.pack()

#2D Transformation Buttons
#Create
trans_button = Button(mode1_frame, text="Translation", width=16, command=set_trans, activebackground = "#e3c3d7")
scaleb_button = Button(mode1_frame, text="Scaling big", width=16, command=set_scale_big, activebackground = "#e3c3d7")
scales_button = Button(mode1_frame, text="Scaling small", width=16, command=set_scale_small, activebackground = "#e3c3d7")
mirror_button = Button(mode1_frame, text="Mirror", width=16, command=set_mirror, activebackground = "#e3c3d7")
rotate_button = Button(mode1_frame, text="Rotate", width=16, command=set_rotate, activebackground = "#e3c3d7")


#Set in GUI
trans_button.pack( side = "left" )
scaleb_button.pack( side = "left" )
scales_button.pack( side = "left" )
mirror_button.pack( side = "left" )
rotate_button.pack( side = "left" )

#Options Buttons
#Create
bg_color_sett = Button(options_frame, text="Background Color", width=16, command=set_bg_colour, activebackground = "#e3c3d7")
save_button = Button(save_load_frame, text="Save to JSON file", width=16, command=save_file, activebackground = "#e3c3d7")
load_button = Button(save_load_frame, text="Load example image", width=16, command=load_example, activebackground = "#e3c3d7" )
load2_button = Button(save_load_frame, text="Load example2 image", width=16, command=load2_example, activebackground = "#e3c3d7" )
curve_n_label = Label(options_frame, text= "Curve Flow")
curve_n = Scale(options_frame, from_=4, to=75, orient="horizontal")
curve_guide_label = Label(options_frame, text = "show curve guide?")
curve_guide_check = Checkbutton(options_frame, variable=curve_guide)
circle_guide_label = Label(options_frame, text = "show circles on click?")
circle_guide_check = Checkbutton(options_frame, variable=click_circle)
curve_n.set(50)
axis_label = Label(options_frame, text = "mirror axis")
x_radio = Radiobutton(options_frame, text="X", variable=mirror_axis, value='x')
y_radio = Radiobutton(options_frame, text="Y", variable=mirror_axis, value='y')
xy_radio = Radiobutton(options_frame, text="XY", variable=mirror_axis, value='xy')

#Set in GUI
load_button.pack( side = "top" )
load2_button.pack( side = "top" )
save_button.pack( side = "bottom" )
bg_color_sett.pack( side = "left" )
curve_n_label.pack(side = "left" )
curve_n.pack( side = "left" )
curve_guide_label.pack( side = "left" )
curve_guide_check.pack(side = "left")
circle_guide_label.pack( side = "left" )
circle_guide_check.pack(side = "left")
xy_radio.pack(side = "bottom")
y_radio.pack(side = "bottom")
x_radio.pack(side = "bottom")
axis_label.pack(side = "bottom")

#Help Text
help_text = Label(help_frame, text="Click on 2 points on the screen to make a line")
help_text.pack()



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



#########################################################################################


def my_scaling_point(sca_point,Sx,Sy):
    scaleMetrix = [[Sx,0,0],
                [0,Sy,0],
                [0,0,1]]
    mulMetrix = np.dot([sca_point[0],sca_point[1],1],scaleMetrix)
    return mulMetrix

def my_scaling_zoom(start, finish):
    clear()
    n = 0.1 #used to normalize scale
    x = abs(finish[0] - start[0])
    y = abs(finish[1] - start[1])
    global data
    for i in data['lines']:
        i = i['point']
        result = my_scaling_point([i[0][0], i[0][1]], x, y)
        i[0][0] = int(np.floor(np.multiply(result[0],n)))
        i[0][1] = int(np.floor(np.multiply(result[1],n)))
        result = my_scaling_point([i[1][0], i[1][1]], x, y)
        i[1][0] = int(np.floor(np.multiply(result[0],n)))
        i[1][1] = int(np.floor(np.multiply(result[1],n)))
    for i in data['circles']:
        i = i['point']
        result = my_scaling_point([i[0][0], i[0][1]], x, y)
        i[0][0] = int(np.floor(np.multiply(result[0],n)))
        i[0][1] = int(np.floor(np.multiply(result[1],n)))
        result = my_scaling_point([i[1][0], i[1][1]], x, y)
        i[1][0] = int(np.floor(np.multiply(result[0],n)))
        i[1][1] = int(np.floor(np.multiply(result[1],n)))
    for i in data['curves']:
        i = i['point']
        result = my_scaling_point([i[0][0], i[0][1]], x, y)
        i[0][0] = int(np.floor(np.multiply(result[0],n)))
        i[0][1] = int(np.floor(np.multiply(result[1],n)))
        result = my_scaling_point([i[1][0], i[1][1]], x, y)
        i[1][0] = int(np.floor(np.multiply(result[0],n)))
        i[1][1] = int(np.floor(np.multiply(result[1],n)))
        result = my_scaling_point([i[2][0], i[2][1]], x, y)
        i[2][0] = int(np.floor(np.multiply(result[0],n)))
        i[2][1] = int(np.floor(np.multiply(result[1],n)))
        result = my_scaling_point([i[3][0], i[3][1]], x, y)
        i[3][0] = int(np.floor(np.multiply(result[0],n)))
        i[3][1] = int(np.floor(np.multiply(result[1],n)))
    draw_data()

def my_scaling_small(start, finish):
    clear()
    n = 0.1 #used to normalize scale
    x = abs(finish[0] - start[0])*n
    y = abs(finish[1] - start[1])*n
    if (not x or not y):
        print("woopsers")
        return
    x = 1/x
    y = 1/y
    global data
    for i in data['lines']:
        i = i['point']
        result = my_scaling_point([i[0][0], i[0][1]], x, y)
        i[0][0] = int(np.floor(np.multiply(result[0],1)))
        i[0][1] = int(np.floor(np.multiply(result[1],1)))
        result = my_scaling_point([i[1][0], i[1][1]], x, y)
        i[1][0] = int(np.floor(np.multiply(result[0],1)))
        i[1][1] = int(np.floor(np.multiply(result[1],1)))
    for i in data['circles']:
        i = i['point']
        result = my_scaling_point([i[0][0], i[0][1]], x, y)
        i[0][0] = int(np.floor(np.multiply(result[0],1)))
        i[0][1] = int(np.floor(np.multiply(result[1],1)))
        result = my_scaling_point([i[1][0], i[1][1]], x, y)
        i[1][0] = int(np.floor(np.multiply(result[0],1)))
        i[1][1] = int(np.floor(np.multiply(result[1],1)))
    for i in data['curves']:
        i = i['point']
        result = my_scaling_point([i[0][0], i[0][1]], x, y)
        i[0][0] = int(np.floor(np.multiply(result[0],1)))
        i[0][1] = int(np.floor(np.multiply(result[1],1)))
        result = my_scaling_point([i[1][0], i[1][1]], x, y)
        i[1][0] = int(np.floor(np.multiply(result[0],1)))
        i[1][1] = int(np.floor(np.multiply(result[1],1)))
        result = my_scaling_point([i[2][0], i[2][1]], x, y)
        i[2][0] = int(np.floor(np.multiply(result[0],1)))
        i[2][1] = int(np.floor(np.multiply(result[1],1)))
        result = my_scaling_point([i[3][0], i[3][1]], x, y)
        i[3][0] = int(np.floor(np.multiply(result[0],1)))
        i[3][1] = int(np.floor(np.multiply(result[1],1)))
    draw_data()


def my_translation_point(tra_point,Tx,Ty):
    translationMetrix = [[1,0,0],
                        [0,1,0],
                        [Tx,Ty,1]]
    muMetrix = np.dot([tra_point[0],tra_point[1],1],translationMetrix)
    return muMetrix

def my_translation(start, finish):
    clear()
    x = finish[0] - start[0]
    y = finish[1] - start[1]
    global data
    for i in data['lines']:
        i = i['point']
        result = my_translation_point([i[0][0], i[0][1]], x, y)
        i[0][0] = result[0]
        i[0][1] = result[1]
        result =  my_translation_point([i[1][0], i[1][1]], x, y)
        i[1][0] = result[0]
        i[1][1] = result[1]
    for i in data['circles']:
        i = i['point']
        result = my_translation_point([i[0][0], i[0][1]], x, y)
        i[0][0] = result[0]
        i[0][1] = result[1]
        result =  my_translation_point([i[1][0], i[1][1]], x, y)
        i[1][0] = result[0]
        i[1][1] = result[1]
    for i in data['curves']:
        i = i['point']
        result = my_translation_point([i[0][0], i[0][1]], x, y)
        i[0][0] = result[0]
        i[0][1] = result[1]
        result =  my_translation_point([i[1][0], i[1][1]], x, y)
        i[1][0] = result[0]
        i[1][1] = result[1]
        result = my_translation_point([i[2][0], i[2][1]], x, y)
        i[2][0] = result[0]
        i[2][1] = result[1]
        result =  my_translation_point([i[3][0], i[3][1]], x, y)
        i[3][0] = result[0]
        i[3][1] = result[1]
    draw_data()

def my_mirror_point(mir_point,axis):
    mirrorXMetrix = [[1,0,0],
                    [0,-1,0],
                    [0,0,1]]
    mirrorYMetrix = [[-1,0,0],
                    [0,1,0],
                    [0,0,1]]
    mirrorXYMetrix = [[-1,0,0],
                    [0,-1,0],
                    [0,0,1]]
    if (axis == 'y'):
        mulMetrix = np.dot([mir_point[0],mir_point[1],1],mirrorYMetrix)
    elif(axis == 'x'):
        mulMetrix = np.dot([mir_point[0],mir_point[1],1],mirrorXMetrix)
    else:
        mulMetrix = np.dot([mir_point[0],mir_point[1],1],mirrorXYMetrix)
    return mulMetrix


def my_mirror():
    clear()
    global data
    axis = mirror_axis.get()
    #normal to re-center image
    if axis == 'x':
        nx = 0
        ny = height
    elif axis == 'y':
        nx = width
        ny = 0
    else:
        nx = width
        ny = height

    for i in data['lines']:
        i = i['point']
        result = my_mirror_point([i[0][0], i[0][1]], axis)
        i[0][0] = result[0] + nx
        i[0][1] = result[1] + ny
        result =  my_mirror_point([i[1][0], i[1][1]],  axis)
        i[1][0] = result[0] + nx
        i[1][1] = result[1] + ny
    for i in data['circles']:
        i = i['point']
        result = my_mirror_point([i[0][0], i[0][1]], axis)
        i[0][0] = result[0] + nx
        i[0][1] = result[1] + ny
        result =  my_mirror_point([i[1][0], i[1][1]], axis)
        i[1][0] = result[0] + nx
        i[1][1] = result[1] + ny
    for i in data['curves']:
        i = i['point']
        result = my_mirror_point([i[0][0], i[0][1]], axis)
        i[0][0] = result[0] + nx
        i[0][1] = result[1] + ny
        result =  my_mirror_point([i[1][0], i[1][1]], axis)
        i[1][0] = result[0] + nx
        i[1][1] = result[1] + ny
        result = my_mirror_point([i[2][0], i[2][1]], axis)
        i[2][0] = result[0] + nx
        i[2][1] = result[1] + ny
        result =  my_mirror_point([i[3][0], i[3][1]], axis)
        i[3][0] = result[0] + nx
        i[3][1] = result[1] + ny
    draw_data()

def my_rotate_point(rot_point,angle):
    rotateMetrix = [[np.cos(angle),np.sin(angle),0],
                    [(-(np.sin(angle))),np.cos(angle),0],
                    [0,0,1]]
    mulMetrix = np.dot([rot_point[0],rot_point[1],1],rotateMetrix)
    return mulMetrix

def my_rotate(points):
    clear()
    global data


    a = np.array(points[0])
    b = np.array(points[1])
    c = np.array(points[2])
    #calculate the angle
    ba = b-a
    ca = c-a

    cosine_angle = np.dot(ba , ca) / (np.linalg.norm(ba) * np.linalg.norm(ca))
    angle = np.arccos(cosine_angle)
  
    for i in data['lines']:
        i = i['point']
        result = my_rotate_point([i[0][0], i[0][1]], angle)
        i[0][0] = int(result[0])
        i[0][1] = int(result[1])
        result =  my_rotate_point([i[1][0], i[1][1]],  angle)
        i[1][0] = int(result[0])
        i[1][1] = int(result[1])
    for i in data['circles']:
        i = i['point']
        result = my_rotate_point([i[0][0], i[0][1]], angle)
        i[0][0] = int(result[0])  
        i[0][1] = int(result[1]) 
        result =  my_rotate_point([i[1][0], i[1][1]], angle)
        i[1][0] = int(result[0])  
        i[1][1] = int(result[1])  
    for i in data['curves']:
        i = i['point']
        result = my_rotate_point([i[0][0], i[0][1]], angle)
        i[0][0] = int(result[0])  
        i[0][1] = int(result[1])  
        result =  my_rotate_point([i[1][0], i[1][1]], angle)
        i[1][0] = int(result[0])  
        i[1][1] = int(result[1])  
        result = my_rotate_point([i[2][0], i[2][1]], angle)
        i[2][0] = int(result[0])  
        i[2][1] = int(result[1])  
        result =  my_rotate_point([i[3][0], i[3][1]], angle)
        i[3][0] = int(result[0])  
        i[3][1] = int(result[1])  
    draw_data()



def my_sheared_point(she_point,value,axis):
    shearedXMetrix = [[1,0,0],
                    [value,1,0],
                    [0,0,1]]
    shearedYMetrix = [[1,value,0],
                    [0,1,0],
                    [0,0,1]]
    if (axis == 'y'):
        mulMetrix = np.dot([she_point[0],she_point[1],1],shearedYMetrix)
    else:
        mulMetrix = np.dot([she_point[0],she_point[1],1],shearedXMetrix)
    return mulMetrix



#initiate drawing on screen
def draw():
        global mode
        if mode == 'line':
            my_line(points[0], points[1], line_color_text.get())
            data['lines'].append({"point": [points[0],points[1]], "color": line_color_text.get()})
        elif mode == 'circle':
            my_circle(points[0], points[1], line_color_text.get())
            data['circles'].append({"point": [points[0],points[1]],"color": line_color_text.get()})   
        elif mode == 'curve':
            my_curve(points, line_color_text.get())
            data['curves'].append({"point": [points[0],points[1], points[2], points[3]],"color": line_color_text.get()})
        elif mode == 'trans':
            my_translation(points[0], points[1])
        elif mode == 'scale big':
            my_scaling_zoom(points[0], points[1])
        elif mode == 'scale small':
            my_scaling_small(points[0], points[1])
        elif mode == 'mirror':
            my_mirror()
        # elif mode == 'shearing':

        elif mode == 'rotate':
            my_rotate(points)
        

#program main
def main():
    draw_data()
    window.mainloop()
    f.close()

if __name__ == '__main__':
    main()
