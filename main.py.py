import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QPushButton
from PyQt5.QtCore import QTimer, QRectF
from PyQt5.QtGui import QPainter, QPixmap
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import pi, sin, cos, radians
from datetime import datetime, timedelta  
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18
from PIL import Image

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):  # Accept parent argument
        super().__init__(parent)
        self.animation_state = "entering"  # Initial animation state
        self.position_x = 300
        self.position_y = -900
        self.mcg_logo_position_x = 259  # Initial X position of the MCG logo
        self.mcg_logo_position_y = -90  # Initial Y position of the MCG logo
        self.animation_speed = 100 # Increase the animation speed (pixels per frame)
        self.paused = False  # Variable to track if animation is paused or not
        self.last_frame_time = datetime.now()

    def initializeGL(self):
        glutInit()  # Initialize GLUT
        glClearColor(0.529, 0.808, 0.922, 1.0)
        glEnable(GL_BLEND)  # Enable blending
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blending function
        
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)  # Set the OpenGL viewport to match the window size
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        
    # Function to draw text on the OpenGL canvas
    def draw_text(self, text, x, y):  # Made it a method of the class
        glRasterPos2f(x, y)
        for character in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        
        self.paintSky()

        self.draw_cancelor_hall() 
        
        self.draw_smaller_shorter_rect_with_text()

        self.draw_trees()

        self.draw_bushes()

        self.draw_clocktower()

        self.draw_trapezium()

        self.draw_clock()
        
        self.draw_ums_logo()
        
        self.draw_mcg_logo()
        
        if not self.paused:  # Only update animation if not paused
            self.update_animation()
        
        # Draw clouds
        self.draw_cloud([(100, 100), (129, 115), (75, 115), (100, 127)])
        self.draw_cloud([(578, 55), (550, 70), (610, 70), (570, 85)])
        
    def paintSky(self):
        glBegin(GL_QUADS)
        # Define colors for the evening sky gradient
        glColor3f(0.3, 0.4, 0.6)  # Slightly darker blue
        glVertex2f(0, 0)
        glVertex2f(self.width(), 0)
        glColor3f(0.53, 0.8, 0.9)  # Sky blue color
        glVertex2f(self.width(), self.height())
        glVertex2f(0, self.height())
        glEnd()

    def draw_bushes(self):
        # Draw the main shape of the bush
        glColor3ub(0, 79, 0)  # Green color for the main bush
        main_circle_radius = 100 # Adjust the radius of the main half circle
        bush_height = 50  # Adjust the height of the half circle
        glBegin(GL_POLYGON)
        for i in range(50):
            angle = pi * i / 50  # Use only half of the circle
            x = 100 + main_circle_radius * cos(angle)  # Adjust the center and radius as needed
            y = 545 - bush_height * sin(angle)  # Increase the height by adjusting the multiplier
            glVertex2f(x, y)
        glEnd()

        # Draw smaller circular shapes to represent leaves
        smaller_centers = [(50, 510), (100, 490), (150, 510)]  # Adjust these positions as needed
        smaller_radius = 30  # Adjust the radius of the smaller circles
        num_segments = 50
        for center in smaller_centers:
            glBegin(GL_POLYGON)
            for i in range(num_segments):
                angle = 2 * pi * i / num_segments
                x = center[0] + smaller_radius * cos(angle)
                y = center[1] + smaller_radius * sin(angle)
                glVertex2f(x, y)
            glEnd()
       
    def draw_trees(self):
        # Tree parameters
        trunk_height = 150
        trunk_width = 20
        tree_top_radius = 60
        num_segments = 50
        num_leaves = 10  # Number of leaves
        leaf_radius = 25  # Radius of the leaves
        lower_amount = -30  # Amount to lower the trees by

        # Draw left tree
        left_tree_x = self.width() / 6 - trunk_width / 2 - 50  # Adjusted x-coordinate
        glColor3f(0.545, 0.271, 0.075)  # Brown color for trunk
        glBegin(GL_QUADS)
        glVertex2f(left_tree_x, self.height() * 0.7 - lower_amount)  # Adjusted y-coordinate
        glVertex2f(left_tree_x + trunk_width, self.height() * 0.7 - lower_amount)  # Adjusted y-coordinate
        glVertex2f(left_tree_x + trunk_width, self.height() * 0.7 - trunk_height - lower_amount)  # Adjusted y-coordinate
        glVertex2f(left_tree_x, self.height() * 0.7 - trunk_height - lower_amount)  # Adjusted y-coordinate
        glEnd()

        glColor3f(0.0, 0.5, 0.0)  # Dark green color for tree top
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(left_tree_x + trunk_width / 2, self.height() * 0.7 - trunk_height - lower_amount)  # Adjusted y-coordinate
        for i in range(num_segments + 1):
            angle = i * (2.0 * pi / num_segments)
            glVertex2f(left_tree_x + trunk_width / 2 + tree_top_radius * cos(angle), self.height() * 0.7 - trunk_height - lower_amount + tree_top_radius * sin(angle))  # Adjusted y-coordinate
        glEnd()

        # Draw leaves for left tree
        glColor3f(0.0, 0.5, 0.0)  # Dark green color for leaves
        leaf_angle = (2.0 * pi) / num_leaves  # Angle between each leaf
        for i in range(num_leaves):
            leaf_center_x = left_tree_x + trunk_width / 2 + tree_top_radius * cos(i * leaf_angle)
            leaf_center_y = self.height() * 0.7 - trunk_height - lower_amount + tree_top_radius * sin(i * leaf_angle)
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(leaf_center_x, leaf_center_y)
            for j in range(num_segments + 1):
                angle = j * (2.0 * pi / num_segments)
                glVertex2f(leaf_center_x + leaf_radius * cos(angle), leaf_center_y + leaf_radius * sin(angle))
            glEnd()

        # Draw right tree
        right_tree_x = self.width() * 5 / 6 - trunk_width / 2 + 50  # Adjusted x-coordinate
        glColor3f(0.545, 0.271, 0.075)  # Brown color for trunk
        glBegin(GL_QUADS)
        glVertex2f(right_tree_x, self.height() * 0.7 - lower_amount)  # Adjusted y-coordinate
        glVertex2f(right_tree_x + trunk_width, self.height() * 0.7 - lower_amount)  # Adjusted y-coordinate
        glVertex2f(right_tree_x + trunk_width, self.height() * 0.7 - trunk_height - lower_amount)  # Adjusted y-coordinate
        glVertex2f(right_tree_x, self.height() * 0.7 - trunk_height - lower_amount)  # Adjusted y-coordinate
        glEnd()

        glColor3f(0.0, 0.5, 0.0)  # Dark green color for tree top
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(right_tree_x + trunk_width / 2, self.height() * 0.7 - trunk_height - lower_amount)  # Adjusted y-coordinate
        for i in range(num_segments + 1):
            angle = i * (2.0 * pi / num_segments)
            glVertex2f(right_tree_x + trunk_width / 2 + tree_top_radius * cos(angle), self.height() * 0.7 - trunk_height - lower_amount + tree_top_radius * sin(angle))  # Adjusted y-coordinate
        glEnd()

        # Draw leaves for right tree
        glColor3f(0.0, 0.5, 0.0)  # Dark green color for leaves
        for i in range(num_leaves):
            leaf_center_x = right_tree_x + trunk_width / 2 + tree_top_radius * cos(i * leaf_angle)
            leaf_center_y = self.height() * 0.7 - trunk_height - lower_amount + tree_top_radius * sin(i * leaf_angle)
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(leaf_center_x, leaf_center_y)
            for j in range(num_segments + 1):
                angle = j * (2.0 * pi / num_segments)
                glVertex2f(leaf_center_x + leaf_radius * cos(angle), leaf_center_y + leaf_radius * sin(angle))
            glEnd()
            
        # Draw the ground (green gradient)
        glBegin(GL_QUADS)
        for i in range(1):  # Split into 10 segments for gradient effect
            glColor3f(0.0, 0.3 + i * 0.02, 0.0)  # Darker green at the bottom
            glVertex2f(0, self.height() * 0.73 + i * (self.height() * 0.27 / 1))  # Adjust y-coordinate here
            glVertex2f(self.width(), self.height() * 0.73 + i * (self.height() * 0.27 / 1))  # Adjust y-coordinate here
            glColor3f(0.0, 0.5 + (i + 1) * 0.02, 0.0)  # Lighter green towards the top
            glVertex2f(self.width(), self.height() * 0.73 + (i + 1) * (self.height() * 0.27 / 1))  # Adjust y-coordinate here
            glVertex2f(0, self.height() * 0.73 + (i + 1) * (self.height() * 0.27 / 1))  # Adjust y-coordinate here
        glEnd()

        # Draw grass (tiny triangles)
        grass_height = self.height() * 0.03  # Height of the grass triangles, adjust as needed
        num_triangles = 120  # Number of triangles, adjust as needed
        triangle_width = self.width() / num_triangles + 5 # Width of each triangle

        # Adjust the y position of the grass
        grass_y_position = self.height() * 0.74  # Change this value as needed

        glColor3f(0.0, 0.3, 0.0)  # Lighter green color for grass

        glBegin(GL_TRIANGLES)
        for i in range(num_triangles):
            # Calculate the vertices of the triangle
            x1 = i * triangle_width
            y1 = grass_y_position
            x2 = x1 + triangle_width / 2
            y2 = y1 - grass_height
            x3 = x1 + triangle_width
            y3 = y1
            
            # Draw the triangle
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
            glVertex2f(x3, y3)
        glEnd()

    def draw_clocktower(self):
        # Draw shorter rectangle
        glColor3f(0.1, 0.1, 0.1)  # Light gray color
        rect_width = 170  # Adjusted width of the rectangle
        rect_height = 400  # Adjusted height of the rectangle
        rect_x = (self.width() - rect_width) / 2  # X-coordinate of the rectangle's top-left corner
        rect_y = self.height() - rect_height  # Y-coordinate of the rectangle's top-left corner
        glBegin(GL_QUADS)
        glVertex2f(rect_x, rect_y)
        glVertex2f(rect_x + rect_width, rect_y)
        glVertex2f(rect_x + rect_width, self.height())
        glVertex2f(rect_x, self.height())
        glEnd()

        # Draw black outline for the rectangle
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        glVertex2f(rect_x, rect_y)
        glVertex2f(rect_x + rect_width, rect_y)
        glVertex2f(rect_x + rect_width, self.height())
        glVertex2f(rect_x, self.height())
        glEnd()

        # Draw shorter square above the rectangle
        glColor3f(0.8, 0.8, 0.8)  # Light gray color
        square_width = 120  # Adjusted width of the square
        square_height = 70  # Adjusted height of the square
        square_x = (self.width() - square_width) / 2  # X-coordinate of the square's top-left corner
        square_y = rect_y - square_height  # Y-coordinate of the square's top-left corner
        glBegin(GL_QUADS)
        glVertex2f(square_x, square_y)
        glVertex2f(square_x + square_width, square_y)
        glVertex2f(square_x + square_width, rect_y)
        glVertex2f(square_x, rect_y)
        glEnd()
        
        # Draw shorter square above the rectangle with darker to lighter gray gradient
        glBegin(GL_QUADS)
        for i in range(50):  # Split into 10 segments for gradient effect
            for j in range(50):  # Split each segment into 10 sub-segments for smoother gradient
                color_factor_x = i / 10.0  # Calculate color factor based on position within segment in x-direction
                color_factor_y = j / 10.0  # Calculate color factor based on position within segment in y-direction
                color_r = 0.4 + color_factor_x * 0.1 + color_factor_y * 0.0  # Interpolate red component
                color_g = 0.4 + color_factor_x * 0.1 + color_factor_y * 0.0  # Interpolate green component
                color_b = 0.4 + color_factor_x * 0.1 + color_factor_y * 0.0  # Interpolate blue component
                glColor3f(color_r, color_g, color_b)  # Set color for this sub-segment
                x1 = square_x + (i * square_width / 50)  # Left x-coordinate of the sub-segment
                x2 = square_x + ((i + 1) * square_width / 50)  # Right x-coordinate of the sub-segment
                y1 = square_y + (j * square_height / 10)  # Bottom y-coordinate of the sub-segment
                y2 = square_y + ((j + 1) * square_height / 10)  # Top y-coordinate of the sub-segment
                glVertex2f(x1, y1)  # Bottom left
                glVertex2f(x2, y1)  # Bottom right
                glVertex2f(x2, y2)  # Top right
                glVertex2f(x1, y2)  # Top left
        glEnd()

        # Draw black outline for the square
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        glVertex2f(square_x, square_y)
        glVertex2f(square_x + square_width, square_y)
        glVertex2f(square_x + square_width, rect_y)
        glVertex2f(square_x, rect_y)
        glEnd()

        # Draw the rectangle with gradient from darker gray to lighter gray
        glBegin(GL_QUADS)  # Begin drawing the rectangle
        for i in range(90):  # Split into 50 segments for gradient effect
            color_factor = i / 50.0  # Calculate color factor based on position within segment
            color_r = 0.4 + color_factor * 0.35  # Interpolate red component from 0.1 to 0.3
            color_g = 0.4 + color_factor * 0.35  # Interpolate green component from 0.1 to 0.3
            color_b = 0.4 + color_factor * 0.35  # Interpolate blue component from 0.1 to 0.3
            glColor3f(color_r, color_g, color_b)  # Set color for this segment
            x1 = rect_x + (i * rect_width / 90)  # Left x-coordinate of the segment
            x2 = rect_x + ((i + 1) * rect_width / 90)  # Right x-coordinate of the segment
            glVertex2f(x1, rect_y)
            glVertex2f(x2, rect_y)
            glVertex2f(x2, rect_y + rect_height)
            glVertex2f(x1, rect_y + rect_height)
        glEnd()  # End drawing the rectangle

        # Draw black outline for the rectangle
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        glVertex2f(rect_x, rect_y)
        glVertex2f(rect_x + rect_width, rect_y)
        glVertex2f(rect_x + rect_width, self.height())
        glVertex2f(rect_x, self.height())
        glEnd()

        # Draw dome above the square
        glColor3f(1.0, 0.843, 0.0)  # Gold color
        num_segments = 100  # Number of segments to approximate the dome
        dome_radius = square_width / 2.5  # Radius of the dome
        dome_center_x = square_x + square_width / 2  # X-coordinate of the dome's center (same as square center)
        dome_center_y = square_y - dome_radius / 40  # Y-coordinate of the dome's center
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(dome_center_x, dome_center_y)  # Center of the dome
        for i in range(num_segments + 1):
            angle = i * (2.0 * pi / num_segments)
            if angle >= pi:  # Only draw lower half of the circle
                glColor3f(1.0 - i * 0.01, 0.843 - i * 0.001, 0.0)  # Apply gold gradient
                glVertex2f(dome_center_x + dome_radius * cos(angle), dome_center_y + dome_radius * sin(angle))
        glEnd()

        glBegin(GL_TRIANGLE_FAN)
        for i in range(num_segments + 1):
            angle = i * (2.0 * pi / num_segments)
            # Calculate color based on gradient
            r = 6.0 - i * 0.01  # Adjust the rate of change to control the gradient
            g = 1.0 - i * 0.0025  # Adjust the rate of change to control the gradient
            b = 0.0
            glColor3f(r, g, b)  # Apply gold gradient
            if angle >= pi:  # Only draw lower half of the circle
                glVertex2f(dome_center_x + dome_radius * cos(angle), dome_center_y + dome_radius * sin(angle))
        glEnd()

        # Draw black outline for the dome
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        for i in range(num_segments + 1):
            angle = i * (2.0 * pi / num_segments)
            if angle >= pi:  # Only draw lower half of the circle
                glVertex2f(dome_center_x + dome_radius * cos(angle), dome_center_y + dome_radius * sin(angle))
        glEnd()

        # Draw thin pointy line above the dome
        line_width = 9  # Adjust the width of the line
        line_height = 70  # Adjust the height of the line
        line_x = dome_center_x - line_width / 2  # X-coordinate of the line's top-left corner
        line_y = dome_center_y - dome_radius  # Y-coordinate of the line's top-left corner, above the dome
        glColor3f(0.0, 0.0, 0.0)  # Black color for the line
        glBegin(GL_TRIANGLES)
        glVertex2f(line_x, line_y)
        glVertex2f(line_x + line_width, line_y)
        glVertex2f(dome_center_x, line_y - line_height)  # Vertex at the top of the line
        glEnd()
        
        # Draw tiny rectangles on the left and right top of the main rectangle
        glColor3f(1.0, 0.843, 0.0)  # Gold color
        rect_top_height = 10  # Height of the tiny rectangles
        rect_top_width = 15  # Width of the tiny rectangles
        
        # Adjust x-coordinate of the left tiny rectangle
        rect_top_left_x = rect_x - rect_top_width + 20  # Example: move 10 units to the left

        # Adjust x-coordinate of the right tiny rectangle
        rect_top_right_x = rect_x + rect_width - 20  # Example: move 10 units to the right

        # Adjust y-coordinate of the tiny rectangles (top of the main rectangle)
        rect_top_y = self.height() - rect_height - 11  # Example: move 20 units upward

        glBegin(GL_QUADS)
        glVertex2f(rect_top_left_x, rect_top_y)
        glVertex2f(rect_top_left_x + rect_top_width, rect_top_y)
        glVertex2f(rect_top_left_x + rect_top_width, rect_top_y + rect_top_height)
        glVertex2f(rect_top_left_x, rect_top_y + rect_top_height)
        
        glVertex2f(rect_top_right_x, rect_top_y)
        glVertex2f(rect_top_right_x + rect_top_width, rect_top_y)
        glVertex2f(rect_top_right_x + rect_top_width, rect_top_y + rect_top_height)
        glVertex2f(rect_top_right_x, rect_top_y + rect_top_height)
        glEnd()
        
        # Draw black outlines for the tiny rectangles (bottom and sides only)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINES)
        # Outline left tiny rectangle
        # Left side
        glVertex2f(rect_top_left_x, rect_top_y)  # Bottom left
        glVertex2f(rect_top_left_x, rect_top_y + rect_top_height)  # Top left

        # Bottom side
        glVertex2f(rect_top_left_x, rect_top_y)  # Bottom left
        glVertex2f(rect_top_left_x + rect_top_width, rect_top_y)  # Bottom right

        # Right side
        glVertex2f(rect_top_left_x + rect_top_width, rect_top_y)  # Bottom right
        glVertex2f(rect_top_left_x + rect_top_width, rect_top_y + rect_top_height)  # Top right

        # Outline right tiny rectangle
        # Left side
        glVertex2f(rect_top_right_x, rect_top_y)  # Bottom left
        glVertex2f(rect_top_right_x, rect_top_y + rect_top_height)  # Top left

        # Bottom side
        glVertex2f(rect_top_right_x, rect_top_y)  # Bottom left
        glVertex2f(rect_top_right_x + rect_top_width, rect_top_y)  # Bottom right

        # Right side
        glVertex2f(rect_top_right_x + rect_top_width, rect_top_y)  # Bottom right
        glVertex2f(rect_top_right_x + rect_top_width, rect_top_y + rect_top_height)  # Top right
        glEnd()
        
        # Draw two smaller squares on top of the small rectangles
        glColor3f(1.0, 0.843, 0.0)  # Gold color
        square_width = 9  # Width of the square
        square_height = 7  # Height of the square
        square_y = rect_top_y + rect_top_height - 15  # Place the squares just above the small rectangles

        # Calculate x-coordinate for both squares to place them at the same left and right positions
        square_left_x = rect_top_left_x + (rect_top_width - square_width) / 2
        square_right_x = rect_top_right_x + (rect_top_width - square_width) / 2

        # Draw the left square
        glBegin(GL_QUADS)
        glVertex2f(square_left_x, square_y)
        glVertex2f(square_left_x + square_width, square_y)
        glVertex2f(square_left_x + square_width, square_y + square_height)
        glVertex2f(square_left_x, square_y + square_height)
        glEnd()

        # Draw the right square
        glBegin(GL_QUADS)
        glVertex2f(square_right_x, square_y)
        glVertex2f(square_right_x + square_width, square_y)
        glVertex2f(square_right_x + square_width, square_y + square_height)
        glVertex2f(square_right_x, square_y + square_height)
        glEnd()
        
        # Draw black outlines for the smaller squares (sides only)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINES)
        # Outline left smaller square
        # Left side
        glVertex2f(square_left_x, square_y)  # Bottom left
        glVertex2f(square_left_x, square_y + square_height)  # Top left

        # Right side
        glVertex2f(square_left_x + square_width, square_y)  # Bottom right
        glVertex2f(square_left_x + square_width, square_y + square_height)  # Top right

        # Outline right smaller square
        # Left side
        glVertex2f(square_right_x, square_y)  # Bottom left
        glVertex2f(square_right_x, square_y + square_height)  # Top left

        # Right side
        glVertex2f(square_right_x + square_width, square_y)  # Bottom right
        glVertex2f(square_right_x + square_width, square_y + square_height)  # Top right
        glEnd()

        #------------- 3rd rect -----------------------------------------
        glColor3f(1.0, 0.843, 0.0)  # Gold color
        rect_top_height = 20  # Height of the tiny rectangles
        rect_top_width = 15  # Width of the tiny rectangles
        
        # Adjust x-coordinate of the left tiny rectangle
        rect_top_left_x = rect_x - rect_top_width + 20  # Example: move 10 units to the left

        # Adjust x-coordinate of the right tiny rectangle
        rect_top_right_x = rect_x + rect_width - 20  # Example: move 10 units to the right

        # Adjust y-coordinate of the tiny rectangles (top of the main rectangle)
        rect_top_y = self.height() - rect_height - 36  # Example: move 20 units upward

        glBegin(GL_QUADS)
        glVertex2f(rect_top_left_x, rect_top_y)
        glVertex2f(rect_top_left_x + rect_top_width, rect_top_y)
        glVertex2f(rect_top_left_x + rect_top_width, rect_top_y + rect_top_height)
        glVertex2f(rect_top_left_x, rect_top_y + rect_top_height)
        
        glVertex2f(rect_top_right_x, rect_top_y)
        glVertex2f(rect_top_right_x + rect_top_width, rect_top_y)
        glVertex2f(rect_top_right_x + rect_top_width, rect_top_y + rect_top_height)
        glVertex2f(rect_top_right_x, rect_top_y + rect_top_height)
        glEnd()
        
        # Draw black outlines for both sides of the left rectangle (sides only)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINES)
        # Left side of the left rectangle
        glVertex2f(rect_top_left_x, rect_top_y)
        glVertex2f(rect_top_left_x, rect_top_y + rect_top_height)
        # Right side of the left rectangle
        glVertex2f(rect_top_left_x + rect_top_width, rect_top_y)
        glVertex2f(rect_top_left_x + rect_top_width, rect_top_y + rect_top_height)
        glEnd()

        # Draw black outlines for both sides of the right rectangle (sides only)
        glBegin(GL_LINES)
        # Left side of the right rectangle
        glVertex2f(rect_top_right_x, rect_top_y)
        glVertex2f(rect_top_right_x, rect_top_y + rect_top_height)
        # Right side of the right rectangle
        glVertex2f(rect_top_right_x + rect_top_width, rect_top_y)
        glVertex2f(rect_top_right_x + rect_top_width, rect_top_y + rect_top_height)
        glEnd()

        # Draw two small half circles on top of the two smaller squares
        glColor3f(1.0, 0.843, 0.0)  # Gold color
        half_circle_radius = square_width / 2 + 3 # Radius of the half circles

        # Calculate the center coordinates for the left half circle
        half_circle_left_center_x = square_left_x + square_width / 2 - 0.5
        half_circle_left_center_y = square_y + square_height - 26

        # Calculate the center coordinates for the right half circle
        half_circle_right_center_x = square_right_x + square_width / 2 - 0.5
        half_circle_right_center_y = square_y + square_height - 26

        num_segments = 50  # Number of segments to approximate the half circles
        
        # Draw the left half circle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(half_circle_left_center_x, half_circle_left_center_y)  # Center of the left half circle
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            glVertex2f(half_circle_left_center_x + half_circle_radius * cos(angle),
                       half_circle_left_center_y - half_circle_radius * sin(angle))  # Negative sin to flip orientation
        glEnd()

        # Draw the right half circle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(half_circle_right_center_x, half_circle_right_center_y)  # Center of the right half circle
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            glVertex2f(half_circle_right_center_x + half_circle_radius * cos(angle),
                       half_circle_right_center_y - half_circle_radius * sin(angle))  # Negative sin to flip orientation
        glEnd()
        
        # Draw black outlines for the half circles (top only)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_STRIP)
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            glVertex2f(half_circle_left_center_x + half_circle_radius * cos(angle),
                    half_circle_left_center_y - half_circle_radius * sin(angle))  # Negative sin to flip orientation
        glEnd()

        glBegin(GL_LINE_STRIP)
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            glVertex2f(half_circle_right_center_x + half_circle_radius * cos(angle),
                    half_circle_right_center_y - half_circle_radius * sin(angle))  # Negative sin to flip orientation
        glEnd()
        
    def draw_trapezium(self):
        # Define trapezium vertices with customized width and height
        bottom_left_x = self.width() / 2 - 85  # Adjust the x-coordinate of bottom left vertex
        bottom_right_x = self.width() / 2 + 85  # Adjust the x-coordinate of bottom right vertex
        top_left_x = self.width() / 2 - 124  # Adjust the x-coordinate of top left vertex
        top_right_x = self.width() / 2 + 124  # Adjust the x-coordinate of top right vertex
        bottom_y =  500 # Adjust the y-coordinate of bottom vertices
        top_y = self.height() - 0.5  # Adjust the y-coordinate of top vertices (inverted)

        trapezium_vertices = [
            (bottom_left_x, bottom_y),        # Bottom left
            (bottom_right_x, bottom_y),       # Bottom right
            (top_right_x, top_y),             # Top right
            (top_left_x, top_y)               # Top left
        ]

        # Draw trapezium
        glColor3f(0.8, 0.8, 0.8)  # Light gray color
        glBegin(GL_QUADS)
        for vertex in trapezium_vertices:
            glVertex2f(vertex[0], vertex[1])
        glEnd()

        # Draw black outline for the trapezium
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        for vertex in trapezium_vertices:
            glVertex2f(vertex[0], vertex[1])
        glEnd()

    # Draw clouds
    def draw_cloud(self, vertices):
        num_circles = len(vertices)

        # Define colors for gradient
        top_color = (1.0, 1.0, 1.0)  # Light gray color for the top of the cloud
        bottom_color = (0.8,0.8,0.8)  # White color for the bottom of the cloud

        # Find the minimum and maximum y-coordinate values
        min_y = min(vertex[1] for vertex in vertices)
        max_y = max(vertex[1] for vertex in vertices)

        for vertex in vertices:
            x, y = vertex
            glBegin(GL_TRIANGLE_FAN)

            # Draw gradient for each circle
            for j in range(360):
                angle = radians(j)
                # Normalize the y-coordinate inversely
                normalized_y = 1.0 - (y - min_y) / (max_y - min_y)
                # Interpolate colors for gradient
                glColor3f(top_color[0] + (bottom_color[0] - top_color[0]) * normalized_y,
                        top_color[1] + (bottom_color[1] - top_color[1]) * normalized_y,
                        top_color[2] + (bottom_color[2] - top_color[2]) * normalized_y)
                glVertex2f(x + 40 * cos(angle), y + 20 * sin(angle))  # Adjust circle parameters accordingly
            glEnd()

    def draw_cancelor_hall(self):
     #----------------------------   4 triangle mount --------------------------------------------------------------------------------------
        # Define vertices coordinates
        top_x = 210
        top_y = 15
        bottom_left_x = -500
        bottom_left_y = 1200
        bottom_right_x = 1890
        bottom_right_y = 1000

        # Dark green color
        glColor3f(0.0, 0.05, 0.0)  
        glBegin(GL_TRIANGLES)
        glVertex2f(top_x, top_y)  
        glVertex2f(bottom_left_x, bottom_left_y)  
        glVertex2f(bottom_right_x, bottom_right_y)  
        glEnd()

        # Define colors for gradient
        top_color = (0.0, 0.05, 0.0)  # Darker green
        bottom_color = (0.0, 0.45, 0.0)  # Lighter green

        # Draw gradient hill 1
        glBegin(GL_TRIANGLES)
        glColor3f(top_color[0], top_color[1], top_color[2])  # Top color
        glVertex2f(600, 20)  

        glColor3f(bottom_color[0], bottom_color[1], bottom_color[2])  # Bottom-left color
        glVertex2f(-200, 600)  

        glColor3f(bottom_color[0], bottom_color[1], bottom_color[2])  # Bottom-right color
        glVertex2f(1400, 600)  
        glEnd()

        # Draw gradient hill 2
        glBegin(GL_TRIANGLES)
        glColor3f(top_color[0], top_color[1], top_color[2])  # Top color
        glVertex2f(235, 30)  

        glColor3f(bottom_color[0], bottom_color[1], bottom_color[2])  # Bottom-left color
        glVertex2f(-500, 500)  

        glColor3f(bottom_color[0], bottom_color[1], bottom_color[2])  # Bottom-right color
        glVertex2f(1000, 500)  
        glEnd()
        
        # Adjusted dimensions and position of the Cancelor Hall art
        cancelor_hall_width = 600  
        cancelor_hall_height = 200  
        cancelor_hall_x = (self.width() - cancelor_hall_width) / 2 
        cancelor_hall_y = self.height() * 0.4 

        # Calculate center_x and center_y before using them
        center_x = cancelor_hall_x + cancelor_hall_width / 2
        center_y = cancelor_hall_y - 2  # Placed directly above the rectangle

        # Draw the main rectangle of the Cancelor Hall
        glColor4f(1.0, 0.95, 0.7, 1.0)  # Yellowish-white color (R: 1.0, G: 0.95, B: 0.7, A: 1.0)
        glBegin(GL_QUADS)
        glVertex2f(cancelor_hall_x, cancelor_hall_y)
        glVertex2f(cancelor_hall_x + cancelor_hall_width, cancelor_hall_y)
        glVertex2f(cancelor_hall_x + cancelor_hall_width, cancelor_hall_y + cancelor_hall_height)
        glVertex2f(cancelor_hall_x, cancelor_hall_y + cancelor_hall_height)
        glEnd()

        # Draw the outline for the Cancelor Hall rectangle (left, right, and bottom edges only)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINES)
        glVertex2f(cancelor_hall_x, cancelor_hall_y)
        glVertex2f(cancelor_hall_x, cancelor_hall_y + cancelor_hall_height)  # Left edge
        glVertex2f(cancelor_hall_x + cancelor_hall_width, cancelor_hall_y)
        glVertex2f(cancelor_hall_x + cancelor_hall_width, cancelor_hall_y + cancelor_hall_height)  # Right edge
        glVertex2f(cancelor_hall_x, cancelor_hall_y + cancelor_hall_height)
        glVertex2f(cancelor_hall_x + cancelor_hall_width, cancelor_hall_y + cancelor_hall_height)  # Bottom edge
        glEnd()

        # Draw the curved top edge of the rectangle
        glColor3f(0.8, 0.8, 0.8)  # Light gray color
        curve_width = 290  # Adjust the width of the curve
        curve_height = 10  # Desired height of the curve
        num_segments = 100
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(center_x, center_y)
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            x = center_x + curve_width * cos(angle)
            y = center_y - curve_height * sin(angle)  # Use a fixed height for y-coordinate
            glVertex2f(x, y)
        glEnd()

        # Draw the outline for the top of the half circle
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            glVertex2f(center_x + curve_width * cos(angle), center_y - curve_height * sin(angle))
        glEnd()
        
        
        #----------------------------  left small rectangles --------------------------------------------------------------------------------------
        
        # Draw the small rectangle at the top of the curved line
        glColor3f(0.9, 0.6, 0.4)  # Darker peach color
        small_rect_width = 20  # Adjust the width of the small rectangle
        small_rect_height = 75  # Adjust the height of the small rectangle

        # Number of rectangles on each side
        num_rectangles = 3

        # Define the spacing between rectangles
        spacing = -90  # Adjust the spacing as needed

        # Define the tilt angle of the sides
        tilt_angle = 30  # Adjust the tilt angle as needed

        # Draw rectangles on the left side of the Cancelor Hall
        small_rect_y = center_y - curve_height - small_rect_height + 120  # Initialize small_rect_y here
        for i in range(num_rectangles):
            # Calculate initial position only for the leftmost rectangle
            if i == 0:
                small_rect_x_left = cancelor_hall_x - small_rect_width + 25
            else:
                # For subsequent rectangles, add the spacing to the x-coordinate
                small_rect_x_left -= small_rect_width + spacing

            # Calculate the X-coordinate for the tilt position
            tilt_x = small_rect_x_left + small_rect_width - 5  # Adjust the tilt position here

            # Draw filled rectangle
            glBegin(GL_QUADS)
            glVertex2f(small_rect_x_left, small_rect_y)
            glVertex2f(small_rect_x_left + small_rect_width, small_rect_y)
            glVertex2f(tilt_x, small_rect_y - small_rect_height)
            
            # Lower the first left corner
            if i == 0:
                glVertex2f(small_rect_x_left - 15, small_rect_y - small_rect_height - 10)  # Adjusted Y-coordinate for the lower corner
            else:
                glVertex2f(small_rect_x_left - 15, small_rect_y - small_rect_height)  # Adjusted Y-coordinate for the other corners
            
            glEnd()
            
        #----------------------------  right small rectangles --------------------------------------------------------------------------------------
       
        # Draw rectangles on the right side of the Cancelor Hall
        for i in range(num_rectangles):
            small_rect_x_right = cancelor_hall_x + cancelor_hall_width - 150 + small_rect_width * i + 40 * i + (2 * i)  # Adjusted X-coordinate for the right side
            small_rect_y = center_y - curve_height - small_rect_height + 120  # Initialize small_rect_y here

            # Calculate the X-coordinate for the tilt position
            tilt_x_right = small_rect_x_right + small_rect_width + 5  # Adjust the tilt position here

            # Draw filled rectangle
            glBegin(GL_QUADS)
            glVertex2f(small_rect_x_right, small_rect_y)
            glVertex2f(small_rect_x_right + small_rect_width, small_rect_y)
            glVertex2f(tilt_x_right, small_rect_y - small_rect_height)

            # Lower the first right corner
            if i == 0:
                glVertex2f(tilt_x_right - 15, small_rect_y - small_rect_height - 10)  # Adjusted Y-coordinate for the lower corner
            else:
                glVertex2f(tilt_x_right - 15, small_rect_y - small_rect_height)  # Adjusted Y-coordinate for the other corners
            glEnd()

        # Draw outline for all rectangles
        glColor3f(0.0, 0.0, 0.0)  # Black color
        for i in range(num_rectangles):
            small_rect_x_right = cancelor_hall_x + cancelor_hall_width - 150 + small_rect_width * i + 40 * i + (2 * i)
            small_rect_y = center_y - curve_height - small_rect_height + 120
            tilt_x_right = small_rect_x_right + small_rect_width + 5

            glBegin(GL_LINE_LOOP)
            glVertex2f(small_rect_x_right, small_rect_y)
            glVertex2f(small_rect_x_right + small_rect_width, small_rect_y)
            glVertex2f(tilt_x_right, small_rect_y - small_rect_height)
            if i == 0:
                glVertex2f(tilt_x_right - 15, small_rect_y - small_rect_height - 10)
            else:
                glVertex2f(tilt_x_right - 15, small_rect_y - small_rect_height)
            glEnd()
        
        #----------------------------  longer rectangle --------------------------------------------------------------------------------------    
      
        # Adjust the dimensions and position as needed
        large_rect_width = 620  # Adjusted width of the larger rectangle
        large_rect_height = 200  # Adjusted height of the larger rectangle
        large_rect_x = (self.width() - large_rect_width) / 2  # Adjusted X-coordinate for the larger rectangle
        large_rect_y = cancelor_hall_y - large_rect_height + 200  # Adjusted Y-coordinate for the larger rectangle

        # Draw the larger rectangle with gradient from darker to lighter yellowish-white
        glBegin(GL_QUADS)
        for i in range(10):  # Split into 10 segments for gradient effect
            glColor4f(1.0, 0.95 - (9 - i) * 0.02, 0.7 - (10 - i) * 0.03, 1.0)  # Darker color towards the top
            glVertex2f(large_rect_x, large_rect_y + i * (large_rect_height / 10))  # Adjust y-coordinate here
            glVertex2f(large_rect_x + large_rect_width, large_rect_y + i * (large_rect_height / 10))  # Adjust y-coordinate here
            glColor4f(1.0, 0.95 - (10 - i) * 0.02, 0.7 - (10 - i) * 0.03, 1.0)  # Lighter color towards the bottom
            glVertex2f(large_rect_x + large_rect_width, large_rect_y + (i + 1) * (large_rect_height / 10))  # Adjust y-coordinate here
            glVertex2f(large_rect_x, large_rect_y + (i + 1) * (large_rect_height / 10))  # Adjust y-coordinate here
        glEnd()

        # Draw the outline for the larger rectangle (left, right, and bottom edges only)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINES)
        glVertex2f(large_rect_x, large_rect_y)
        glVertex2f(large_rect_x, large_rect_y + large_rect_height)  # Left edge
        glVertex2f(large_rect_x + large_rect_width, large_rect_y)
        glVertex2f(large_rect_x + large_rect_width, large_rect_y + large_rect_height)  # Right edge
        glVertex2f(large_rect_x, large_rect_y + large_rect_height)
        glVertex2f(large_rect_x + large_rect_width, large_rect_y + large_rect_height)  # Bottom edge
        glEnd()
        
        # Draw the curved top edge of the rectangle
        glColor4f(1.0, 0.95, 0.7, 1.0)  # Yellowish-white color (R: 1.0, G: 0.95, B: 0.7, A: 1.0)
        curve_width = 620  # Use the same width as the other curve
        curve_height = 20  # Use the same height as the other curve
        center_x = cancelor_hall_x + cancelor_hall_width / 2
        center_y = cancelor_hall_y + 2  # Placed directly above the rectangle
        num_segments = 100
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(center_x, center_y)
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            x = center_x + curve_width / 2 * cos(angle)  # Adjusted calculation for x-coordinate
            y = center_y - curve_height * sin(angle)  # Use a fixed height for y-coordinate
            glVertex2f(x, y)
        glEnd()
        
       #----------------------------  bottom rectangle --------------------------------------------------------------------------------------

        # Adjusted width of the short rectangle
        short_rect_width = 620  # Adjust the width as needed

        glColor4f(1.0, 0.95, 0.7, 1.0)  # Yellowish-white color (R: 1.0, G: 0.95, B: 0.7, A: 1.0)

        # Draw the bottom rectangle above the small rectangles
        short_rect_height = 25  # Adjusted height of the bottom rectangle
        short_rect_x = cancelor_hall_x + (cancelor_hall_width - short_rect_width) / 2  # Adjusted X-coordinate for centering
        short_rect_y = cancelor_hall_y - short_rect_height + 10  # Y-coordinate of the short rectangle's top-left corner, adjusted upwards

        # Tilt angle for the sides of the bottom rectangle
        tilt_angle = 15  # Angle of tilt for the sides (in degrees)
        tilt_radians = radians(tilt_angle)  # Convert angle to radians

        # Calculate the tilt offsets for the left and right sides
        left_tilt_offset = short_rect_height * sin(tilt_radians)
        right_tilt_offset = short_rect_height * sin(tilt_radians)

        # Draw the filled bottom rectangle
        glBegin(GL_QUADS)
        # Top-left vertex
        glVertex2f(short_rect_x - left_tilt_offset, short_rect_y)
        # Top-right vertex
        glVertex2f(short_rect_x + short_rect_width + right_tilt_offset, short_rect_y)
        # Bottom-right vertex
        glVertex2f(short_rect_x + short_rect_width, short_rect_y + short_rect_height)
        # Bottom-left vertex
        glVertex2f(short_rect_x, short_rect_y + short_rect_height)
        glEnd()

       # Draw the outline for the bottom rectangle (including bottom and side edges only)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINES)
        # Bottom side
        glVertex2f(short_rect_x, short_rect_y + short_rect_height)
        glVertex2f(short_rect_x + short_rect_width, short_rect_y + short_rect_height)
        # Left side
        glVertex2f(short_rect_x, short_rect_y + short_rect_height)
        glVertex2f(short_rect_x - left_tilt_offset, short_rect_y)
        # Right side
        glVertex2f(short_rect_x + short_rect_width, short_rect_y + short_rect_height)
        glVertex2f(short_rect_x + short_rect_width + right_tilt_offset, short_rect_y)
        glEnd()
        
        # Draw the curved top edge of the rectangle
        glColor4f(1.0, 0.95, 0.7, 1.0)  # Yellowish-white color (R: 1.0, G: 0.95, B: 0.7, A: 1.0)
        curve_width = 635  # Use the same width as the other curve
        curve_height = 5  # Use the same height as the other curve
        center_x = cancelor_hall_x + cancelor_hall_width / 2
        center_y = cancelor_hall_y - 12  # Placed directly above the rectangle
        num_segments = 210  # Increased number of segments for smoother curve
        glBegin(GL_LINE_LOOP)  # Use GL_LINE_LOOP to ensure a continuous outline
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            x = center_x + curve_width / 2 * cos(angle)  # Adjusted calculation for x-coordinate
            y = center_y - curve_height * sin(angle)  # Use a fixed height for y-coordinate
            glVertex2f(x, y)
        glEnd()
        
        # Draw the outline for the curved top edge (use GL_LINE_LOOP for a continuous outline)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINES)
        for i in range(num_segments):
            angle = i * (pi / num_segments)
            next_angle = (i + 1) * (pi / num_segments)
            x1 = center_x + curve_width / 2 * cos(angle)
            y1 = center_y - curve_height * sin(angle)
            x2 = center_x + curve_width / 2 * cos(next_angle)
            y2 = center_y - curve_height * sin(next_angle)
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
        glEnd()

        #----------------------------  short long rectangle --------------------------------------------------------------------------------------
        # Set the color to darker peach
        glColor3f(0.9, 0.6, 0.4)  # Darker peach color

        # Adjusted width of the short rectangle
        long_trapezium_width = 620  # Adjust the width as needed

        # Draw the short rectangle above the small rectangles
        long_trapezium_height = 30  # Adjusted height of the short rectangle
        long_trapezium_x = cancelor_hall_x + (cancelor_hall_width - long_trapezium_width) / 2  # Adjusted X-coordinate for centering
        long_trapezium_y = cancelor_hall_y - long_trapezium_height - 30  # Y-coordinate of the short rectangle's top-left corner, adjusted upwards

        # Tilt angle for the sides of the short rectangle
        tilt_angle = 15  # Angle of tilt for the sides (in degrees)
        tilt_radians = radians(tilt_angle)  # Convert angle to radians

        # Calculate the tilt offsets for the left and right sides
        left_tilt_offset = long_trapezium_height * sin(tilt_radians)
        right_tilt_offset = long_trapezium_height * sin(tilt_radians)

        # Draw the filled short rectangle
        glBegin(GL_QUADS)
        # Top-left vertex
        glVertex2f(long_trapezium_x - left_tilt_offset, long_trapezium_y)
        # Top-right vertex
        glVertex2f(long_trapezium_x + long_trapezium_width + right_tilt_offset, long_trapezium_y)
        # Bottom-right vertex
        glVertex2f(long_trapezium_x + long_trapezium_width, long_trapezium_y + long_trapezium_height)
        # Bottom-left vertex
        glVertex2f(long_trapezium_x, long_trapezium_y + long_trapezium_height)
        glEnd()
        
        # Draw the outline for the trapezium (black color)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        # Top-left vertex
        glVertex2f(long_trapezium_x - left_tilt_offset, long_trapezium_y)
        # Top-right vertex
        glVertex2f(long_trapezium_x + long_trapezium_width + right_tilt_offset, long_trapezium_y)
        # Bottom-right vertex
        glVertex2f(long_trapezium_x + long_trapezium_width, long_trapezium_y + long_trapezium_height)
        # Bottom-left vertex
        glVertex2f(long_trapezium_x, long_trapezium_y + long_trapezium_height)
        glEnd()

        #----------------------------  cancelor dome --------------------------------------------------------------------------------------

       # Adjust the height and width separately
        dome_radius_x = 220  # Adjust the radius in the x-direction (width)
        dome_radius_y = 100  # Adjust the radius in the y-direction (height)

        dome_center_x = cancelor_hall_x + cancelor_hall_width / 2
        dome_center_y = cancelor_hall_y - short_rect_height - 35

        # Draw the dome behind the short rectangle with light peach color
        glColor3f(1.0, 0.8, 0.6)  # Light peach color
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(dome_center_x, dome_center_y)
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            x = dome_center_x + dome_radius_x * cos(angle)
            y = dome_center_y - dome_radius_y * sin(angle)  # Flip the sign of y-coordinate to flip the dome
            glVertex2f(x, y)
        glEnd()

        # Draw the dome outline
        glColor3f(0.0, 0.0, 0.0)  # Black color for the outline
        glBegin(GL_LINE_LOOP)
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            x = dome_center_x + (dome_radius_x + 2) * cos(angle)  # Adding 2 to radius for the outline
            y = dome_center_y - (dome_radius_y + 2) * sin(angle)  # Adding 2 to radius for the outline
            glVertex2f(x, y)
        glEnd()

        # Draw the short rectangle above the dome
        glColor4f(1.0, 0.95, 0.7, 1.0)  # Yellowish-white color (R: 1.0, G: 0.95, B: 0.7, A: 1.0)
        glBegin(GL_QUADS)
        glVertex2f(short_rect_x - left_tilt_offset, short_rect_y)
        glVertex2f(short_rect_x + short_rect_width + right_tilt_offset, short_rect_y)
        glVertex2f(short_rect_x + short_rect_width, short_rect_y + short_rect_height)
        glVertex2f(short_rect_x, short_rect_y + short_rect_height)
        glEnd()

        # Draw the black outline around the short rectangle
        glColor3f(0.0, 0.0, 0.0)  # Black color for the outline
        glBegin(GL_LINE_LOOP)
        glVertex2f(short_rect_x - left_tilt_offset - 1, short_rect_y - 1)  # Slightly larger than the original rectangle
        glVertex2f(short_rect_x + short_rect_width + right_tilt_offset + 1, short_rect_y - 1)  # Slightly larger than the original rectangle
        glVertex2f(short_rect_x + short_rect_width + 1, short_rect_y + short_rect_height + 1)  # Slightly larger than the original rectangle
        glVertex2f(short_rect_x - 1, short_rect_y + short_rect_height + 1)  # Slightly larger than the original rectangle
        glEnd()
        
        # Adjusted dimensions and position of the smaller rectangle
        smaller_rect_width = 350  
        smaller_rect_height = 210  
        smaller_rect_x = (self.width() - smaller_rect_width) / 2 
        smaller_rect_y = self.height() * 0.4 + 80  # Slightly above the main rectangle

        # Draw the smaller rectangle
        glColor4f(1.0, 0.95, 0.7, 1.0)  # Yellowish-white color (R: 1.0, G: 0.95, B: 0.7, A: 1.0)
        glBegin(GL_QUADS)
        glVertex2f(smaller_rect_x, smaller_rect_y)
        glVertex2f(smaller_rect_x + smaller_rect_width, smaller_rect_y)
        glVertex2f(smaller_rect_x + smaller_rect_width, smaller_rect_y + smaller_rect_height)
        glVertex2f(smaller_rect_x, smaller_rect_y + smaller_rect_height)
        glEnd()

        # Draw the outline for the smaller rectangle
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINES)
        glVertex2f(smaller_rect_x, smaller_rect_y)
        glVertex2f(smaller_rect_x, smaller_rect_y + smaller_rect_height)  # Left edge
        glVertex2f(smaller_rect_x + smaller_rect_width, smaller_rect_y)
        glVertex2f(smaller_rect_x + smaller_rect_width, smaller_rect_y + smaller_rect_height)  # Right edge
        glVertex2f(smaller_rect_x, smaller_rect_y + smaller_rect_height)
        glVertex2f(smaller_rect_x + smaller_rect_width, smaller_rect_y + smaller_rect_height)  # Bottom edge
        glEnd()
        
        #---------------------------------------------------------

        # Adjusted dimensions and position of the left long shorter rectangle
        left_long_shorter_rect_width = 40  
        left_long_shorter_rect_height = 200 

        # Adjusting x position to move the left long shorter rectangle to the left
        left_long_shorter_rect_x = smaller_rect_x - left_long_shorter_rect_width + 40  # Move 50 units to the left

        # Adjusting y position to move the left long shorter rectangle up
        left_long_shorter_rect_y = smaller_rect_y - left_long_shorter_rect_height + 150  # Move 50 units up

        # Draw the left long shorter rectangle
        glColor3f(0.9, 0.6, 0.4)  # Darker peach color
        glBegin(GL_QUADS)
        glVertex2f(left_long_shorter_rect_x, left_long_shorter_rect_y)
        glVertex2f(left_long_shorter_rect_x + left_long_shorter_rect_width, left_long_shorter_rect_y)
        glVertex2f(left_long_shorter_rect_x + left_long_shorter_rect_width, left_long_shorter_rect_y + left_long_shorter_rect_height)
        glVertex2f(left_long_shorter_rect_x, left_long_shorter_rect_y + left_long_shorter_rect_height)
        glEnd()
        
        # Draw the outline for the left long shorter rectangle (black color)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        glVertex2f(left_long_shorter_rect_x, left_long_shorter_rect_y)
        glVertex2f(left_long_shorter_rect_x + left_long_shorter_rect_width, left_long_shorter_rect_y)
        glVertex2f(left_long_shorter_rect_x + left_long_shorter_rect_width, left_long_shorter_rect_y + left_long_shorter_rect_height)
        glVertex2f(left_long_shorter_rect_x, left_long_shorter_rect_y + left_long_shorter_rect_height)
        glEnd()

        # Adjusted dimensions and position of the right long shorter rectangle
        right_long_shorter_rect_width = 40  
        right_long_shorter_rect_height = 200  

        # Adjusting x position to move the right long shorter rectangle to the right
        right_long_shorter_rect_x = smaller_rect_x + smaller_rect_width - 40  # Move 50 units to the right

        # Adjusting y position to move the right long shorter rectangle down
        right_long_shorter_rect_y = smaller_rect_y - right_long_shorter_rect_height + 150  # Move 50 units down

        # Draw the right long shorter rectangle
        glColor3f(0.9, 0.6, 0.4)  # Darker peach color
        glBegin(GL_QUADS)
        glVertex2f(right_long_shorter_rect_x, right_long_shorter_rect_y)
        glVertex2f(right_long_shorter_rect_x + right_long_shorter_rect_width, right_long_shorter_rect_y)
        glVertex2f(right_long_shorter_rect_x + right_long_shorter_rect_width, right_long_shorter_rect_y + right_long_shorter_rect_height)
        glVertex2f(right_long_shorter_rect_x, right_long_shorter_rect_y + right_long_shorter_rect_height)
        glEnd()
        
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        glVertex2f(right_long_shorter_rect_x, right_long_shorter_rect_y)
        glVertex2f(right_long_shorter_rect_x + right_long_shorter_rect_width, right_long_shorter_rect_y)
        glVertex2f(right_long_shorter_rect_x + right_long_shorter_rect_width, right_long_shorter_rect_y + right_long_shorter_rect_height)
        glVertex2f(right_long_shorter_rect_x, right_long_shorter_rect_y + right_long_shorter_rect_height)
        glEnd()
        
        #-------------------------------------- windows left ---------------------------------------------------------------
        # Adjusted dimensions and position of the windows
        windows_width = 70  
        windows_height = 80  
        windows_x = (self.width() - windows_width) / 2 - 230 
        windows_y = self.height() * 0.2 + 180  # Adjusted y-position to be above the rectangle

        # Draw the windows rectangle
        glColor3f(0.0, 0.0, 0.2)  # White color
        glBegin(GL_QUADS)
        glVertex2f(windows_x, windows_y)
        glVertex2f(windows_x + windows_width, windows_y)
        glVertex2f(windows_x + windows_width, windows_y + windows_height)
        glVertex2f(windows_x, windows_y + windows_height)
        glEnd()

        # Draw the outline for the windows rectangle (black color)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        glVertex2f(windows_x, windows_y)
        glVertex2f(windows_x + windows_width, windows_y)
        glVertex2f(windows_x + windows_width, windows_y + windows_height)
        glVertex2f(windows_x, windows_y + windows_height)
        glEnd()

        #-------------------------------------- half circle above the windows --------------------------------------------------
        # Define the center coordinates of the half circle
        half_circle_center_x = windows_x + windows_width / 2
        half_circle_center_y = windows_y + windows_height + windows_width / 2 - 115  # Adjusted y-coordinate

        # Define the radius and number of segments for the half circle
        half_circle_radius = windows_width / 2
        num_segments = 100

        # Draw the filled half circle above the rectangle (flipped upside down)
        glColor3f(0.0, 0.0, 0.2)  # White color
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(half_circle_center_x, half_circle_center_y)  # Center point
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            x = half_circle_center_x + half_circle_radius * cos(angle)
            y = half_circle_center_y - half_circle_radius * sin(angle)  # Inverted sin to flip upside down
            glVertex2f(x, y)
        glEnd()
        
        # Draw the outline for the half circle (black color)
        glColor3f(0.0, 0.0, 0.2)  # Black color
        glBegin(GL_LINE_LOOP)
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            x = half_circle_center_x + half_circle_radius * cos(angle)
            y = half_circle_center_y - half_circle_radius * sin(angle)  # Inverted sin to flip upside down
            glVertex2f(x, y)
        glEnd()
        
        #-------------------------------------- windows right ---------------------------------------------------------------
        # Adjusted dimensions and position of the windows right
        windows_right_width = 70  
        windows_right_height = 80  
        windows_right_x = (self.width() - windows_right_width) / 2 + 230  # Adjusted x-position to be on the right-hand side
        windows_right_y = self.height() * 0.2 + 180  # Adjusted y-position to be above the rectangle

        # Draw the windows right rectangle
        glColor3f(0.0, 0.0, 0.2)  # White color
        glBegin(GL_QUADS)
        glVertex2f(windows_right_x, windows_right_y)
        glVertex2f(windows_right_x + windows_right_width, windows_right_y)
        glVertex2f(windows_right_x + windows_right_width, windows_right_y + windows_right_height)
        glVertex2f(windows_right_x, windows_right_y + windows_right_height)
        glEnd()

        # Draw the outline for the windows right rectangle (black color)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        glVertex2f(windows_right_x, windows_right_y)
        glVertex2f(windows_right_x + windows_right_width, windows_right_y)
        glVertex2f(windows_right_x + windows_right_width, windows_right_y + windows_right_height)
        glVertex2f(windows_right_x, windows_right_y + windows_right_height)
        glEnd()

        #-------------------------------------- half circle above the windows right --------------------------------------------------
        # Define the center coordinates of the half circle right
        half_circle_right_center_x = windows_right_x + windows_right_width / 2
        half_circle_right_center_y = windows_right_y + windows_right_height + windows_right_width / 2 - 115  # Adjusted y-coordinate

        # Define the radius and number of segments for the half circle right
        half_circle_right_radius = windows_right_width / 2

        # Draw the filled half circle above the rectangle right (flipped upside down)
        glColor3f(0.0, 0.0, 0.2)  # White color
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(half_circle_right_center_x, half_circle_right_center_y)  # Center point
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            x = half_circle_right_center_x + half_circle_right_radius * cos(angle)
            y = half_circle_right_center_y - half_circle_right_radius * sin(angle)  # Inverted sin to flip upside down
            glVertex2f(x, y)
        glEnd()

        # Draw the outline for the half circle right (black color)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        for i in range(num_segments + 1):
            angle = i * (pi / num_segments)
            x = half_circle_right_center_x + half_circle_right_radius * cos(angle)
            y = half_circle_right_center_y - half_circle_right_radius * sin(angle)  # Inverted sin to flip upside down
            glVertex2f(x, y)
        glEnd()
        
    # Function to draw the smaller shorter rectangle with text
    def draw_smaller_shorter_rect_with_text(self):
        # Adjusted dimensions and position of the smaller shorter rectangle
        smaller_shorter_rect_width = 350  
        smaller_shorter_rect_height = 40 
        smaller_shorter_rect_x = (self.width() - smaller_shorter_rect_width) / 2 
        smaller_shorter_rect_y = self.height() * 0.4 - 20  # Slightly above the main rectangle

        # Draw the smaller shorter rectangle
        glColor3f(1, 1, 1)  # White color
        glBegin(GL_QUADS)
        glVertex2f(smaller_shorter_rect_x, smaller_shorter_rect_y)
        glVertex2f(smaller_shorter_rect_x + smaller_shorter_rect_width, smaller_shorter_rect_y)
        glVertex2f(smaller_shorter_rect_x + smaller_shorter_rect_width, smaller_shorter_rect_y + smaller_shorter_rect_height)
        glVertex2f(smaller_shorter_rect_x, smaller_shorter_rect_y + smaller_shorter_rect_height)
        glEnd()

        # Draw the outline for the smaller shorter rectangle (black color)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        glVertex2f(smaller_shorter_rect_x, smaller_shorter_rect_y)
        glVertex2f(smaller_shorter_rect_x + smaller_shorter_rect_width, smaller_shorter_rect_y)
        glVertex2f(smaller_shorter_rect_x + smaller_shorter_rect_width, smaller_shorter_rect_y + smaller_shorter_rect_height)
        glVertex2f(smaller_shorter_rect_x, smaller_shorter_rect_y + smaller_shorter_rect_height)
        glEnd()

        # Draw text within the smaller shorter rectangle
        glColor3f(0.0, 0.0, 0.0)  # Black color for text
        text = "DEWAN                         CANSELOR"  # Text to display
        text_x = smaller_shorter_rect_x + 30  # Adjust x-position for centering
        text_y = smaller_shorter_rect_y + 23  # Adjust y-position for centering
        self.draw_text(text, text_x, text_y)  # Use self.draw_text instead of draw_text

        # Draw the second smaller shorter rectangle below the first one
        glColor3f(1, 1, 1)  # White color
        text_wall_y = smaller_shorter_rect_y + 30  # Adjust y-coordinate for the second rectangle
        glBegin(GL_QUADS)
        glVertex2f(smaller_shorter_rect_x, text_wall_y)
        glVertex2f(smaller_shorter_rect_x + smaller_shorter_rect_width, text_wall_y)
        glVertex2f(smaller_shorter_rect_x + smaller_shorter_rect_width, text_wall_y + smaller_shorter_rect_height)
        glVertex2f(smaller_shorter_rect_x, text_wall_y + smaller_shorter_rect_height)
        glEnd()
        
        # Draw the outline for the second smaller shorter rectangle (black color)
        glColor3f(0.0, 0.0, 0.0)  # Black color for text
        glBegin(GL_LINE_LOOP)
        glVertex2f(smaller_shorter_rect_x, text_wall_y)
        glVertex2f(smaller_shorter_rect_x + smaller_shorter_rect_width, text_wall_y)
        glVertex2f(smaller_shorter_rect_x + smaller_shorter_rect_width, text_wall_y + smaller_shorter_rect_height)
        glVertex2f(smaller_shorter_rect_x, text_wall_y + smaller_shorter_rect_height)
        glEnd()
        
        # Draw the second smaller shorter rectangle (door) below the text_wall
        door_width = 220  # Adjusted width for the door
        door_height = 150
        door_x = (self.width() - door_width) / 2
        door_y = smaller_shorter_rect_y + 80  # Adjusted y-coordinate below text_wall
        glColor3f(1.0, 1.0, 0.5)  # White color
        glBegin(GL_QUADS)
        glVertex2f(door_x, door_y)
        glVertex2f(door_x + door_width, door_y)
        glVertex2f(door_x + door_width, door_y + door_height)
        glVertex2f(door_x, door_y + door_height)
        glEnd()

        # Draw the outline for the door (black color)
        glColor3f(0.0, 0.0, 0.0)  # Black color
        glBegin(GL_LINE_LOOP)
        glVertex2f(door_x, door_y)
        glVertex2f(door_x + door_width, door_y)
        glVertex2f(door_x + door_width, door_y + door_height)
        glVertex2f(door_x, door_y + door_height)
        glEnd()
     
    def draw_clock(self):
        # Define clock position
        clock_center_x = self.width() / 2
        clock_center_y = self.height() * 0.48  # Adjust the vertical position here

        # Draw clock face
        glColor3f(1.0, 1.0, 1.0)  # White color
        circle_radius = 60  # Radius of the main circle
        num_segments = 100  # Number of segments to approximate the circle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(clock_center_x, clock_center_y)  # Center of the clock face
        for i in range(num_segments + 1):
            angle = i * (2.0 * pi / num_segments)
            glVertex2f(clock_center_x + circle_radius * cos(angle), clock_center_y + circle_radius * sin(angle))
        glEnd()
        
        # Draw black circle ring around the clock face
        glColor3f(0.0, 0.0, 0.0)  # Black color
        ring_thickness = 2  # Adjusted thickness of the ring
        num_segments = 100  # Number of segments to approximate the circle
        for i in range(ring_thickness):
            adjusted_radius = circle_radius + i  # Adjusted radius for each ring
            glBegin(GL_LINE_LOOP)
            for j in range(num_segments + 1):
                angle = j * (2.0 * pi / num_segments)
                glVertex2f(clock_center_x + adjusted_radius * cos(angle), clock_center_y + adjusted_radius * sin(angle))
            glEnd()

         # Draw a small red dot at the center of the clock face
        glColor3f(1.0, 0.0, 0.0)  # Red color
        dot_radius = 3  # Radius of the dot
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(clock_center_x, clock_center_y)  # Center of the dot
        for i in range(num_segments + 1):
            angle = i * (2.0 * pi / num_segments)
            glVertex2f(clock_center_x + dot_radius * cos(angle), clock_center_y + dot_radius * sin(angle))
        glEnd()

        # Draw clock hours
        glColor3f(0.0, 0.0, 0.0)  # Black color for the numbers
        font = GLUT_BITMAP_TIMES_ROMAN_24  # Choose font and size
        for hour in range(1, 13):
            hour_str = str(hour)
            hour_width = glutBitmapWidth(font, ord(hour_str[0])) * len(hour_str)  # Calculate total width of the hour string
            angle = (hour - 3) * 30 * (pi / 180)  # Calculate angle for each hour
            x = clock_center_x + (circle_radius - 15) * cos(angle) - hour_width / 2 + 2  # Adjust position based on angle, text width, and offset
            y = clock_center_y + (circle_radius - 15) * sin(angle) + 9  # Adjust position based on angle and text height
            glRasterPos2f(x, y)
            for char in hour_str:
                glutBitmapCharacter(font, ctypes.c_int(ord(char)))

        # Get current Malaysian time
        malaysia_time = datetime.utcnow() + timedelta(hours=8)  # Adding 8 hours to UTC time for Malaysian time
        hour = malaysia_time.hour
        minute = malaysia_time.minute
        second = malaysia_time.second

        # Draw clock hands
        glColor3f(0.0, 0.0, 0.0)  # Black color for clock hands

        # Hour hand
        hour_angle = ((hour % 12) + minute / 60.0) * (360 / 12) * (pi / 180)
        hour_hand_length = 30
        hour_hand_width = 2

        glLineWidth(hour_hand_width)  # Set the line width for the hour hand
        glBegin(GL_LINES)
        glVertex2f(clock_center_x, clock_center_y)
        glVertex2f(clock_center_x + hour_hand_length * sin(hour_angle),
                    clock_center_y - hour_hand_length * cos(hour_angle))  # Adjusted coordinates
        glEnd()

        # Minute hand
        minute_angle = minute * (360 / 60) * (pi / 180)
        minute_hand_length = 50
        minute_hand_width = 2

        glLineWidth(minute_hand_width)  # Set the line width for the minute hand
        glBegin(GL_LINES)
        glVertex2f(clock_center_x, clock_center_y)
        glVertex2f(clock_center_x + minute_hand_length * sin(minute_angle),
                    clock_center_y - minute_hand_length * cos(minute_angle))  # Adjusted coordinates
        glEnd()

        # Restore default line width
        glLineWidth(1.0)  # or whatever your default line width should be

        # Second hand
        second_angle = second * (360 / 60) * (pi / 180)
        second_hand_length = 60
        second_hand_width = 1
        glColor3f(1.0, 0.0, 0.0)  # Red color for the second hand
        glBegin(GL_LINES)
        glVertex2f(clock_center_x, clock_center_y)
        glVertex2f(clock_center_x + second_hand_length * cos(second_angle),
                    clock_center_y + second_hand_length * sin(second_angle))
        glEnd()
    
    def draw_ums_logo(self):
        # Load image
        image = Image.open("D:/fcg2024/Tutorial/ums_logo_round.png")  # Change to the actual path of your image
        image = image.resize((image.width // 2 - 90, image.height // 2 - 90))  # Resize the image
        image_data = image.convert("RGBA").tobytes("raw", "RGBA", 0, -1)  # Change RGBA to BGRA

        # Draw image
        glRasterPos2i(368, 194)  # Adjust position as needed
        glDrawPixels(image.width, image.height, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    def draw_mcg_logo(self):
        image = Image.open("D:/fcg2024/Tutorial/umslogo.jpg")
        image = image.resize((image.width // 2, image.height // 2))
        image_data = image.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
        glRasterPos2i(int(self.mcg_logo_position_x), int(self.mcg_logo_position_y))
        glDrawPixels(image.width, image.height, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    def update_animation(self):
        current_time = datetime.now()
        time_diff = (current_time - self.last_frame_time).total_seconds()
        self.last_frame_time = current_time

        if self.animation_state == "entering":
            target_y = 900
            # Calculate the distance to move based on time elapsed
            distance = self.animation_speed * time_diff
            # Ensure we don't overshoot the target
            distance = min(distance, target_y - self.mcg_logo_position_y)
            # Update the position of the logo
            self.mcg_logo_position_y += distance

            # Check if logo position is slightly below the bottom of the window
            if self.mcg_logo_position_y > self.height() :
                # Reset logo position
                self.mcg_logo_position_y = -90

        # Always reset animation state to entering to keep the loop
        self.animation_state = "entering"        
        
    def easing_function(self, current, target, time_diff):
        # Simple linear interpolation for now, you can replace with easing functions
        return self.animation_speed * time_diff

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("MCG: The Clock Wall")
        self.glWidget = OpenGLWidget(self)
        self.glWidget.setGeometry(0, 0, 800, 600)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.glWidget.update)
        self.timer.start(10)  # Update every second

        # Add a button to toggle animation
        self.pause_button = QPushButton("Pause Animation", self)
        self.pause_button.setGeometry(20, 20, 150, 30)
        self.pause_button.clicked.connect(self.toggle_animation)

    def toggle_animation(self):
        # Toggle animation state and update button text
        self.glWidget.paused = not self.glWidget.paused
        if self.glWidget.paused:
            self.pause_button.setText("Resume Animation")
        else:
            self.pause_button.setText("Pause Animation")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())