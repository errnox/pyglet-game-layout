import math
import random

import pyglet
from pyglet.gl import *

class App(pyglet.window.Window):
  def __init__(self):
    super(App, self).__init__(width=800, height=600)
    # glClearColor(0.04, 0.08, 0.09, 1.0)
    self.is_fullscreen = False
    self.main_label = pyglet.text.Label(
      'Hello', font_name='Monospace', x = self.width/2,
      y=self.height/2, anchor_x='center', anchor_y='center')
    self.fps_label = pyglet.text.Label(
      '{} fps'.format(str(int(round(pyglet.clock.get_fps())))),
      font_name='Monospace', x = 35, y=self.height - 15,
      anchor_x='center', anchor_y='center')
    self.colors = [
      (255, 0, 0, 255),
      (0, 255, 0, 255),
      (0, 0, 255, 255),
      (255, 255, 0, 255),
      (255, 255, 0, 255),
    ]
    self.mx = self.width / 2
    self.my = self.height / 2
    self.fps_display = pyglet.clock.ClockDisplay()

    pyglet.resource.path = ['res']
    pyglet.resource.reindex()
    self.player_image = pyglet.resource.image('player.png')
    self.player_texture = self.player_image.get_texture()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    self.player_texture.width = 300
    self.player_texture.height = 300

    # Log all events
    #
    # self.push_handlers(pyglet.window.event.WindowEventLogger())

    # pyglet.resource.path = ['res']
    # pyglet.resource.reindex()
    self.pew_sound = pyglet.resource.media(
      'pew.wav', streaming=False)

    self.keys = pyglet.window.key.KeyStateHandler()
    self.push_handlers(self.keys)

    pyglet.clock.schedule_interval(self.jitter_main_label, 0.4)

  def jitter_main_label(self, dt):
    if self.main_label.x < self.width / 2:
      self.shake_main_label()

  def shake_main_label(self):
    self.main_label.x += random.randint(-60, 60)
    self.main_label.y += random.randint(-60, 60)

  def run(self):
    pyglet.app.run()

  def update(self):
    self.fps_label.text = '{} fps'.format(
      str(int(round(pyglet.clock.get_fps()))))

    self.main_label.text = "{}, {}".format(self.mx, self.my)
    self.main_label.color = random.choice(self.colors)
    # self.main_label.x += 1
    if self.main_label.x > self.width:
      self.main_label.x = 0
    elif self.main_label.x < 0:
      self.main_label.x = self.width

    dmx = self.mx - self.main_label.x
    dmy = self.my - self.main_label.y
    if self.main_label.x != self.mx and self.main_label.y != self.my:
      self.main_label.x += dmx / 10
      self.main_label.y += dmy / 10

  def on_draw(self):
    self.clear()
    # glClear(GL_COLOR_BUFFER_BIT)
    if self.keys[pyglet.window.key.LCTRL] == True:
      glViewport(self.width/2-self.mx/10-self.width/2,
                 self.height/2-self.my/10-self.height/2,
                 self.width, self.height)
    glColor3f(1.0, 1.0, 1.0)
    self.fps_display.draw()
    self.update()
    self.draw_triangle()
    self.main_label.draw()
    self.fps_label.draw()
    self.player_texture.blit(self.width/2, self.height/2)
    self.draw_objects()
    glFlush()

  def draw_objects(self):
    glColor3f(1.0, 0.3, 0.3)
    # glBegin(GL_POLYGON)
    # glVertex3f(250.0+self.mx/10, 250.0+self.my/10, 0.0)
    # glVertex3f(270.0+self.mx/10, 250.0+self.my/10, 0.0)
    # glVertex3f(270.0+self.mx/10, 270.0+self.my/10, 0.0)
    # glVertex3f(250.0+self.mx/10, 270.0+self.my/10, 0.0)
    # glEnd()

    for y in range(5):
      for x in range(5):
        # glBegin(GL_POLYGON)
        # glColor3f(1.0*x/5, 0.3*x/5, 0.3)
        # glVertex3f(250.0+(x*50)+self.mx/10, 250.0+(y*50)+self.my/10, 0.0)
        # glVertex3f(270.0+(x*50)+self.mx/10, 250.0+(y*50)+self.my/10, 0.0)
        # glVertex3f(270.0+(x*50)+self.mx/10, 270.0+(y*50)+self.my/10, 0.0)
        # glVertex3f(250.0+(x*50)+self.mx/10, 270.0+(y*50)+self.my/10, 0.0)
        # glEnd()

        # Shorter version:
        #
        glPushMatrix()
        glRotatef(15.0, 0.0, 0.0, 1.0)
        glTranslatef(-20.0, -20.0, 0.0)
        glColor3f(1.0*x/5, 0.3*x/5, 0.3)
        glRectf(
          250.0+(x*50)+self.mx/10, 250.0+(y*50)+self.my/10,
          270.0+(x*50)+self.mx/10, 270.0+(y*50)+self.my/10)
        glPopMatrix()

    glColor3f(1.0, 0.2, 0.2)
    d = 0.01
    r = 30
    glBegin(GL_POLYGON)
    for i in range(2*int(math.pi)*100):
      glVertex3f(200+r*math.cos(i*d)+self.mx/10,
                 200+r*math.sin(i*d)+self.my/10, 0.0)
    glEnd()

    glColor3f(1.0, 1.0, 0.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    glEdgeFlag(GL_TRUE)
    glVertex3f(150.0, 150.0, 0.0)
    glVertex3f(170.0, 150.0, 0.0)
    glEdgeFlag(GL_FALSE)
    glVertex3f(180.0, 160.0, 0.0)
    glVertex3f(160.0, 170.0, 0.0)
    glEdgeFlag(GL_TRUE)
    glVertex3f(130.0, 140.0, 0.0)
    glEdgeFlag(GL_FALSE)
    glVertex3f(150.0, 120.0, 0.0)
    glEnd()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

  def draw_triangle(self):
    # glClear(GL_COLOR_BUFFER_BIT)
    # glLoadIdentity()
    # glBegin(GL_TRIANGLES)
    # glVertex2f(0, 0)
    # glVertex2f(self.width/2, self.main_label.y)
    # glVertex2f(self.width/2, self.main_label.x)
    # glEnd()

    # pyglet.graphics.draw(2, GL_POINTS, ('v2i', (10, 15, 30, 35)))
    v = tuple([i for i in range(self.mx)])
    if len(v) % 2 != 0:
      v = v[:-1]
    data = ('v2i', v)
    pyglet.graphics.draw(len(v) / 2, GL_POINTS, data)

    # Draw a green square.
    #
    # pyglet.graphics.draw(
    #   4, GL_QUADS,
    #   ('v2i', (0, 0, 0, self.my, self.mx, self.my, self.mx, 0)),
    #   ('c3B', (0, 255, 120) * 4))

  def on_key_press(self, symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
      self.main_label.x = self.width / 2
    elif symbol == pyglet.window.key.LEFT:
      self.main_label.x -= 10
    elif symbol == pyglet.window.key.RIGHT:
      self.main_label.x += 10
    elif (symbol == pyglet.window.key.F and
      modifiers == pyglet.window.key.MOD_CTRL):
      self.is_fullscreen = not self.is_fullscreen
      self.set_fullscreen(self.is_fullscreen)
    elif (symbol == pyglet.window.key.Q and
      modifiers == pyglet.window.key.MOD_CTRL):
      pyglet.app.exit()

  def on_mouse_motion(self, x, y, dx, dy):
    self.mx = x
    self.my = y

  def on_mouse_press(self, x, y, button, modifiers):
    self.pew_sound.play()
    self.mx = x
    self.my = y
    if button == pyglet.window.mouse.LEFT:
      self.shake_main_label()

  def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
    self.mx = x
    self.my = y


if __name__ == '__main__':
  app = App()
  app.run()
