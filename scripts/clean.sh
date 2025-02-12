#!/bin/bash

# Para todos os contêineres Docker
sudo docker stop $(sudo docker ps -a -q)

# Remove todos os contêineres Docker
sudo docker rm $(sudo docker ps -a -q)

# Limpa o ambiente Mininet
sudo mn -c
