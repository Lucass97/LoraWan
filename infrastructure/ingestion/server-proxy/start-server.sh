
sudo docker build -t server-proxy .
sudo docker stop server-proxy
sudo docker rm server-proxy
sudo docker run --name server-proxy --network shared-net -p 80:80 server-proxy
