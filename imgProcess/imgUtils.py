# imgUtils.py
# Author: SFU CMPT 120
# Contains helper functions to wrap the 
# Pygame image functions

import pygame
import numpy

def getImage(filename):
  """
  Input: filename - string containing image filename to open
  Returns: 3d array, i.e. 2d array of RGB values (list)
  """
  image = pygame.image.load(filename)
  return pygame.surfarray.array3d(image).tolist()

def saveImage(pixels, filename):
  """
  Input:  pixels - 3d array, i.e. 2d array of RGB values (list)
          filename - string containing filename to save image
  Output: Saves a file with name filename, containing pixels 
  """
  nparray = numpy.asarray(pixels)
  surf = pygame.surfarray.make_surface(nparray)
  (width, height, colours) = nparray.shape
  surf = pygame.display.set_mode((width, height))
  pygame.surfarray.blit_array(surf, nparray)
  pygame.image.save(surf, filename)

def showImage(pixels):
  """
  Input:  pixels - 2d array of RGB values
  Output: show the image in a window
  """
  nparray = numpy.asarray(pixels)
  surf = pygame.surfarray.make_surface(nparray)
  (width, height, colours) = nparray.shape
  pygame.display.init()
  pygame.display.set_caption("CMPT120 - Image")
  screen = pygame.display.set_mode((width, height))
  screen.fill((225, 225, 225))
  screen.blit(surf, (0, 0))
  pygame.display.update()