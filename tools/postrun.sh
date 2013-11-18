#!/bin/bash

ps -e -o pid,args| grep dome | head -n 1 | cut -d' ' -f1 | while read pid; do kill $pid; done
