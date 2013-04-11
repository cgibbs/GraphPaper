import pygame
import os
import math

# Define colors
BLACK =   (  0,  0,  0)
WHITE =   (255,255,255)
GREY  =   (150,150,150)
BLUE  =   (  0,  0,255)
GREEN =   (  0,255,  0)
RED   =   (255,  0,  0)
BROWN =   ( 51, 25,  0)
YELLOW=   (255,255,  0)
GOLD  =   (204,204,  0)

color_names = {				
 (  0,  0,  0): "BLACK",
 (255,255,255): "WHITE",
 (150,150,150): "GREY",
 (  0,  0,255): "BLUE",
 (  0,255,  0): "GREEN",
 (255,  0,  0): "RED",
 ( 51, 25,  0): "BROWN",
 (255,255,  0): "YELLOW",
 (204,204,  0): "GOLD"}

# Define constants
FPS = 30
screen_width = 800
screen_height = 600
screen_res = (screen_width, screen_height)

# Lists for drawing
line_list = []
fill_list = []
fill_tri_list = []
fill_cir_list = []
write_list = []

def setup_screen():
    screen = pygame.display.set_mode(screen_res)
    refresh_screen(screen)
    return screen

def refresh_screen(screen):
    screen.fill(WHITE)
    draw_all_lines(screen)
    draw_all_nodes(screen)

def draw_node(screen, x,y):
    pygame.draw.rect(screen, GREY, [(x*20)-2,(y*20)-2,5,5])

def draw_all_nodes(screen):
    for j in range(1,screen_width / 20):
        for k in range(1,screen_height / 20):
            draw_node(screen, j,k)

def draw_all_lines(screen):
    bigger = 0
    if screen_width > screen_height:
        bigger = screen_width / 20
    else:
        bigger = screen_height / 20
    for i in range(0, bigger):
        pygame.draw.line(screen, GREY, (i*20,0),(i*20,screen_height), 1)
        pygame.draw.line(screen, GREY, (0,i*20),(screen_width,i*20), 1)

def get_pos(pos):
    pos2 = [0,0]
    if (pos[0]%20) < 5:
        pos2[0] = pos[0] - pos[0]%20
    elif (pos[0]%20) < 10:
        pos2[0] = pos[0] - pos[0]%10 + 10
    elif (pos[0]%20) < 15:
        pos2[0] = pos[0] - pos[0]%10
    else:
        pos2[0] = pos[0] - pos[0]%20 + 20 
    if (pos[1]%20) < 5:
        pos2[1] = pos[1] - pos[1]%20
    elif (pos[1]%20) < 10:
        pos2[1] = pos[1] - pos[1]%10 + 10
    elif (pos[1]%20) < 15:
        pos2[1] = pos[1] - pos[1]%10
    else:
        pos2[1] = pos[1] - pos[1]%20 + 20
    return pos2

