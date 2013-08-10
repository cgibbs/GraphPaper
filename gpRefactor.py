import pygame
import os
import math
from constants import *

# -----Lists for drawing-----

line_list = []
fill_list = []
triangle_list = []
circle_list = []
write_list = []
temp = []

# -----Some globally-relevant stuff-----

mode = "line"
debug = True
color = BLACK
line_thickness = 3

# -----Boring stuff (screen methods)-----

def create_screen():
    screen = pygame.display.set_mode(screen_res)
    refresh_screen(screen)
    return screen

def refresh_screen(screen):
    screen.fill(WHITE)
    draw_all_lines(screen)
    draw_all_nodes(screen)

def draw_node(screen,x,y):
    pygame.draw.rect(screen, GREY, [(x*tile_size)-2,(y*tile_size)-2,5,5])

def draw_all_lines(screen):
    bigger = 0
    if screen_width > screen_height:
        bigger = screen_width / tile_size
    else:
        bigger = screen_height / tile_size
    for i in range(0, bigger):
        pygame.draw.line(screen, GREY, (i*tile_size,0),(i*tile_size,
                                                        screen_height),1)
        pygame.draw.line(screen, GREY, (0,i*tile_size),(screen_width,
                                                        i*tile_size),1)

def draw_all_nodes(screen):
    for j in range(1,screen_width / tile_size):
        for k in range(1,screen_height / tile_size):
            draw_node(screen, j,k)

def draw_bot_text(screen, tf):
    bot_text = "Mode = {0}    Color = {1}    Mouse Pos = {2}"
    info_text = tf.render(bot_text.format(mode.capitalize(),color_names[color],
                                          pygame.mouse.get_pos()),
                              True,BLACK,GREY)
    info_rect = info_text.get_rect(bottomleft = (0, screen_height))
    pygame.draw.rect(screen, GREY, (0, info_rect.top, screen_width,
                                    screen_height))
    screen.blit(info_text, info_rect)

def draw_selected(screen,tf,sel):
    draw_selected_node(screen,sel)
    draw_selected_text(screen,tf,sel)
    pygame.display.flip()

def draw_selected_node(screen,sel):
    try:
        pygame.draw.rect(screen,HPINK,[sel[0]-2,sel[1]-2,5,5])
    except TypeError:
        for i in sel:
            pygame.draw.rect(screen,HPINK,[i[0]-2,i[1]-2,5,5])

def draw_selected_text(screen,tf,sel):
    info_text = tf.render("Selected = {0}".format(sel),True,BLACK,GREY)
    info_rect = info_text.get_rect(bottomleft = (500, screen_height))
    pygame.draw.rect(screen, GREY, (500, info_rect.top, (screen_width-500),
                                    screen_height))
    screen.blit(info_text, info_rect)

def draw_shapes(screen):
    for j in circle_list:
        pygame.draw.circle(screen,j[0],j[1],j[2])
    for i in triangle_list:
        pygame.draw.polygon(screen,i[0],i[1])
    for k in fill_list:
        pygame.draw.rect(screen, k[0],[k[1][0]+2,k[1][1]+2,tile_size-3,
                                       tile_size-3])
    for m in line_list:
        pygame.draw.line(screen,m[0],m[1],m[2],m[3])
    for n in temp:
        pygame.draw.rect(screen, GREY, [(n[0]*tile_size)-2,(n[1]*tile_size)-2,
                                        5,5])
        
def draw_letters(screen, tf):
    for i in write_list:
        write_text = tf.render("{0}".format(n[2]), True, n[0])
        write_rect = write_text.get_rect(bottomleft = (n[1][0]+4,n[1][1]+20))
        screen.blit(write_text, write_rect)

# -----Get positions in various ways -----

def get_pos():
    pos = pygame.mouse.get_pos()
    pos2 = [0,0]
    if (pos[0]%tile_size) < tile_size/4:
        pos2[0] = pos[0] - pos[0]%tile_size
    elif (pos[0]%tile_size) < tile_size/2:
        pos2[0] = pos[0] - pos[0]%(tile_size/2) + tile_size/2
    elif (pos[0]%tile_size) < tile_size*3/4:
        pos2[0] = pos[0] - pos[0]%(tile_size/2)
    else:
        pos2[0] = pos[0] - pos[0]%tile_size + tile_size 
    if (pos[1]%tile_size) < tile_size/4:
        pos2[1] = pos[1] - pos[1]%tile_size
    elif (pos[1]%tile_size) < tile_size/2:
        pos2[1] = pos[1] - pos[1]%(tile_size/2) + tile_size/2
    elif (pos[1]%tile_size) < tile_size*3/4:
        pos2[1] = pos[1] - pos[1]%(tile_size/2)
    else:
        pos2[1] = pos[1] - pos[1]%tile_size + tile_size
    return pos2

