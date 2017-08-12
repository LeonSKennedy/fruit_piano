#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import signal
import sys
from time import sleep
import MPR121

print("""
==============================
  Fruit Piano? FRUIT PIANO!
==============================
""")

try:
  sensor = MPR121.begin()
except Exception as e:
  print e
  sys.exit(1)


# this is the touch threshold - setting it low makes it more like a proximity trigger default value is 40 for touch
touch_threshold = 40

# this is the release threshold - must ALWAYS be smaller than the touch threshold default value is 20 for touch
release_threshold = 20

# set the thresholds
sensor.set_touch_threshold(touch_threshold)
sensor.set_release_threshold(release_threshold)

# handle ctrl+c gracefully
def signal_handler(signal, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# LET THERE BE MUSIC!
pygame.init()
pygame.mixer.pre_init(44100, -16, 12, 2048)
pygame.mixer.init()
volume = 1
pygame.mixer.music.set_volume(volume)
source_folder = "synths"
channels = ["drumkit", "percussion", "synths", "farts", "funny", "piano", "animals"]
num_channels = len(channels) - 1
current_channel = 0

# LET DECISIONS HAPPEN!
def change_sounds():
    global current_channel
    next_channel = current_channel + 1

    if(next_channel > num_channels):
        next_channel = 0

    current_channel = next_channel
    print("channel: " + str(current_channel) + " / " + channels[current_channel])




try:

    while True:
      if sensor.touch_status_changed():
        sensor.update_touch_data()
        for i in range(12):

          if sensor.is_new_touch(i):

              if(i == 11):

                  change_sounds()

              else:

                  source_folder = channels[current_channel]
                  print("Sample: " + str(i))
                  song = "/home/pi/fruit_piano/sfx/" + source_folder + "/" + str(i) + ".ogg"

                  sound = pygame.mixer.Sound(song)
                  sound.play(0)

      sleep(0.1)

except KeyboardInterrupt:
    # kill the piano if the user hits ctrl+c
    print("""
==============================
FRUIT PIANO! OUT!
==============================
    """)