def main():
    pygame.init()
    screen = setup_screen()

    mode = "line"
    selected = [0,0]
    sel_tri1 = [0,0]
    sel_tri2 = [0,0]
    color = BLACK
    line_thickness = 3
    
    running = True
    while running:
        text18 = pygame.font.Font("freesansbold.ttf", 16)
        if mode == "line" or mode == "fill_cir":
            info_text = text18.render("Mode = {0}    Color = {1}    Mouse Pos = {2}    Selected = {3}".format(mode.capitalize(),
                                                        color_names[color],
                                                        pygame.mouse.get_pos(),
                                                        selected),    
                                  True, BLACK, GREY)
        elif mode == "fill_tri":
            info_text = text18.render("Mode = {0}    Color = {1}    Mouse Pos = {2}    Selected = {3}".format(mode.capitalize(),
                                                        color_names[color],
                                                        pygame.mouse.get_pos(),
                                                        [sel_tri1, sel_tri2]),    
                                  True, BLACK, GREY)
        else:
            info_text = text18.render("Mode = {0}    Color = {1}    Mouse Pos = {2}".format(mode.capitalize(),
                                                        color_names[color],
                                                        pygame.mouse.get_pos()),    
                                  True, BLACK, GREY)
        info_rect = info_text.get_rect(bottomleft = (0, screen_height))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    mode = "line"
                elif event.key == pygame.K_F2:
                    mode = "fill"
                elif event.key == pygame.K_F3:
                    mode = "fill_tri"
                elif event.key == pygame.K_F4:
                    mode = "fill_cir"
                elif event.key == pygame.K_F5:
                    mode = "write_b"
                elif event.key == pygame.K_F6:
                    mode = "write_w"
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
                elif event.key == pygame.K_DELETE:
                    refresh_screen(screen)
                    selected = [0,0]
                    sel_tri1 = [0,0]
                    sel_tri2 = [0,0]
                    global line_list, fill_list, fill_tri_list, fill_cir_list
                    line_list = []
                    fill_list = []
                    fill_tri_list = []
                    fill_cir_list = []
                elif event.key == pygame.K_BACKSPACE:
                    if mode == "line":
                        if line_list != []:
                            line_list.pop()
                    elif mode == "fill":
                        if fill_list != []:
                            fill_list.pop()
                    elif mode == "fill_tri":
                        if fill_tri_list != []:
                            fill_tri_list.pop()
                    elif mode == "fill_cir":
                        if fill_cir_list != []:
                            fill_cir_list.pop()
                    elif mode == "write_w" or mode == "write_b":
                        if write_list != []:
                            write_list.pop()
                elif event.key == pygame.K_BACKSLASH:
                    draw_all_nodes(screen)
                elif event.key == pygame.K_RETURN:
                    draw_all_lines(screen)
                elif event.key == pygame.K_ESCAPE:
                    if mode == "line" or mode == "fill_cir":
                        selected = [0,0]
                    elif mode == "fill_tri":
                        sel_tri1 = [0,0]
                        sel_tri2 = [0,0]
                
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if mode == "line" or mode == "fill_cir":
                    # Rounds mouse pos to nearest node
                    pos2 = get_pos(pos)
                    if selected == [0,0]:
                        selected[0] = pos2[0]
                        selected[1] = pos2[1]
                    elif selected == pos2:
                        pass
                    elif mode == "fill_cir":
                        if selected[0] > pos2[0]:
                            a = selected[0] - pos2[0]
                        else:
                            a = pos2[0] - selected[0]
                        if selected[1] > pos2[1]:
                            b = pos2[1] - selected[1]
                        else:
                            b = selected[1] - pos2[1]
                        rad = int(math.sqrt(math.pow(a,2) + math.pow(b,2)))
                        fill_cir_list.append([color,selected,rad])
                        selected = [0,0]
                    else:
                        line_list.append([color,selected,pos2,line_thickness])
                        selected = [0,0]
                elif mode == "fill" or mode == "write_w" or mode == "write_b":
                    pos2 = [0,0]
                    pos2[0] = pos[0] - pos[0]%20
                    pos2[1] = pos[1] - pos[1]%20
                    if mode == "fill":
                        fill_list.append([color, pos2])
                    elif mode == "write_w" or mode == "write_b":
                        key = pygame.event.wait()
                        while key.type != 2:
                            key = pygame.event.wait()
                        if len(pygame.key.name(key.__dict__['key'])) < 2:
                            msg = pygame.key.name(key.__dict__['key'])
                        print msg
                        if mode == "write_w" and msg != None:
                            write_list.append([WHITE, pos2, msg])
                        elif mode == "write_b" and msg != None:
                            write_list.append([BLACK, pos2, msg])
                        msg = None
                        key = None                        

                elif mode == "fill_tri":
                    if sel_tri1 != [0,0]:
                        if sel_tri2 != [0,0]:
                            fill_tri_list.append([color,[sel_tri1,sel_tri2,get_pos(pos)]])
                            sel_tri1 = [0,0]
                            sel_tri2 = [0,0]
                        else:
                            sel_tri2 = get_pos(pos)
                    else: sel_tri1 = get_pos(pos)

        refresh_screen(screen)

        for j in fill_cir_list:
            pygame.draw.circle(screen,j[0],j[1],j[2])
        for i in fill_tri_list:
            pygame.draw.polygon(screen,i[0],i[1])
        for k in fill_list:
            pygame.draw.rect(screen, k[0],[k[1][0]+2,k[1][1]+2,17,17])
        for m in line_list:
            pygame.draw.line(screen,m[0],m[1],m[2],m[3])
        for n in write_list:
            if n[0] == BLACK:
                write_text = text18.render("{0}".format(n[2]), True, BLACK, None)
            elif n[0] == WHITE:
                write_text = text18.render("{0}".format(n[2]), True, WHITE, None)
            write_rect = write_text.get_rect(bottomleft = (n[1][0]+4,n[1][1]+20))
            screen.blit(write_text, write_rect)
            

        pygame.draw.rect(screen, GREY, (0, info_rect.top, screen_width,
                                        screen_height))
        screen.blit(info_text, info_rect)
        pygame.display.flip()
                

if __name__ == "__main__":
    main()
    pygame.quit()
