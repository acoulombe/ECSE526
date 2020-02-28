#!/usr/bin/env python3

import sys
from random import randrange
from ale_py import ALEInterface
import numpy as np
import RL

if len(sys.argv) < 2:
  print('Usage: %s rom_file' % sys.argv[0])
  sys.exit()

ale = ALEInterface()

# Get & Set the desired settings
ale.setInt(b'random_seed', 0)
ale.setInt(b'frame_skip', 5)

# Set USE_SDL to true to display the screen. ALE must be compilied
# with SDL enabled for this to work. On OSX, pygame init is used to
# proxy-call SDL_main.
USE_SDL = False
if USE_SDL:
  if sys.platform == 'darwin':
    import pygame
    pygame.init()
    ale.setBool('sound', False) # Sound doesn't work on OSX
  elif sys.platform.startswith('linux'):
    ale.setBool('sound', True)
  ale.setBool('display_screen', True)

# Load the ROM file
rom_file = str.encode(sys.argv[1])
ale.loadROM(rom_file)

# Get the list of minimal actions
legal_actions = ale.getMinimalActionSet()

# Play 10 episodes
for episode in range(10):
  total_reward = 0
  while not ale.game_over():
    (screen_width,screen_height) = ale.getScreenDims()
    screen_data = np.zeros(screen_width*screen_height,dtype=np.uint8)
    ale.getScreen(screen_data)

    screen = RL.convertEnv(screen_data)
    grid = RL.getState(screen)
    for i in range(14):
      print(grid[i])
    print('')
    exit()

    a = legal_actions[randrange(len(legal_actions))]
    # Apply an action and get the resulting reward
    reward = ale.act(a)
    total_reward += reward
  print('Episode %d ended with score: %d' % (episode, total_reward))
  ale.reset_game()
