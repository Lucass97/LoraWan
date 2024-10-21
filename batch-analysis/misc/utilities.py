
def save_to_cassandra(df, table_name, keyspace="batchkeyspace"):
    """
    Saves a PySpark DataFrame to a Cassandra table.

    Args:
        df (DataFrame): The PySpark DataFrame to be saved to Cassandra.
        table_name (str): The name of the destination table in Cassandra.
        keyspace (str, optional): The name of the keyspace where the table is located. 
                                  The default value is "batchkeyspace".

    Returns:
        None: This function does not return any value; it only writes data to Cassandra.

    Note:
        - Ensure that the keyspace and table exist in Cassandra before calling this function.
        - The 'append' mode allows adding data to the existing content of the table.
    """
    
    # Write the DataFrame in the specified format for Cassandra
    df.write \
      .format("org.apache.spark.sql.cassandra") \
      .mode('append') \
      .options(table=table_name, keyspace=keyspace) \
      .save()
      
      
      
def heat_index_calculation(df):
    return