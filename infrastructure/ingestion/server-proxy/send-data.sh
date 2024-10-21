#!bin/bash

curl -X POST http://localhost:3000/ricevi \
-H "Content-Type: application/json" \
-d '{"chiave1": "valore1", "chiave2": "valore2"}'
