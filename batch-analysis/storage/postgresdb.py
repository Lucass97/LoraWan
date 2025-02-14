
def save_to_postgres(df, table_name: str, properties: str, url: str = POSTGRES_URL) -> None:
    """
    Saves a PySpark DataFrame to a PostgreSQL table.

    Args:
        df (DataFrame): The PySpark DataFrame to be saved to PostgreSQL.
        table_name (str): The name of the destination table in PostgreSQL.
        properties (str): Connection properties, including credentials and driver settings.
        url (str, optional): The JDBC URL for connecting to the PostgreSQL database.
                             The default value is defined by POSTGRES_URL.

    Returns:
        None: This function does not return any value; it only writes data to PostgreSQL.

    Note:
        - Ensure that the PostgreSQL database and the target table exist before calling this function.
        - The 'overwrite' mode replaces existing data in the table.
        - The properties argument should contain the necessary authentication details and driver configuration.
    """
    
    df.write.jdbc(url=url, table=table_name, mode="overwrite", properties=properties)
