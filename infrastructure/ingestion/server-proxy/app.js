const express = require('express');
const { Kafka } = require('kafkajs');

const app = express();
const kafka = new Kafka({ brokers: ['localhost:29092','localhost:39092'] });
const producer = kafka.producer();

app.use(express.json());

app.post('/ricevi', async (req, res) => {
    await producer.send({
        topic: 'live-data',
        messages: [{ value: JSON.stringify(req.body) }],
    });
    res.status(200).send('Messaggio inviato a Kafka!');
});

app.listen(80, async () => {
    await producer.connect();
    console.log('Server in ascolto su http://localhost:3000');
});