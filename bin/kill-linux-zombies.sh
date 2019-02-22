#!/bin/bash
# Kill of any zombie processes
# only use if zombies to kill

ps axo stat,ppid,pid,comm | grep -w defunct | awk '{print $2}'| xargs kill -9
