import pygame, math

pygame.init()
pygame.font.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 128, 64
SCREEN_SCALE = 4
DISPLAY_WIDTH, DISPLAY_HEIGHT = SCREEN_WIDTH*SCREEN_SCALE, SCREEN_HEIGHT*SCREEN_SCALE
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Color Switch")
clock = pygame.time.Clock()
BLACK = (0,0,0)
WHITE = (255,255,255)
radius = 10
obstacles = []
    
def draw_pixel(x,y, color=True):
    if(color):
        pygame.draw.rect(display, BLACK, (x*SCREEN_SCALE, y*SCREEN_SCALE, SCREEN_SCALE, SCREEN_SCALE))
    else:
        pygame.draw.rect(display, WHITE, (x*SCREEN_SCALE, y*SCREEN_SCALE, SCREEN_SCALE, SCREEN_SCALE))
        
def sgn(x):
    if(x == 0):
        return 0
    return (x / math.fabs(x))
        
def draw_line(x0, y0, x1, y1, color=True):
    dX = x1-x0
    dY = y1-y0
    dErr = 0
    
    if(dX == 0):
        for y in range(int(y0), int(y1)+1):
            draw_pixel(x0,y, color)
        return
    elif(dY == 0):
        for x in range(int(x0), int(x1)+1):
            draw_pixel(x,y0, color)
        return
    else:
        dErr = dY/dX
        error = 0
        dErr = math.fabs(dY/dX)
    y = 0
    for x in range(int(x0), int(x1)):
        draw_pixel(x,y, color)
        error+=dErr
        while(error >= 0.5):
            draw_pixel(x,y, color)
            y+= sgn(dY)
            error -= 1
        
def draw_circle(cX, cY, rad, color=True):
    x,y = rad, 0
    decisionOver2 = 1 - x  # Decision criterion divided by 2 evaluated at x=r, y=0

    while(y <= x):
        draw_pixel( x + cX,  y + cY, color) #Octant 1
        draw_pixel(-x + cX,  y + cY, color) #Octant 4
        draw_pixel( y + cX,  x + cY, color) #Octant 2
        draw_pixel(-y + cX,  x + cY, color) #Octant 3
        draw_pixel( x + cX, -y + cY, color) #Octant 7
        draw_pixel(-x + cX, -y + cY, color) #Octant 5
        draw_pixel( y + cX, -x + cY, color) #Octant 8
        draw_pixel(-y + cX, -x + cY, color) #Octant 6
        y+=1
        if (decisionOver2<=0):
            decisionOver2 += 2 * y + 1   # Change in decision criterion for y -> y+1
        else:
            x-=1
            decisionOver2 += 2 * (y - x) + 1   # Change for y -> y+1, x -> x-1
        
def draw_filled_circle(cX, cY, rad, color=True):
    x, y = rad, 0
    decisionOver2 = 1 - x 
    while(y<=x):
        
        draw_line(-x+cX, y+cY, x+cX, y+cY, color)
        draw_line(-y+cX, -x+cY, y+cX, -x+cY, color)
        draw_line(-x+cX, -y+cY, x+cX, -y+cY, color)
        draw_line(-y+cX, x+cY, y+cX, x+cY, color)
        
        draw_pixel( x + cX,  y + cY, color) #Octant 1
        draw_pixel(-x + cX,  y + cY, color) #Octant 4
        draw_pixel( y + cX,  x + cY, color) #Octant 2
        draw_pixel(-y + cX,  x + cY, color) #Octant 3
        draw_pixel( x + cX, -y + cY, color) #Octant 7
        draw_pixel(-x + cX, -y + cY, color) #Octant 5
        draw_pixel( y + cX, -x + cY, color) #Octant 8
        draw_pixel(-y + cX, -x + cY, color) #Octant 6
        y+=1
        if (decisionOver2<=0):
            decisionOver2 += 2 * y + 1   # Change in decision criterion for y -> y+1
        else:
            x-=1
            decisionOver2 += 2 * (y - x) + 1   # Change for y -> y+1, x -> x-1
        
        