def get_fill_pos(pos):
    pos2 = [0,0]
    pos2[0] = pos[0] - pos[0]%tile_size
    pos2[1] = pos[1] - pos[1]%tile_size
    return pos2

def get_wait_pos():
    while True:
        e = pygame.event.wait()
        if e.type == pygame.MOUSEBUTTONUP:
            return get_pos()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                print "break"
                return None

# -----Draw list appends-----

def circle(screen,tf):
    p1 = get_pos()
    draw_selected(screen,tf,p1)
    p2 = get_wait_pos()
    if not p2:
        return
    if p1[0] > p2[0]:
        a = p1[0] - p2[0]
    else:
        a = p2[0] - p1[0]
    if p1[1] > p2[1]:
        b = p2[1] - p1[1]
    else:
        b = p1[1] - p2[1]
    rad = int(math.sqrt(math.pow(a,2) + math.pow(b,2)))
    circle_list.append([color,p1,rad])

def fill():
    fill_list.append([color,get_fill_pos(get_pos())])

def line(screen,tf):
    p1 = get_pos()
    draw_selected(screen,tf,p1)
    p2 = get_wait_pos()
    if not p2:
        return
    line_list.append([color,p1,p2,line_thickness])

def triangle(screen,tf):
    p1 = get_pos()
    draw_selected(screen,tf,p1)
    p2 = get_wait_pos()
    if not p2:
        return
    draw_selected(screen,tf,[p1,p2])
    p3 = get_wait_pos()
    if not p3:
        return
    triangle_list.append([color,[p1,p2,p3]])

def write():
    p1 = get_fill_pos(get_pos())
    e = pygame.event.wait()
    while e.type != pygame.KEYDOWN:
        e = pygame.event.wait()
    if len(pygame.key.name(e.dict['key'])) < 2:
        msg = pygame.key.name(e.dict['key'])
        write_list.append([color, p1, msg])

# -----The Annihilator-----

def clear_lists():
    global line_list, fill_list, triangle_list, circle_list, write_list         
    line_list = []
    fill_list = []
    triangle_list = []
    circle_list = []
    write_list = []

#
#
# -----Main-----
#
#

def main():
    pygame.init()
    screen = create_screen()

    global color, line_thickness, mode, temp
    text16 = pygame.font.Font("freesansbold.ttf", 16)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # mode changes (insert music theory joke here)
                if event.key == pygame.K_F1:
                    mode = "line"
                elif event.key == pygame.K_F2:
                    mode = "fill"
                elif event.key == pygame.K_F3:
                    mode = "triangle"
                elif event.key == pygame.K_F4:
                    mode = "circle"
                elif event.key == pygame.K_F5:
                    mode = "write"

                # color changes
                elif event.key == pygame.K_r:
                    color = RED
                elif event.key == pygame.K_a:
                    color = BLACK
                elif event.key == pygame.K_b:
                    color = BLUE
                elif event.key == pygame.K_e:
                    color = GREY
                elif event.key == pygame.K_g:
                    color = GREEN
                elif event.key == pygame.K_w:
                    color = WHITE
                elif event.key == pygame.K_d:
                    color = GOLD
                elif event.key == pygame.K_y:
                    color = YELLOW
                elif event.key == pygame.K_o:
                    color = BROWN
                elif event.key == pygame.K_1:
                    line_thickness = 1
                elif event.key == pygame.K_2:
                    line_thickness = 3
                elif event.key == pygame.K_3:
                    line_thickness = 5

                # deletions
                elif event.key == pygame.K_DELETE:
                    refresh_screen(screen)
                    clear_lists()
                elif event.key == pygame.K_BACKSPACE:
                    if mode == "line":
                        if line_list != []:
                            line_list.pop()
                    elif mode == "fill":
                        if fill_list != []:
                            fill_list.pop()
                    elif mode == "triangle":
                        if triangle_list != []:
                            triangle_list.pop()
                    elif mode == "circle":
                        if circle_list != []:
                            circle_list.pop()
                    elif mode == "write":
                        if write_list != []:
                            write_list.pop()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if mode == "circle":
                    circle(screen,text16)
                elif mode == "fill":
                    fill()
                elif mode == "line":
                    line(screen,text16)
                elif mode == "triangle":
                    triangle(screen,text16)
                elif mode == "write":
                    write()
                    
        refresh_screen(screen)
        draw_shapes(screen)
        draw_letters(screen,text16)
        draw_bot_text(screen,text16)
        temp = []
        pygame.display.flip()
                

# -----Run-----

if __name__ == "__main__":
    main()
    pygame.quit()
