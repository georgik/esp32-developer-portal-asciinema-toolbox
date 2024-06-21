#!/bin/bash

rm -rf session.cast swift-embedded-examples
asciinema rec --idle-time-limit=1 -c "./record-esp32.exp" session.cast
