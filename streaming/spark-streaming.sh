sudo docker cp ./spark-streaming.py spark-master:/opt/bitnami/spark/spark-streaming.py
sudo docker exec -it spark-master rm -r /opt/bitnami/spark/misc
sudo docker cp ./misc spark-master:/opt/bitnami/spark/misc
sudo docker exec -it spark-master spark-submit \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.1,com.github.jnr:jnr-posix:3.1.20,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark-streaming.py