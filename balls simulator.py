import pygame as pg
import tkinter as tk
import random
import math
import json
pg.init()

def get_screen_size():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()  # Destroy the hidden window
    return screen_width, screen_height

#settings
hide_mouse = True
spawn_random_x = True
spawn_random_y = False

ball_size_multiplier = 0.5
gravity = 0.4
clockspeed = 100
base_restitution = 0.8
base_friction_cutoff = 2
random_maxupscale = 2
random_xvelscale = 30

color_choices = [
    (0,0,255),
    (0,255,0),
    (0,255,255),
    (255,0,0),
    (255,0,255),
    (255,255,0),
    (255,255,255),
    ]


background_color = (0,0,0)







displaysize = get_screen_size()
display = pg.display.set_mode(displaysize,pg.FULLSCREEN)
ball_radius = ball_size_multiplier*displaysize[0]/40
if hide_mouse:
    pg.mouse.set_visible(False)


class ball_class:
    def __init__(self,pos,vel,radius,restitution_coefficent,color):
        self.x,self.y = pos
        self.color = color
        self.xvel,self.yvel = vel
        self.radius = radius
        self.res = restitution_coefficent
        self.mass = self.radius


    def draw_self(self):
        pg.draw.circle(display,self.color,(self.x,self.y),self.radius)
        
    def collide_balls(self):
        global balls
        for other_ball in balls:
            if other_ball != self:
                dx = other_ball.x - self.x
                dy = other_ball.y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)                # Calculate the distance between the centers of the two balls
                # Check if the balls are colliding
                if distance < self.radius + other_ball.radius:

                    

                    normal_x = dx / distance
                    normal_y = dy / distance

                    # Calculate the relative velocity
                    relative_velocity_x = other_ball.xvel - self.xvel
                    relative_velocity_y = other_ball.yvel - self.yvel

                    # Calculate the dot product of the relative velocity and the normal vector
                    dot_product = relative_velocity_x * normal_x + relative_velocity_y * normal_y

                    # Apply the impulse to both balls
                    impulse = (2 * dot_product) / (1 / self.res + 1 / other_ball.res)
                    impulse_x = impulse * normal_x
                    impulse_y = impulse * normal_y

                    self.xvel += impulse_x / self.res
                    self.yvel += impulse_y / self.res

                    other_ball.xvel -= impulse_x / other_ball.res
                    other_ball.yvel -= impulse_y / other_ball.res

                    # Move the balls to resolve collision
                    overlap = (self.radius + other_ball.radius - distance) / 2
                    self.x -= overlap * normal_x
                    self.y -= overlap * normal_y
                    other_ball.x += overlap * normal_x
                    other_ball.y += overlap * normal_y                    







                    



                    
    def collide_self(self):
        # collide walls
        if self.x < self.radius:
            self.x = self.radius
            self.xvel = (-self.xvel)*self.res

        if self.y < self.radius:
            self.y = self.radius
            self.yvel = (-self.yvel)*self.res


        if self.x > displaysize[0] - self.radius:
            self.x = displaysize[0] - self.radius
            self.xvel = (-self.xvel)*self.res

        if self.y > displaysize[1] - self.radius:
            self.y = displaysize[1] - self.radius
            self.yvel = (-self.yvel)*self.res

        self.collide_balls()


    def move_self(self):
        self.yvel += gravity


        self.x += self.xvel

        self.y += self.yvel




def logic_calls():
    for ball in balls:
        ball.move_self()
        ball.collide_self()
        

    clock.tick(clockspeed)


def graphic_calls():
    display.fill(background_color)
    for ball in balls:
        ball.draw_self()


    pg.display.flip()
    
def spawn_ball():
    global balls
    x,y = 0,0
    radius = round(ball_radius + ball_radius*(random.random()*random_maxupscale))
    color = random.choice(color_choices)
    if spawn_random_x:
        x = random.randint(radius,displaysize[0]-radius)
    if spawn_random_y:
        y = random.randint(radius,displaysize[1]-radius)


    balls.append(ball_class((x,y),(random.randint(-abs(random_xvelscale),abs(random_xvelscale)),0),radius,base_restitution,color))



def main():
    global dead,balls,clock
    clock = pg.time.Clock()
    dead = False
    balls = []
    while not dead:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                dead = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    dead = True
                if event.key == pg.K_g:
                    spawn_ball()
                if event.key == pg.K_h and len(balls) > 0:
                    balls.pop(0)
                    



        keystate = pg.key.get_pressed()

        if keystate[pg.K_l]:
            spawn_ball()
        if keystate[pg.K_p] and len(balls) > 0:
            balls.pop(0)




        logic_calls()
        graphic_calls()





main()
pg.quit()
quit()












