sudo docker cp ./spark.py spark-master:/opt/bitnami/spark/spark.py
sudo docker cp ./misc spark-master:/opt/bitnami/spark/misc
sudo docker exec -it spark-master spark-submit \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.1,com.github.jnr:jnr-posix:3.1.7 spark.py
