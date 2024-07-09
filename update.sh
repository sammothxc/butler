#!/bin/bash
git add . && git commit -m \"update\" && git push
source .env
IFS='.' read -r -a version_parts <<< "$BOT_VERSION"
((version_parts[2]++))
new_version="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"
sed -i "s/BOT_VERSION=.*/BOT_VERSION=$new_version/" .env
ssh butler@hitmanserver << ENDSSH
cd /home/butler/butler
git pull
source .env
IFS='.' read -r -a version_parts <<< "$BOT_VERSION"
((version_parts[2]++))
new_version="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"
sed -i "s/BOT_VERSION=.*/BOT_VERSION=$new_version/" .env
sudo systemctl restart butler
ENDSSH