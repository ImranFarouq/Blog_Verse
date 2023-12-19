#! /bin/bash


sudo yum install git -y 
sudo yum install pip -y


sudo tee /etc/yum.repos.d/mongodb-org-7.0.repo<<EOL
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
EOL
sudo yum install mongodb-mongosh-shared-openssl3 -y
sudo yum install mongodb-org -y
sudo systemctl start mongod --now

sudo -u ec2-user git clone https://github.com/ImranFarouq/Blog.git /home/ec2-user/blogverse


sudo pip install -r /home/ec2-user/blogverse/requirements.txt
sudo python3 /home/ec2-user/blogverse/main.py



