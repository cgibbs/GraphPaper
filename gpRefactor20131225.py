import pygame
import os
import math
from constants import *
import eztext
import shelve

# -----Some globally-relevant stuff-----

mode = "line"
debug = True
color = BLACK
line_thickness = 3

pygame.init()
text16 = pygame.font.Font("freesansbold.ttf", 16)
sym_font = pygame.font.Font("dPoly 4EDings.ttf", 24)

# -----Boring stuff (screen methods)-----

def create_screen():
    screen = pygame.display.set_mode(SCREEN_RES)
    return screen

def refresh_screen(screen):
    screen.fill(WHITE)
    draw_all_lines()
    draw_all_nodes()

def draw_all_lines():
    bigger = 0
    if SCREEN_WIDTH > SCREEN_HEIGHT:
        bigger = SCREEN_WIDTH / TILE_SIZE
    else:
        bigger = SCREEN_HEIGHT / TILE_SIZE
    for i in range(0, bigger):
        pygame.draw.line(screen, GREY, (i*TILE_SIZE,0),(i*TILE_SIZE,
                                                        SCREEN_HEIGHT),1)
        pygame.draw.line(screen, GREY, (0,i*TILE_SIZE),(SCREEN_WIDTH,
                                                        i*TILE_SIZE),1)

def draw_all_nodes():
    for j in range(1,SCREEN_WIDTH / TILE_SIZE):
        for k in range(1,SCREEN_HEIGHT / TILE_SIZE):
            draw_node(j,k)

def draw_node(x,y):
    pygame.draw.rect(screen, GREY, [(x*TILE_SIZE)-2,(y*TILE_SIZE)-2,5,5])

def draw_bot_text():
    bot_text = "Mode = {0}    Color = {1}    Mouse Pos = {2}"
    info_text = text16.render(bot_text.format(mode.capitalize(),color_names[color],
                                          pygame.mouse.get_pos()),
                            True,BLACK,GREY)
    info_rect = info_text.get_rect(bottomleft = (0, SCREEN_HEIGHT))
    pygame.draw.rect(screen, GREY, (0, info_rect.top, SCREEN_WIDTH,
                                    SCREEN_HEIGHT))
    screen.blit(info_text, info_rect)

def draw_selected(sel):
    draw_selected_node(sel)
    draw_selected_text(sel)
    pygame.display.flip()

def draw_selected_node(sel):
    try:
        pygame.draw.rect(screen,HPINK,[sel[0]-2,sel[1]-2,5,5])
    except TypeError:
        for i in sel:
            pygame.draw.rect(screen,HPINK,[i[0]-2,i[1]-2,5,5])

def draw_selected_text(sel):
    info_text = text16.render("Selected = {0}".format(sel),True,BLACK,GREY)
    info_rect = info_text.get_rect(bottomleft = (500, SCREEN_HEIGHT))
    pygame.draw.rect(screen, GREY, (500, info_rect.top, (SCREEN_WIDTH-500),
                                    SCREEN_HEIGHT))
    screen.blit(info_text, info_rect)

def draw_shapes(screen):
    global line_list, fill_list, triangle_list, circle_list
    for j in circle_list:
        pygame.draw.circle(screen,j[0],j[1],j[2])
    for i in triangle_list:
        pygame.draw.polygon(screen,i[0],i[1])
    for k in fill_list:
        pygame.draw.rect(screen, k[0],[k[1][0]+2,k[1][1]+2,TILE_SIZE-3,
                                       TILE_SIZE-3])
    for m in line_list:
        pygame.draw.line(screen,m[0],m[1],m[2],m[3])
        
def draw_letters():
    global write_list, symbol_list
    for i in write_list:
        write_text = text16.render("{0}".format(i[2]), True, i[0])
        write_rect = write_text.get_rect(bottomleft = (i[1][0]+4,i[1][1]+20))
        screen.blit(write_text, write_rect)
    for i in symbol_list:
        write_text = sym_font.render("{0}".format(i[2]), True, i[0])
        write_rect = write_text.get_rect(bottomleft = (i[1][0],i[1][1]+20))
        screen.blit(write_text, write_rect)

def draw_symbol_menu():
    (mx, my) = get_fill_pos()
    pygame.draw.rect(screen, GREY, ((680, 60), (799, 300)))
    write_text = text16.render("Symbols:", True, BLACK)
    write_rect = write_text.get_rect(bottomleft = (700,100))
    screen.blit(write_text, write_rect)
    x = 35
    y = 5
    for s in "abcdefhijklmopqrstuxyz345":
        write_text = sym_font.render(s, True, BLACK)
        write_rect = write_text.get_rect(bottomleft = (x * 20, (y + 1) * 20))
        screen.blit(write_text, write_rect)
        x += 1
        if x > 38:
            x = 35
            y += 1

    pygame.display.flip()

    looping = True
    while looping:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                looping = False
                break
        if event.type == pygame.MOUSEBUTTONUP:
            # this part just saves me some headache of mapping individual keys,
            # at the slight (negligible, even) cost of time
            (j, k) = get_fill_pos()
            j = j / TILE_SIZE
            k = k / TILE_SIZE
            x = 35
            y = 5
            for s in "abcdefhijklmopqrstuxyz345":
                if j == x and k == y:
                    symbol_list.append((color, (mx, my), s))
                    looping = False
                    break
                else:
                    x += 1
                    if x > 38:
                        x = 35
                        y += 1
        

