
def save_to_postgres(df, table_name: str, properties: str, url: str = POSTGRES_URL) -> None:
    """
    Saves a PySpark DataFrame to a PostgreSQL table.

    Args:
        df (DataFrame): PySpark DataFrame to save.
        table_name (str): Destination table name.
        properties (str): Connection properties (credentials, driver settings).
        url (str, optional): JDBC URL (default: POSTGRES_URL).

    Note:
        - Overwrites existing data.
        - Ensure the table exists.
    """
    df.write.jdbc(url=url, table=table_name, mode="overwrite", properties=properties)
