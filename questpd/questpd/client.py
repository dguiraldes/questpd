import psycopg2 as pg
import pandas as pd
from questdb.ingress import Sender, IngressError, TimestampNanos
import sys


class qdbClient:

    def __init__(self, host, front_port, back_port, user, password, database):
        self.host = host
        self.front_port = front_port
        self.back_port = back_port
        self.user = user
        self.password = password
        self.database = database

    def get_qdb_df(self, query):
        """
        Function to get a dataframe from QuestDB using a query
        Args:
            query (str): SQL query to be executed
        Returns:
            pd.DataFrame: Dataframe containing the results of the query
        """
        try:
            connection = pg.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port=self.back_port,
                                    database=self.database)
            cursor = connection.cursor()
            dataframe = pd.read_sql_query(query,connection)

        except (Exception, pg.Error) as error:
            print("Error while connecting to QuestDB", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return dataframe
    
    def upload_to_qdb(self, df, table_name, ts):
        """
        Function to upload a dataframe to QuestDB
        Args:
            df (pd.DataFrame): Dataframe to be uploaded
            table_name (str): Name of the table to upload the data to
            ts (str): Name of the column in the dataframe that contains the timestamp

        Returns:
            bool: True if successful, False otherwise

        Raises:
            Exception: Any exception that occurs during the upload process
        """
        try:
            conf = f'http::addr={self.host}:{self.front_port};'
            with Sender.from_conf(conf) as sender:
                sender.dataframe(df, table_name=table_name, at=ts)
            return True
        except IngressError as e:
            sys.stderr.write(f'QuestDB Ingress Error (URL: {conf}): {e}\n')
            raise
        except Exception as e:
            sys.stderr.write(f'Unexpected error during QuestDB upload: {str(e)}\n')
            raise

    def truncate_table(self, table_name):
        """
        Function to truncate a table in QuestDB
        Args:
            table_name (str): Name of the table to truncate

        Raises:
            Exception: Any exception that occurs during the truncation process
        """
        try:
            connection = pg.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port=self.back_port,
                                    database=self.database)
            cursor = connection.cursor()
            cursor.execute(f"TRUNCATE TABLE {table_name};")
            connection.commit()
        except (Exception, pg.Error) as error:
            print("Error while connecting to QuestDB", error)
            raise
        finally:
            if (connection):
                cursor.close()
                connection.close()

    def check_table_exists(self, table_name):
        """
        Function to check if a table exists in QuestDB
        Args:
            table_name (str): Name of the table to check
        Returns:
            bool: True if the table exists, False otherwise

        Raises:
            Exception: Any exception that occurs during the check process
        """
        try:
            connection = pg.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port=self.back_port,
                                    database=self.database)
            cursor = connection.cursor()
            cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1;")
            return True
        except (Exception, pg.Error) as error:
            print("Error while connecting to QuestDB", error)
            raise
        finally:
            if (connection):
                cursor.close()
                connection.close()

    def create_table(self, table_name, column_dict, ts_column, partition=None, dedup=None):
        """
        Function to create a table in QuestDB
        Args:
            table_name (str): Name of the table to create
            column_dict (dict): Dictionary containing the column names and types
            ts_column (str): Name of the column to be used as the timestamp
            partition (str): Time attribute to partition by
            dedup (str): Name of the column or columns to deduplicate by
        
        Raises:
            Exception: Any exception that occurs during the table creation process
        """
        column_str = ', '.join([f'{k} {v}' for k, v in column_dict.items()])
        partition = ','.join(partition) if isinstance(partition, list) else partition
        dedup = ','.join(dedup) if isinstance(dedup, list) else dedup
        partition_by = '' if partition == None else f'PARTITION BY {partition}'
        dedup_by = '' if dedup == None else f'DEDUP UPSERT KEYS ({dedup})'
        try:
            connection = pg.connect(user=self.user, 
                                    password=self.password, 
                                    host=self.host, 
                                    port=self.back_port, 
                                    database=self.database)
            cursor = connection.cursor()
            cursor.execute(f"CREATE TABLE {table_name} ({column_str}) timestamp({ts_column}) {partition_by} {dedup_by};")
            connection.commit()
        except (Exception, pg.Error) as error:
            print("Error while connecting to QuestDB", error)
            raise
        finally:
            if (connection):
                cursor.close()
                connection.close()