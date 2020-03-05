#!/usr/bin/env python3

import sys
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
USE_SDL = True
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

# Set Agent Parameters
for idx in range(2, len(sys.argv)):
  if(sys.argv[idx]=='-a'):
    try:
      RL.alpha = float(sys.argv[idx+1])
    except ValueError:
      print("Invalid learning rate, must be a float")
  elif(sys.argv[idx]=='-g'):
    try:
      RL.gamma = float(sys.argv[idx+1])
    except:
      print("Invalid discount rate, must be a float")
  elif(sys.argv[idx]=='-e'):
    try:
        RL.epsilon = float(sys.argv[idx+1])
    except:
      print("Invalid exploration factor, must be a float")
  elif(sys.argv[idx]=='-x'):
    try:
      RL.getWeights(sys.argv[idx+1])
    except:
      print("Couldn't locate csv file with prior experience, continuing with no experience")

if(
  RL.alpha is None or
  RL.gamma is None or
  RL.epsilon is None
):
  print("Invalid or missing arguments. Usage:\n python3 agent.py -a [learning rate] -g [discount rate] -e [exploration factor] -x [prior experience file (csv)(optional)]")
  exit(0)

# Play 100 episodes
for episode in range(100):
  reward = 0
  total_reward = 0
  while not ale.game_over():
    (screen_width,screen_height) = ale.getScreenDims()
    screen_data = np.zeros(screen_width*screen_height,dtype=np.uint8)
    ale.getScreen(screen_data)

    screen = RL.convertEnv(screen_data)
    state = RL.getState(screen)

    a = RL.Q_learn(state, reward)
    if a is None:
      a = 0
    # Apply an action and get the resulting reward
    reward = ale.act(a)
    total_reward += reward
  print('Episode %d ended with score: %d' % (episode, total_reward))
  ale.reset_game()

RL.saveWeights('weights.csv')