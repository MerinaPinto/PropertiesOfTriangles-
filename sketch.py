from p5 import *

def setup():
  createCanvas(windowWidth,windowHeight)
  global p1,p2,p3
  p1 = createMovableCircle(100,300,20)
  p2 = createMovableCircle(250,500,20)
  p3 = createMovableCircle(400,300,20)
  
def draw():
  background("black")
  global p1,p2,p3

  drawTickAxes()
  p1.draw()
  p2.draw()
  p3.draw()

  strokeWeight(4)
  stroke("red")
  line(p1.x,p1.y,p2.x,p2.y)

  strokeWeight(4)
  stroke("blue")
  line(p2.x,p2.y,p3.x,p3.y)

  strokeWeight(4)
  stroke("green")
  line(p3.x,p3.y,p1.x,p1.y)

  lengthRed = calculatesides(p2.x,p1.x,p2.y,p1.y)
  lengthBlue = calculatesides(p3.x,p2.x,p3.y,p2.y)
  lengthGreen = calculatesides(p3.x,p1.x,p3.y,p1.y)

  
  # acos(((b**2)+(c**2)-(a**2))/(2*b*c))
  #lengthRed = c
  #lengthGreen = b
  #lengthBlue = a
  
  #acos = inverse of cos 
  angleA = acos(((lengthGreen**2)+(lengthRed**2)-(lengthBlue**2))/(2*lengthGreen*lengthRed))  #A - oppsite blue

  angleB = acos(((lengthBlue**2)+(lengthRed**2)-(lengthGreen**2))/(2*lengthRed*lengthBlue)) #B

  angleC = 180-angleA-angleB
  
  #text(output, x, y) -- sides 
  noStroke()
  fill("white")
  text(round(lengthRed,2),(p1.x+p2.x)/2,(p1.y+p2.y)/2)
  text(round(lengthBlue,2),(p2.x+p3.x)/2,(p2.y+p3.y)/2)
  text(round(lengthGreen,2),(p1.x+p3.x)/2,(p1.y+p3.y)/2)
  text(round(angleA,2),p1.x+10,p1.y)
  text(round(angleB,2),p2.x+10,p2.y)
  text(round(angleC,2),p3.x+10,p3.y)
  text("A=",p1.x+7,p1.y+10)
  text("B=",p2.x+7,p2.y+10)
  text("C=",p3.x+7,p3.y+10)


  #Mutually exclusive = both cannot happen at same time (either or)

  rightAngle = angleA == 90 or angleB == 90 or angleC == 90
  obtuseAngle = angleA > 90 or angleB > 90 or angleC > 90
  acuteAngle = angleA < 90 and angleB < 90 and angleC < 90

  angleType = "This triangle is"
  
  if obtuseAngle:
    angleType += " Obtuse" 
  elif acuteAngle:
    angleType += " Acute" 
  elif rightAngle: 
    angleType += " Right Angle"


  noStroke()
  fill("white")
  text(angleType, 250, 550)

  Equilateral = lengthRed == lengthBlue == lengthGreen 
  Isosceles = not Equilateral and (lengthRed == lengthBlue or lengthBlue == lengthGreen or lengthRed == lengthGreen) 
  Scalene = not Equilateral and not Isosceles

  #pcik up here
  angleType = "This triangle is"
  
  if obtuseAngle:
    angleType += " Obtuse" 
  elif acuteAngle:
    angleType += " Acute" 
  elif rightAngle: 
    angleType += " Right Angle"


  noStroke()
  fill("white")
  text(angleType, 250, 550)

def calculatesides(x2,x1,y2,y1):
  return sqrt(((x2-x1)**2)+((y2-y1)**2)) #((p2.x-p1.x)**2)+((p2.y-p1.y)**2))

def createMovableCircle(x, y, d, clr=None):
  return MovableCircle(x, y, d, clr)

class MovableCircle:
  instances = []
  currently_dragging = None

  def __init__(self, x, y, d, clr=None):
    self.x = x
    self.y = y
    self.d = d
    self.clr = clr
    self.dragging = False
    self.rollover = False
    self.offset_x = 0
    self.offset_y = 0
    MovableCircle.instances.append(self)

  def draw(self):
    self.update()
    if self.rollover:
      fill(self.clr if self.clr else 'red')
    else:
      fill(200)
    noStroke()
    circle(self.x, self.y, self.d)

  def update(self):
    # Check if mouse is over the circle
    if dist(mouseX, mouseY, self.x, self.y) < self.d / 2:
      self.rollover = True
    else:
      self.rollover = False

    # If being dragged, update position to mouse coordinates with offset
    if self.dragging:
      self.x = mouseX + self.offset_x
      self.y = mouseY + self.offset_y

  def mousePressed(self):
    # Check if the mouse is pressed within the circle
    if self.rollover and MovableCircle.currently_dragging is None:
      self.dragging = True
      MovableCircle.currently_dragging = self
      self.offset_x = self.x - mouseX
      self.offset_y = self.y - mouseY

  def mouseReleased(self):
    # Stop dragging
    if self.dragging:
      self.dragging = False
      MovableCircle.currently_dragging = None

  @classmethod
  def handle_mouse_pressed(cls):
    for instance in reversed(cls.instances):  # Check the topmost circle first
      instance.mousePressed()
      if cls.currently_dragging:
        break  # Exit loop if a circle is selected

  @classmethod
  def handle_mouse_released(cls):
    if cls.currently_dragging:
      cls.currently_dragging.mouseReleased()

# Call the mouse event functions for all circles
def mousePressed():
  MovableCircle.handle_mouse_pressed()

def mouseReleased():
  MovableCircle.handle_mouse_released()
