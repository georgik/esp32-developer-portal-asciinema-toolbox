#!/bin/bash

rm -rf session.cast esp32-graphical-bootloader
asciinema rec --idle-time-limit=1 -c "./record-esp32.exp" session.cast
