ssh root@truenas-butler << ENDSSH
cd /home/butler/butler
git pull
systemctl restart butler
ENDSSH