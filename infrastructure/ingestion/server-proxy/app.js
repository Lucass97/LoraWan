const express = require('express');
const { Kafka, Partitioners } = require('kafkajs');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const kafka = new Kafka({ brokers: ['kafka1:9092', 'kafka2:9092'] });
const producer = kafka.producer({
    createPartitioner: Partitioners.LegacyPartitioner
});

app.use(express.json());

// middleware to log every request
app.use((req, res, next) => {
    console.log(`Received ${req.method} request for '${req.url}'`);
    console.log('Request Headers:', JSON.stringify(req.headers, null, 2));
    console.log('Request Body:', JSON.stringify(req.body, null, 2));
    next();
});

app.post('/stream', async (req, res) => {
    await producer.send({
        topic: 'live-data',
        messages: [{ value: JSON.stringify(req.body) }],
    });
    res.status(200).json({});
});

// Endpoint per reindirizzare le richieste a Grafana
app.use('/grafana', createProxyMiddleware({
    target: 'http://grafana:3000/login', // Cambia con l'URL di Grafana
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        // Inoltra le intestazioni originali
        if (req.headers['authorization']) {
            proxyReq.setHeader('Authorization', req.headers['authorization']);
        }
    },
}));

app.listen(80, async () => {
    await producer.connect();
    console.log('Server in ascolto su http://localhost:80');
});