git add . && git commit -m \"update\" && git push
ssh butler@hitmanserver << ENDSSH
cd /home/butler/butler
git pull
sudo systemctl restart butler
ENDSSH