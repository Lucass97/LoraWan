
## Installazione locale di node

```bash
npm install
```

```bash
sudo node app.js
```

## Docker

```bash
sudo docker build -t server-proxy .
```

```bash
sudo docker run --name server-proxy -d -p 80:80 server-proxy
sudo docker run --name server-proxy -p 80:80 server-proxy
sudo docker run --name server-proxy -d --network shared-net -p 80:80 server-proxy

```