#!/bin/bash
source /home/butler/butler/.env
IFS='.' read -r -a version_parts <<< "$BOT_VERSION"
((version_parts[2]++))
new_version="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"
sed -i "s/BOT_VERSION=.*/BOT_VERSION=$new_version/" /home/butler/butler/.env