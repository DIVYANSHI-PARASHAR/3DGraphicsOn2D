#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pygame
from pygame.locals import *
import numpy as np
import sys


# Define colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)

# Define window size and center
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
WINDOW_CENTER = np.array([WINDOW_WIDTH/2, WINDOW_HEIGHT/2])

# Initialize Pygame and set up display
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("3D Object Viewer")

# Define function to read object from file
def read_object_from_file(filename):
  with open(filename) as f:
      num_vertices, num_faces = map(int, f.readline().strip().split(','))
      vertices = []
      for i in range(num_vertices):
          vertex_data = list(map(float, f.readline().strip().split(',')))
          vertex = np.array(vertex_data[1:])
          vertices.append(vertex)
      faces = []
      for i in range(num_faces):
          face_data = list(map(int, f.readline().strip().split(',')))
          face = np.array(face_data)
          faces.append(face)
      vertices = np.array(vertices)
  return vertices, faces

# Define function to draw object
def draw_object(screen, vertices, faces):
  #vertices = np.array(vertices)
  for face in faces:
      point1 = vertices[face[0]-1]
      point2 = vertices[face[1]-1]
      point3 = vertices[face[2]-1]
      pygame.draw.line(screen, BLUE, (point1[0], point1[1]), (point2[0], point2[1]))
      pygame.draw.line(screen, BLUE, (point2[0], point2[1]), (point3[0], point3[1]))
      pygame.draw.line(screen, BLUE, (point3[0], point3[1]), (point1[0], point1[1]))
  for vertex in vertices:
      pygame.draw.circle(screen, BLUE, (int(vertex[0]), int(vertex[1])), 3)

def center_object(vertices):
  # Get the average x, y, and z values of all vertices
  avg_x = sum(v[0] for v in vertices) / len(vertices)
  avg_y = sum(v[1] for v in vertices) / len(vertices)
  avg_z = sum(v[2] for v in vertices) / len(vertices)

  # Subtract the average values from each vertex to center the object around the origin
  centered_vertices = [(v[0] - avg_x, v[1] - avg_y, v[2] - avg_z) for v in vertices]
  return centered_vertices

def main():
  # initialize pygame and create window
  vertices, faces = read_object_from_file('object.txt')
  
  # Center object around the origin
  vertices = center_object(vertices)

  # Scale object to fit screen
  vertices = np.array(vertices)
  x_range = np.max(vertices[:,0]) - np.min(vertices[:,0])
  y_range = np.max(vertices[:,1]) - np.min(vertices[:,1])
  z_range = np.max(vertices[:,2]) - np.min(vertices[:,2])
  scale_factor = min(WINDOW_WIDTH/x_range/2, WINDOW_HEIGHT/y_range/2)
  vertices[:,0:3] *= scale_factor
  vertices[:,0:2] += WINDOW_CENTER

  # Set up event loop
  clock = pygame.time.Clock()
  done = False
  rotating = False
  prev_mouse_pos = None
  while not done:
      for event in pygame.event.get():
          if event.type == QUIT:
              done = True
          elif event.type == MOUSEBUTTONDOWN:
              rotating = True
              prev_mouse_pos = np.array(pygame.mouse.get_pos())
          elif event.type == MOUSEBUTTONUP:
              rotating = False

      # Rotate object if mouse is being dragged
      if rotating:
          mouse_pos = np.array(pygame.mouse.get_pos())
          if prev_mouse_pos is not None:
              # Calculate horizontal and vertical mouse movement
              delta_x = mouse_pos[0] - prev_mouse_pos[0]
              delta_y = mouse_pos[1] - prev_mouse_pos[1]

              # Calculate rotation angles
              angle_y = np.radians(delta_x / WINDOW_WIDTH * 360)
              angle_x = np.radians(delta_y / WINDOW_HEIGHT * 360)

              # Rotate object about Y and X axes
              vertices = rotate_about_y(vertices, angle_y)
              vertices = rotate_about_x(vertices, angle_x)

              # Update prev_mouse_pos
              prev_mouse_pos = mouse_pos

      # Clear screen
      screen.fill(WHITE)

      # Draw object
      draw_object(screen, vertices, faces)

      # Update display
      pygame.display.update()

      # Control frame rate
      clock.tick(60)

  # Quit Pygame
  pygame.quit()


def rotate_about_y(vertices, angle):
  # Get the center of the object
  center = np.mean(vertices, axis=0)

  # Create rotation matrix
  rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                              [0, 1, 0],
                              [-np.sin(angle), 0, np.cos(angle)]])

  # Translate object to the origin
  vertices = vertices - center

  # Rotate object about Y axis
  vertices = np.matmul(rotation_matrix, vertices.T).T

  # Translate object back to its original position
  vertices = vertices + center

  return vertices


def rotate_about_x(vertices, angle):
  # Get the center of the object
  center = np.mean(vertices, axis=0)

  # Create rotation matrix
  rotation_matrix = np.array([[1, 0, 0],
                              [0, np.cos(angle), -np.sin(angle)],
                              [0, np.sin(angle), np.cos(angle)]])

  # Translate object to the origin
  vertices = vertices - center

  # Rotate object about X axis
  vertices = np.matmul(rotation_matrix, vertices.T).T

  # Translate object back to its original position
  vertices = vertices + center

  return vertices

if __name__ == '__main__':
  main()

