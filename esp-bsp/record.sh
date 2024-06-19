#!/bin/bash

rm session.cast
rm -rf display_audio_photo
asciinema rec --idle-time-limit=1 -c "./record-esp32.exp" session.cast
