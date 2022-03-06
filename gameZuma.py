#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 09:40:33 2021

@author: amanda
"""

"""
Projeto 2 - Código Parcial II - Algoritmos e Estruturas de Dados

Autora: Amanda Jorge Mendes
Matrícula: 149344

O projeto proposto consiste em um jogo estilo Zuma.

Código Parcial I:
    
    Movimento das bolinhas ao longo do percurso;
    Simulação de novas bolinhas sendo inseridas na fila;
    Simulação de bolinhas sendo excluídas da fila;
    
CÓDIGO PARCIAL II:
    
    Canhão giratório de bolinhas
    Inserção de novas bolinhas no percurso dado o ângulo do canhão
    Eliminação de conjuntos de 3 ou mais bolinhas da mesma cor
    
Entrega Final:
    
    Organização do código 
    Refinamento de elementos gráficos
    Revisão e otimização da lógica do jogo
"""
from graphics import *
import time
import numpy as np
import random
import math


class PathLine:
    """
    This represents a line along which the balls will move
    """
    def __init__(self, lim_min, lim_max, theta, first=False):
        """
        lim_min = Start - (x,y)
        lim_max = End - (x,y)
        theta = Angle in radians (0 to 2pi)
        first = First line? If first, "no minimum limit"
        """
        move_min = lim_min if not first else (lim_min[0]-20000*math.cos(theta),
                                              lim_min[0]-20000*math.sin(theta))
        self.theta = theta
        self.xs = [move_min[0], lim_min[0], lim_max[0]]
        self.ys = [move_min[1], lim_min[1], lim_max[1]]
        
        """
        Define line equation
        """
        try:
            a = math.sin(self.theta)/round(math.cos(self.theta),5)
            b = self.ys[1] - a*self.xs[1]
            self.line = [a, -1, -b]
            
        except ZeroDivisionError:
            self.line = [1, 0, self.xs[1]]
            
    def move(self, x, y, steps):
        """
        Move steps from point (x,y)
        Returns:
            -Necessary displacement in x and y
            -Number of steps left
        """
        if not (min(self.xs)<= round(x) <= max(self.xs)  and min(self.ys)<= round(y) <=max(self.ys)):
            return 0,0,steps
       
        if steps > 0:
            possible = min(steps, int(((x-self.xs[2])**2 + (y-self.ys[2])**2)**0.5))      
        else:
            possible = -min(-steps, int(((x-self.xs[0])**2 + (y-self.ys[0])**2)**0.5)) 
        self.x = possible*math.cos(self.theta)
        self.y = possible*math.sin(self.theta)
        
        return self.x, self.y, steps - possible
 
    def intercept(self, point, theta):
        """
        Interception of path line with line that describes the ball movement
        -Point: ball position (x,y)
        -Theta: shooting angle
        Returns:
            - Interception - (x,y)
            - Distance from point to this line
            - None if there is no interception within line limits
            
        """
        
        """
        Define line that describes the ball movement
        """
        try:
            a1 = math.sin(theta)/round(math.cos(theta),5)
            b1 = point[1] - a1*point[0]
            line1 = [a1, -1, -b1]
            
        except ZeroDivisionError:
            line1 = [1, 0, point[0]]
        
        """
        Calculate interception
        """
        try:
            intercept = np.linalg.solve(np.array([self.line[:-1], line1[:-1]]),
                                        np.array([[self.line[-1]],[line1[-1]]]))

        except:
            return
        
        """
        Check if interception is within path line limits and if direction
        is valid (line is infinite, shooting line has a starting point)
        """
        if min(self.xs[1:]) <= intercept[0][0] <= max(self.xs[1:]) and \
            min(self.ys[1:]) <= intercept[1][0] <= max(self.ys[1:]):
                dist = np.linalg.norm(np.array(point) - intercept.reshape(1,2))
                nt = math.atan2(intercept[1][0]-point[1], intercept[0][0]-point[0])
                nt = nt+2*math.pi if nt<0 else nt
                if round(nt,2) == round(theta%(2*math.pi),2):  
                    return intercept[0][0], intercept[1][0], dist
            
                
def move(lines, ball, v=2):
    """
    Move ball along lines for v steps(pixels)
    """
    mx = my = 0
    xc, yc = (ball.getCenter().x, ball.getCenter().y)
    left = v
    vdir = 1 if v>0 else -1

    for l in lines[::vdir]:
        if not left:
            break
        x, y, l = l.move(xc+mx, yc+my, left)
        left = l
        mx+=x
        my+=y
        
    ball.move(round(mx,2), round(my,2))


""" 
Window
"""

win = GraphWin("Zuma", 650, 650, autoflush = False)
win.setCoords(0, 0, 650, 650)
background = Image(Point(325, 325), "verde1.png")
background.draw(win)

radius = 20 
colors = ["goldenrod1", "cyan4", "deeppink4"] 

"""
Levels
"""

vs = [1,1,2] 
ns_balls = [80,120,50] 
all_lines=[] 

boundaries = [PathLine((-50, 700), (700, 700),0),
              PathLine((-50, -50), (700, -50),0),
              PathLine((-50,-50), (-50, 700),math.radians(90)),
              PathLine((700, -50), (650, 650),math.radians(90))]

    
all_lines.append(boundaries+[PathLine((50, 650), (50, 50), math.radians(270), first = True),
                             PathLine((50, 50), (600, 50), math.radians(0)),
                             PathLine((600, 50), (600, 620), math.radians(90))])

all_lines.append(boundaries+[PathLine((50, 650), (50, 50), math.radians(270), first = True),
                             PathLine((50, 50), (125, 50), math.radians(0)),
                             PathLine((125, 50), (125, 500), math.radians(90)),
                             PathLine((125, 500), (525, 500), math.radians(0)),
                             PathLine((525, 500), (525, 50), math.radians(270)),
                             PathLine((525, 50), (600, 50), math.radians(0)),
                             PathLine((600, 50), (600, 620), math.radians(90))])
all_lines.append(all_lines[-1].copy())


presentation = [Image(Point(325,325), "level1.png"),
                Image(Point(325,325), "level2.png"),
                Image(Point(325,325), "level3.png")]

"""
Graphic elements
"""
backR = Rectangle(Point(0,0),Point(650,650)) 
backR.setFill("gray75")

instruc = Image(Point(325, 200), "zuma.png") 

can_x, can_y = (325, 325)
la = 1.5*radius
lb = 4*radius  
inc = 6
theta = 0

base = Circle(Point(can_x, can_y), 50)
base.setFill("gray65")
base.setOutline("gray40")
base.setWidth(3)

p1 = Point(la*math.sin(theta)+can_x, la*math.cos(theta)+can_y)
p2 = Point(la*math.sin(theta+math.pi)+can_x, la*math.cos(theta-math.pi)+can_y)
circle = Circle(Point(can_x, can_y),
                (((p1.getX() - p2.getX())**2 + (p1.getY() - p2.getY())**2)**0.5)/2 )
circle.setFill("gray30")

start_p = Image(Point(50, 618), "top5.png")
end_p = Image(Point(600, 618), "top5.png")

"""
Game
"""
change = delete = end = close = False
level = 0
while level<3:
    v = vs[level]
    lines = all_lines[level]
    n_balls = ns_balls[level]
    change = delete = end  = False
    if close:
        break
    
    """
    Display level 
    """
    backR.draw(win)
    presentation[level].draw(win)
    update(30)
    time.sleep(1)
    backR.undraw()
    presentation[level].undraw()
    
    """
    Set up graphic elements for level
        - Paths (Green rectangles)
        - Balls
        - Cannon/cannon ball/base/line     
        - Start point/end point
        - Instructions
    """
    
    """
    Paths
    """
    paths = []
    for l in lines[4:]:
        v1 = Point(l.xs[1] + radius*math.cos(l.theta - math.pi/2),
                   l.ys[1] + radius*math.sin(l.theta - math.pi/2))
        v2 = Point(l.xs[0] + radius*math.cos(l.theta + math.pi/2),
                   l.ys[1] + radius*math.sin(l.theta + math.pi/2))
        v3 = Point(l.xs[2] + radius*math.cos(l.theta - math.pi/2),
                   l.ys[2] + radius*math.sin(l.theta - math.pi/2))
        v4 = Point(l.xs[2] + radius*math.cos(l.theta + math.pi/2),
                   l.ys[2] + radius*math.sin(l.theta + math.pi/2))
        p = Polygon([v1, v2, v4, v3])
        corner = Circle(Point(l.xs[2], l.ys[2]), 20)
        corner.setWidth(0)
        corner.setFill("darkolivegreen")
        corner.draw(win)
        p.setFill("darkolivegreen")
        p.setOutline("darkolivegreen")
        p.draw(win)
        paths.append((p,corner))
    
    
    """
    Balls
    """
    
    balls = []
    previous = [None, None]
    
    for i in range(n_balls):
        if i == 0:
            prev = (lines[4].xs[1], lines[4].ys[1]) 
        else:
            c_prev = balls[-1][0].getCenter()
            prev = (c_prev.x, c_prev.y)
            
        xn, yn, _ = lines[4].move(prev[0], prev[1], -2*radius)
        ball = Circle(Point(prev[0]+xn, prev[1]+yn), radius)
    
        if previous[0] == previous[1] != None:
            options = colors.copy()
            options.remove(previous[0])
        else:
            options = colors
            
        color = random.choice(options)
        ball.setFill(color)
        ball.draw(win)
        
        balls.append((ball,color))
        del previous[0]
        previous.append(color)
    
    
    """ 
    Base/cannon/cannon ball/base/line 
    """
    
    theta = 0
    cannon = None
    line = None
    base.draw(win)
    circle.draw(win)
    
    cannon_ball = Circle(Point((p1.getX() + p2.getX())/2, (p1.getY() + p2.getY())/2), radius)
    color = random.choice(colors)
    cannon_ball.setFill(color)
    
    cannon_ball.draw(win)
    instruc.draw(win)
    
    start_p.draw(win)
    end_p.draw(win)
    
    
    """
    Start level
    """
    
    while not close: 
        ck = win.checkKey()
        close = win.checkMouse()
        restart = ck == "Return"
        new = ck == "space"
        
        """
        Redraw/move cannon/cannon ball/line with new theta
        """
        
        theta+=0.05
        p1 = Point(la*math.cos(theta-math.radians(90))+can_x,
                   la*math.sin(theta-math.radians(90))+can_y)
        p2 = Point(la*math.cos(theta+math.pi/2)+can_x,
                   la*math.sin(theta+math.pi/2)+can_y)
        p3 = Point(lb*math.cos(theta+math.radians(inc))+p1.getX(),
                   lb*math.sin(theta+math.radians(inc))+p1.getY())    
        p4 = Point(lb*math.cos(theta+math.radians(-inc))+p2.getX(),
                   lb*math.sin(theta+math.radians(-inc))+p2.getY())
        if cannon:
            cannon.undraw()       
        if line:
            line.undraw()  
            
        cannon = Polygon([p1, p2, p4, p3])
        cannon.setFill("gray30")
            
        movex =  (p3.getX() + p4.getX())/2 - cannon_ball.getCenter().getX()
        movey =  (p3.getY() + p4.getY())/2 - cannon_ball.getCenter().getY()
        cannon_ball.move(movex, movey)
        
        line = Line(Point(cannon_ball.getCenter().x, cannon_ball.getCenter().y),
                    Point(cannon_ball.getCenter().x+2*650*math.cos(theta),
                          cannon_ball.getCenter().y+2*650*math.sin(theta)))
        
        line.draw(win)
        cannon.draw(win)
        
        """
        Move balls along PathLines
        """
        for c in balls:
            move(lines[4:], c[0], v)     
            if c[0].getCenter().x >= lines[-1].xs[2] and c[0].getCenter().y >= lines[-1].ys[2]:
                """
                A ball reached the end point --> Game over
                Undraw ball
                """
                end = True
                v = 20
                c[0].undraw()
                balls.remove(c)
        update(30)
        
        if not end:
            if change:
                """
                If there is a new ball in the path or balls were deleted,
                then check for 3 or more balls of the same color in a row and 
                set delete = True
                """
                change = delete = False
                counter = ind = col = 0
                
                for i in range(len(balls)):
                    if not col == balls[i][1]:
                        col = balls[i][1]
                        if counter >= 3:
                            delete = True
                            range_del = (i-counter, i-1)
                            counter = 1
                            break
                        counter = 1
                    else:
                        counter+=1
                        if counter>=3 and i+1 == len(balls):
                            delete = True
                            range_del = (i-counter+1, i)
                            counter = 1             
                            break
        
                
            if delete:  
                """
                If there are balls to be deleted
                """
                change = True
                delete = False
                for c in balls[range_del[0]: range_del[1]+1]:
                    c[0].undraw()
                    balls.remove(c)   
                for i in range(int(2*radius/10)*(range_del[1]+1-range_del[0])):
                    for c in balls[:range_del[0]]:
                        move(lines[4:], c[0], v = -10)  
                    update(30)            
        
            if new:
                """
                If a ball is thrown:
                    - Look for interception with all PathLines
                    - Sort by distance
                    - Check for closest ball to the interception point
                """
                change = True
                cb = cannon_ball.getCenter()
                dists = {}
                points = []
                for l in lines:
                    i = l.intercept((cb.getX(), cb.getY()), theta)
                    if i:
                        dists[l] = i[2]
                        points.append((i[0],i[1]))
                    else:
                        points.append(None)
                dists = sorted(dists, key=dists.get)
        
                d = 1000
                add = False
                dest=()
                for i in dists:                
                    dest = points[lines.index(i)]
                    if lines.index(i)<4:
                        continue
                    if add:
                        break
                    for b in balls:
                        dn = np.linalg.norm(np.array((b[0].getCenter().x,b[0].getCenter().y)) - 
                                            np.array((dest[0],dest[1])))
                        if dn<d:
                            d = dn
                            n = balls.index(b)                  
                        if d<2*radius:
                            add = True
                            break
        
                if add:      
                    """
                    If there is a ball close to the interception point:
                        - Create new ball
                        - The destination is the position of the closest ball
                            to the interception point
                        - Insert new ball in balls
                        - Move previous balls to get space for the new one           
                    """
                    xn, yn = (balls[n][0].getCenter().x,
                              balls[n][0].getCenter().y)       
                    newb = Circle(Point(xn, yn), radius)
                    newb.setFill(color)
                    dx = xn - cb.x
                    dy = yn - cb.y
                    balls.insert(n+1, (newb,color))
                    
                    for i in range(int(2*radius/10)):
                        for c in balls[:n+1]:
                            move(lines[4:], c[0], v=10)    
                        update(30)           
                    
                else: 
                    """
                    The destination will be the interception point 
                    """
                    dx = round(dest[0],2) - round(cb.x,2)
                    dy = round(dest[1],2) - round(cb.y,2)
                
                """
                Move cannon ball to destination
                """
                for i in range(5):
                    cannon_ball.move(dx/5, dy/5)    
                    update(30)
                    
                if add:
                    """
                    If the ball was added to the path:
                        - Draw new ball 
                    """
                    newb.draw(win)
                 
                """
                Redraw cannon ball/cannon/start/end
                """
                cannon_ball.undraw()
                start_p.undraw()
                end_p.undraw()
                cannon.undraw()
                
                cannon_ball = Circle(Point(cb.x, cb.y), radius)
                color = random.choice(colors)
                cannon_ball.setFill(color)
                cannon_ball.draw(win)
            
                cannon.draw(win)   
                start_p.draw(win)
                end_p.draw(win)
                
                update(30)
    
    
            if not balls:
                """
                All the balls were deleted -> End -> Win
                """
                end = True
                
                """
                Undraw all the graphic elements
                """                
                instruc.undraw()
                cannon.undraw()
                circle.undraw()
                base.undraw()
                cannon_ball.undraw()
                line.undraw()
                start_p.undraw()
                end_p.undraw()
                for i,j in paths:
                    i.undraw()
                    j.undraw()
                
                    
                if level == 2:
                    """
                    Game over
                    """
                    
                    """
                    Set up final window 
                    """
                    t_restart = Image(Point(325, 325), "end.png")
                    t_restart.draw(win)
                    restart = win.checkKey()
                    close = win.checkMouse()
                    end_balls1 = []
                    prev = 0
                    for i in range(1000):
                        ball = Circle(Point(50, prev), radius)
                        prev-=2*radius
                        ball.setFill(random.choice(options))
                        ball.draw(win)
                        end_balls1.append(ball)
                    end_balls2 = []
                    prev = 650
                    for i in range(1000):
                        ball = Circle(Point(600, prev), radius)
                        prev+=2*radius
                        ball.setFill(random.choice(options))
                        ball.draw(win)
                        end_balls2.append(ball)
                    """
                    Wait for user to close window or restart the game
                    """
                    while not (restart or close):
                        restart = win.checkKey() == "Return"
                        close = win.checkMouse() 
                        for b in end_balls1:
                            b.move(0,10)
                        for b in end_balls2:
                            b.move(0,-10)
                        update(30)
                        
                    """
                    Undraw final window graphic elements
                    """
                    for b in end_balls1+end_balls2:
                        b.undraw()
                    t_restart.undraw()
                    
                    """
                    Break out of this level
                    """
                    if restart:
                        level = 0 
                        break                 
                    else:
                        """
                        close will be checked in the begginig of the outter loop
                        """
                        break
                """
                If it isn't the last level, just go on to the next level
                """
                level+=1
                break
    
        else:
            """
            A ball reached the end point -> End -> Lose
            """
            if not balls:
                """
                If all the balls have been undrawn:
                    - Undraw all the graphic elements
                    - Go back to first level
                    - Break out of this level
                """
                instruc.undraw()
                cannon.undraw()
                circle.undraw()
                base.undraw()
                cannon_ball.undraw()
                line.undraw()
                start_p.undraw()
                end_p.undraw()
                for i,j in paths:
                    i.undraw()
                    j.undraw()
                              
                level = 0
                break
        

win.close()
win.update()