def draw_arc(cX, cY, rad, sAngle, eAngle, col=True):
    if(sAngle < 0):
        sAngle+=360
    if(eAngle < 0):
        eAngle+=360

    if(sAngle > 360):
        sAngle-=360
    if(eAngle > 360):
        eAngle-=360

    #Standard Midpoint Circle algorithm
    p = int((5 - rad * 4) / 4)
    x = 0
    y = rad
    draw_circle_points(cX, cY, x, y, sAngle, eAngle, col);
    while(x <= y):
        x+=1
        if (p < 0):
            p += 2 * x + 1;
        else:
            y-=1
            p += 2 * (x - y) + 1
        draw_circle_points(cX, cY, x, y, sAngle, eAngle, col)
        
def draw_circle_points(cX, cY, x, y, sAngle, eAngle, col=True):

    #Calculate the angle the current point makes with the circle center
    angle = int(math.degrees(math.atan2(y, x)))
    #draw the circle points as long as they lie in the range specified
    if (x < y):
        #draw point in range 0 to 45 degrees
        if ((90 - angle >= sAngle or sAngle > eAngle) and 90 - angle <= eAngle):
            draw_pixel(cX - y, cY - x, col)

        #draw point in range 45 to 90 degrees
        if ((angle >= sAngle or sAngle > eAngle) and angle <= eAngle):
            draw_pixel(cX - x, cY - y, col)

        #draw point in range 90 to 135 degrees
        if (180 - angle >= sAngle and 180 - angle <= eAngle):
            draw_pixel(cX + x, cY - y, col)

        #draw point in range 135 to 180 degrees
        if (angle + 90 >= sAngle and angle + 90 <= eAngle):
            draw_pixel(cX + y, cY - x, col)

        #draw point in range 180 to 225 degrees
        if (270 - angle >= sAngle and 270 - angle <= eAngle):
            draw_pixel(cX + y, cY + x, col)
                
        #draw point in range 225 to 270 degrees
        if (angle + 180 >= sAngle and angle + 180 <= eAngle):
            draw_pixel(cX + x, cY + y, col)

        #draw point in range 270 to 315 degrees
        if (360 - angle >= sAngle and (360 - angle <= eAngle or sAngle > eAngle)):
            draw_pixel(cX - x, cY + y, col)

        #draw point in range 315 to 360 degrees
        if (angle + 270 >= sAngle and (angle + 270 <= eAngle or sAngle > eAngle) ):
            draw_pixel(cX - y, cY + x, col)
    
x = int(SCREEN_WIDTH*(1/4))
y = int(SCREEN_HEIGHT/2)
vel = 0
radius = 3
cam_x, cam_y = 0,0

def draw_letter(letter, x, y,col=True):
    if(letter == "A"):
        draw_pixel(x+1, y, col)
        draw_pixel(x+2, y, col)
        draw_pixel(x, y+1, col)
        draw_pixel(x, y+2, col)
        draw_pixel(x, y+3, col)
        draw_pixel(x, y+4, col)
        draw_pixel(x+3, y+1, col)
        draw_pixel(x+3, y+2, col)
        draw_pixel(x+3, y+3, col)
        draw_pixel(x+3, y+4, col)
        draw_pixel(x+1, y+2, col)
        draw_pixel(x+2, y+2, col)
        draw_pixel(x+3, y+2, col)
    elif(letter == "B"):
        draw_pixel(x,y,col)
        draw_pixel(x+1,y,col)
        draw_pixel(x+2,y,col)
        draw_pixel(x,y+1,col)
        draw_pixel(x+3,y+1,col)
        draw_pixel(x,y+2,col)
        draw_pixel(x+1,y+2,col)
        draw_pixel(x+2,y+2,col)
        draw_pixel(x,y+3,col)
        draw_pixel(x+3,y+3,col)
        draw_pixel(x,y+4,col)
        draw_pixel(x+1,y+4,col)
        draw_pixel(x+2,y+4,col)

def ball_jump():
    global x,y,vel
    vel = 4
    
def ball_draw():
    draw_filled_circle(int(x-cam_x), int(y), radius, False)
    
def ball_update():
    global x,y,vel,cam_x,cam_y
    x+=vel
    if(cam_x <= x-SCREEN_WIDTH*0.4):
        cam_x = x-SCREEN_WIDTH*0.4
    vel-=0.5
    collision_detection()
    
def collision_detection():
    pass
    
def handle_events():
    global radius
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                return False
            elif(e.key == pygame.K_LEFT):
                radius-=1
            elif(e.key == pygame.K_RIGHT):
                radius+=1
            if(e.key == pygame.K_SPACE):
                ball_jump()
        if(e.type == pygame.QUIT):
            return False
    return True

