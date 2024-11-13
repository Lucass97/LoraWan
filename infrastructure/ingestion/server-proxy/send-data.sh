#!bin/bash

curl -X POST http://pitagora.inf.uniroma3.it:80/stream \
-H "Content-Type: application/json" \
-d '{"chiave1": "valore1", "chiave2": "valore2"}'
