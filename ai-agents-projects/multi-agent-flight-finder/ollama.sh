#!/bin/bash

set -e

docker run -d -v $PWD/ollama:/root/.ollama --name ollama ollama/ollama:0.11.6


ip=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'` ollama

echo "ollama 已经运行在 $ip"

sleep 3s

# 模型列表地址 https://ollama.com/search
docker exec -it ollama ollama run deepseek-r1:7b
