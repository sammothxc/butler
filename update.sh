ssh butler@truenas-butler << ENDSSH
cd /home/butler/butler
git pull
sudo systemctl restart butler
ENDSSH