sudo apt-get update
sudo apt install openjdk-11-jdk -y
sudo apt install apt-transport-https
echo "deb https://debian.cassandra.apache.org 40x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -
sudo apt-get update
sudo apt install cassandra
sudo systemctl enable cassandra

sed -i "cassandra.yaml"
