#!/bin/bash
mkdir -p logs
screen -d -m -S pandoraBot python3 pandora.py > "logs/$(date +"%Y-%m-%d_%H%M%S").log"