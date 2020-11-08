# Deployment Notes

## Django
- git clone <repo>
- Change executables permissions
chmod +x gunicorn_bingo.sh 

- Delete/create Postgres DB
sudo su - postgres
dropdb bingo_db
createdb --owner bingo_admin bingo_db

- Pip install venv
- Migrate

Redis: 
Error: BZPOPMIN
---> Restart the machine!!!!

## Vue.js
#### REFERENCE: Install Vue (https://www.youtube.com/watch?v=uIx5QLrNqn0&ab_channel=PartiallyDeveloped): 
1) Make sure to install on the system:
- nvm (curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh |bash)
-- nvm use stable

- nodejs / npm (nvm install stable)
- yarn (https://linuxize.com/post/how-to-install-yarn-on-ubuntu-18-04/ )

2) Vue
- axios package

## Vue commands
npm run serve

** If Error with core package while running the server:
npm add core-js

## Server Setup (https://www.youtube.com/watch?v=9L5vhIyQFQk)
Add group:
sudo addgroup --system bingo

Create directory for the apps
mkdir -p /webapps/bingo

Add user and make it the owner of the directory
sudo useradd --system --gid bingo --shell /bin/bash --home /webapps/bingo bingouser
sudo chown bingouser: /webapps/bingo

## Deployment Vue: 
* This is with the dist directory and index.html file in it:
- https://www.youtube.com/watch?v=9L5vhIyQFQk
- https://www.youtube.com/watch?v=OIQIniWTJlU

* For setup that runs npm server, use the config file here

## Installing pm2("supervisor") for the npm:
- https://nuxtjs.org/faq/deployment-pm2
- https://www.digitalocean.com/community/tutorials/how-to-set-up-a-node-js-application-for-production-on-ubuntu-18-04

pm2 start (from inside project dir)
pm2 list
pm2 ls
pm2 info app_name
pm2 stop app_name_or_id
pm2 restart app_name_or_id
pm2 delete app


## Setup hooks for automatic deployment from git
- https://www.youtube.com/watch?v=vaQ0N9082Nw (time: 15:30)
mkdir hooks
vi post_receive
----- post_receive ----
#!/bin/bash
git --work-tree=/home/ubuntu/vue_bingo/bingo --git-dir=/home/ubuntu/vue_bingo/bingo checkout -f
------------------------

From your machine, in the project directory:
git remote add origin ubuntu@18.216.128.97:/home/ubuntu/vue_bingo/bingo

chmod +x post_receive