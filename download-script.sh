#!/bin/bash

fileid="1wD7BYASZcryGCOdu-5GGYN7Z_KnLNfRq"
filename="data/ecommerce_sessions.npy"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}


fileid="1ASvO6lo04dcoMcOKS8_7w5KRlmwVf7cg"
filename="data/kosarak_sessions.npy"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}


fileid="1O_ENbH0Zp77wVH0e8FqYAD17aUK6v39t"
filename="data/music_1.npy"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

fileid="1nzlfjKcr9vYjpon24svXmGlTiRLxEfQf"
filename="data/music_2.npy"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

