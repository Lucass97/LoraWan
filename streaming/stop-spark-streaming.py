from pyspark.sql import SparkSession
#import requests
import time

# Inizializza una sessione Spark
spark = SparkSession.builder \
    .appName("Flight Streaming Analysis") \
    .getOrCreate()

# Ottieni il SparkContext
sc = spark.sparkContext

# Ottieni l'ID del job (ID dell'applicazione)
job_id = sc.applicationId
print(f"Job ID: {job_id}")
print(f"Job ID: {job_id}")
print(f"Job ID: {job_id}")
print(f"Job ID: {job_id}")
print(f"Job ID: {job_id}")

print(f"Job ID: {job_id}")
print(f"Job ID: {job_id}")



# Ferma il SparkContext
sc.stop()
print("SparkContext fermato.")



# URL per fermare il job tramite l'API REST di Spark
# Assicurati di sostituire <driver-node> con l'indirizzo del tuo nodo driver
"""driver_node = "localhost"
url = f"http://{driver_node}:4040/jobs/{job_id}/kill"

# Invia una richiesta per fermare il job
try:
    response = requests.post(url)
    if response.status_code == 200:
        print(f"Job {job_id} fermato con successo.")
    else:
        print(f"Errore nel fermare il job {job_id}: {response.text}")
except Exception as e:
    print(f"Si è verificato un errore: {e}")"""