angle = 0

def draw_star_outline(x,y,col=True):
    draw_pixel(x+4,y-1,col)
    draw_pixel(x+4,y+1,col)
    draw_pixel(x+5,y-1,col)
    draw_pixel(x+5,y+1,col)
    
    draw_pixel(x+6,y,col)
    
    draw_pixel(x+3, y-2,col)
    draw_pixel(x+3,y+2,col)
    
    draw_line(x+2,y-6,x+2,y-3,col)
    draw_line(x+2,y+3,x+2,y+6,col)
    draw_pixel(x+2,y-6,col)
    draw_pixel(x+2,y+6,col)
    
    draw_pixel(x+1,y-6,col)
    draw_pixel(x+1,y+6,col)
    
    draw_pixel(x,y-5,col)
    draw_pixel(x,y+5,col)
    
    draw_pixel(x-1,y-4,col)
    draw_pixel(x-1,y+4,col)
    
    draw_pixel(x-2,y-3,col)
    draw_pixel(x-2,y+3,col)
    
    draw_pixel(x-3,y-4,col)
    draw_pixel(x-3,y+4,col)
    
    draw_pixel(x-4,y-4,col)
    draw_pixel(x-4,y+4,col)
    draw_pixel(x-4,y,col)
    
    draw_pixel(x-5,y-4,col)
    draw_pixel(x-5,y-1,col)
    draw_pixel(x-5,y-2,col)
    
    draw_pixel(x-5,y+1,col)
    draw_pixel(x-5,y+4,col)
    draw_pixel(x-5,y+2,col)
    
    draw_pixel(x-6,y+3,col)
    draw_pixel(x-6,y+4,col)
    draw_pixel(x-6,y-3,col)
    draw_pixel(x-6,y-4,col)

def draw_star(x,y,col=True):
    draw_pixel(x,y,col)
    draw_pixel(x+1,y+1,col)
    draw_pixel(x-1,y-1,col)
    draw_pixel(x+1,y,col)
    draw_pixel(x-1,y,col)
    draw_pixel(x+1,y-1,col)
    draw_pixel(x-1,y+1,col)
    draw_pixel(x,y+1,col)
    draw_pixel(x,y-1,col)
    
    for i in range(2,6):
        draw_pixel(x+i,y,col)
        draw_pixel(x+i,y-1,col)
        draw_pixel(x+i,y+1,col)
    draw_pixel(x+6,y,col)
    
    draw_pixel(x+3, y-2,col)
    draw_pixel(x+3,y+2,col)
    
    draw_line(x+2,y-6,x+2,y+6,col)
    draw_pixel(x+2,y-6,col)
    draw_pixel(x+2,y+6,col)
    
    draw_line(x+1,y-6,x+1,y+6,col)
    draw_line(x,y-5,x,y+5,col)
    draw_line(x-1,y-4,x-1,y+4,col)
    draw_line(x-2,y-3,x-2,y+3,col)
    draw_line(x-3,y-4,x-3,y+4,col)
    draw_line(x-4,y-4,x-4,y+4,col)
    draw_line(x-5,y-4,x-5,y-1,col)
    draw_line(x-5,y+1,x-5,y+4,col)
    draw_pixel(x-5,y+1,col)
    draw_pixel(x-5,y+4,col)
    draw_pixel(x-6,y+3,col)
    draw_pixel(x-6,y+4,col)
    draw_pixel(x-6,y-3,col)
    draw_pixel(x-6,y-4,col)

def spawn_obstacles():
    for i in range(1, 20):
        obstacles.append((i*SCREEN_WIDTH, SCREEN_HEIGHT/2))

def draw_obstacle(x,y):
    global angle
    draw_circle(x-cam_x, y,radius+16, False)
    draw_circle(x-cam_x, y,radius+22, False)
    draw_star(x-cam_x, y, False)
    i = 16
    while(i <= 21):
        i+=1
        draw_arc(x-cam_x, y,radius+i,angle,angle+90, False)
    
spawn_obstacles()

while(handle_events()):
    clock.tick(30)
    display.fill(BLACK)
    
    ball_update()
    if(angle < 360):
        angle+=2
    else:
        angle-=360
    
    for obstacle in obstacles:
        if(obstacle[0]-cam_x <= 500):
            draw_obstacle(obstacle[0],obstacle[1])
    
    ball_draw()

    pygame.display.flip()

pygame.quit()
