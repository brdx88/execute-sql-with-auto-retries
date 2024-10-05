from impala.dbapi import connect, OperationalError
from impala.util import as_pandas
import datetime
import pytz

jakarta_tz = pytz.timezone('Asia/Jakarta')

def execute_query(cursor, query, retry_limit=500):
    retry_count = 0                                                                                        # counter. will be used to track how many times the query has been retried if it fails.

    while retry_count < retry_limit:                                                                       # loop is set to keep running as long as the number of retries is less than the retry_limit (i.e., 500). This loop will handle automatic retries if the query fails.
        try:                                                                                               
            cursor.execute(query)                                                                          # try block attempts to execute the query using the provided database cursor
            now = datetime.datetime.now(jakarta_tz).strftime("%Y-%m-%d %H:%M:%S")                          # current time in the jakarta_tz timezone is fetched and formatted as YYYY-MM-DD HH:MM:SS. This is used for logging purposes.
            print(f'[{now}] Successfully executed the query after {retry_count} retries.')
            break                                                                                          # the loop breaks here if the query is successful, and no further retries are attempted.
        except OperationalError:                                                                           # if an OperationalError (likely related to database connectivity issues) is encountered during query execution, the program moves to the except block to handle it.
            now = datetime.datetime.now(jakarta_tz).strftime("%Y-%m-%d %H:%M:%S")                          
            retry_count += 1                                                                               # the retry_count is incremented by 1 to keep track of how many retries have been performed
            print(f'[{now}] Encountered an OperationalError. Retry #{retry_count}. Retrying...')

    if retry_count == retry_limit:                                                                         # after the loop ends, and if the number of retries has reached the retry limit, this block is executed.
        print(f'Failed to execute the query after {retry_limit} retries.')


# Establishing the Impala connection
conn = connect(host='your.big.data.address.com', port=8888, auth_mechanism='GSSAPI', use_ssl=False, kerberos_service_name='impala')
cursor = conn.cursor() 

# Establishing your database table
table_name = "your_scheme.your_table"

# Execute the your query (even your complex sql query)
execute_query(cursor, f"SELECT * FROM {table_name}")

# if the sql query goes complex, you cold use below, or use your preferences
your_query = """
SELECT *
FROM your_table AS BASELINE
LEFT JOIN your_another_table AS ANOTHER
  ON BASELINE.id = ANOTHER.unique_id
"""
execute_query(cursor, your_query, retry_limit = 888)        # you can put your desire numbers to retry the execution of the sql query
