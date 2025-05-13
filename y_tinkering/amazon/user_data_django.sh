yum install httpd php php-mysql -y
yum install python36 python36-virtualenv python36-pip -y
pip install --upgrade pip
cd /home/ec2-user
python3 -m venv /home/ec2-user/venv
source /home/ec2-user/venv/bin/activate
pip install django
pip install --upgrade pip
yum update -y
service httpd start
chkconfig httpd on