# -----Get positions in various ways -----

def get_pos():
    x, y = pygame.mouse.get_pos()
    x = int(round_to_nearest(x, TILE_SIZE/2.0))
    y = int(round_to_nearest(y, TILE_SIZE/2.0))
    return (x,y)

def get_fill_pos():
    x, y = pygame.mouse.get_pos()
    x = int(round_to_nearest(x, TILE_SIZE))
    y = int(round_to_nearest(y, TILE_SIZE))
    return (x,y)

def get_wait_pos():
    while True:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            return None
        elif e.type == pygame.MOUSEBUTTONUP:
            return get_pos()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return None

def round_to_nearest(number, to):
    return round(number / to, 0) * to

# -----Draw list appends-----

def circle():
    p1 = get_pos()
    draw_selected(p1)
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
    fill_list.append([color,get_fill_pos()])

def line():
    p1 = get_pos()
    draw_selected(p1)
    p2 = get_wait_pos()
    if not p2:
        return
    line_list.append([color,p1,p2,line_thickness])

def triangle():
    p1 = get_pos()
    draw_selected(p1)
    p2 = get_wait_pos()
    if not p2:
        return
    draw_selected([p1,p2])
    p3 = get_wait_pos()
    if not p3:
        return
    triangle_list.append([color,[p1,p2,p3]])

def write():
    p1 = get_fill_pos()
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

# -----Lists for drawing-----

line_list = []
fill_list = []
triangle_list = []
circle_list = []
write_list = []
symbol_list = []

# -----Key dictionaries-----

key_to_mode = {
    pygame.K_F1: "line",
    pygame.K_F2: "fill",
    pygame.K_F3: "triangle",
    pygame.K_F4: "circle",
    pygame.K_F5: "write",
    pygame.K_F6: "symbol"
}

key_to_color = {
    pygame.K_r: RED,
    pygame.K_a: BLACK,
    pygame.K_b: BLUE,
    pygame.K_e: GREY,
    pygame.K_g: GREEN,
    pygame.K_w: WHITE,
    pygame.K_d: GOLD,
    pygame.K_y: YELLOW,
    pygame.K_o: BROWN
}

key_to_line_thickness = {
    pygame.K_1: 1,
    pygame.K_2: 3,
    pygame.K_3: 5
}

mode_to_list = {
    "line": 'line_list',
    "fill": 'fill_list',
    "triangle": 'triangle_list',
    "circle": 'circle_list',
    "write": 'write_list',
    "symbol": 'symbol_list'
}

mode_to_method = {
    "circle": circle,
    "fill": fill,
    "line": line,
    "triangle": triangle,
    "write": write,
    "symbol": draw_symbol_menu
}

# Save/Load

def save():
    textbox = eztext.Input(maxlength=45, color=(255,0,0), prompt="Save name: ")
    looping = True
    while looping:
        pygame.draw.rect(screen, WHITE, ((0, 0), (600, 20)))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    looping = False
        val = textbox.update(events)
        textbox.draw(screen)
        pygame.display.flip()
    file = shelve.open(val, 'n')
    file['line_list'] = line_list
    file['fill_list'] = fill_list
    file['triangle_list'] = triangle_list
    file['circle_list'] = circle_list
    file['write_list'] = write_list
    file['symbol_list'] = symbol_list
    file.close()

def load():
    global line_list, fill_list, triangle_list, circle_list, write_list
    global symbol_list
    
    textbox = eztext.Input(maxlength=45, color=(255,0,0), prompt="Load name: ")
    looping = True
    while looping:
        pygame.draw.rect(screen, WHITE, ((0, 0), (600, 20)))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    looping = False
        val = textbox.update(events)
        textbox.draw(screen)
        pygame.display.flip()
    #clear_lists()
    file = shelve.open(val, 'r')
    line_list = file['line_list']
    fill_list = file['fill_list']
    triangle_list = file['triangle_list']
    circle_list = file['circle_list']
    write_list = file['write_list']
    symbol_list = file['symbol_list']
    file.close()

#
#
# -----Main-----
#
#

screen = create_screen()
refresh_screen(screen)

def main():
    global color, line_thickness, mode
    
    pygame.display.flip() 
    
    running = True
    while running:        
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in key_to_mode:
                mode = key_to_mode[event.key]

            elif event.key in key_to_color:
                color = key_to_color[event.key]

            elif event.key in key_to_line_thickness:
                line_thickness = key_to_line_thickness[event.key]

            elif event.key in key_to_color:
                color = key_to_color[event.key]

            elif event.key == pygame.K_DELETE:
                clear_lists()
                
            elif event.key == pygame.K_BACKSPACE:
                # not sure why using globals normally doesn't work...
                if globals()[mode_to_list[mode]]: 
                   globals()[mode_to_list[mode]].pop()

            elif event.key == pygame.K_HOME:
                save()

            elif event.key == pygame.K_END:
                load()
                            
        elif event.type == pygame.MOUSEBUTTONUP:
            mode_to_method[mode]()

        refresh_screen(screen)
        draw_shapes(screen)
        draw_letters()
        draw_bot_text()
        pygame.display.flip()


        

# -----Run-----

if __name__ == "__main__":
    main()
    pygame.quit()
