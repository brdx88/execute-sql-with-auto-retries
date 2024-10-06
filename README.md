# Retryable SQL Query Execution in Python 🔄

## Overview
This Python script is designed to execute SQL queries with an automated retry mechanism, ensuring reliable database interaction even when encountering operational errors. If an error occurs, the script will retry the query multiple times until either it succeeds or reaches a defined retry limit.

This approach is helpful in scenarios where database connectivity might be unstable, ensuring your queries are executed without manual intervention.

## Problems
When running SQL queries through Hue for Impala or Hive, encountering errors is a common frustration. Each time a query fails, I would need to manually hit the 'run' button or press Ctrl + Enter repeatedly, hoping the query would eventually succeed. 

This process ties me to the screen, forcing constant supervision. It's not only time-consuming but also mentally exhausting, as any moment away from the monitor could result in missed retries. 

It would be far more efficient to automate this process, ensuring that queries handle errors gracefully and retry automatically—giving me peace of mind that the execution will succeed without my direct oversight.

## Features
- **Automatic Retry Handling**: If a query fails due to an operational error, the script retries it up to 500 times (configurable).
- **Customizable Retry Limit**: Set a custom retry limit based on your requirements.
- **Time-Stamped Logs**: Detailed logs for both successful and failed attempts, complete with timestamps.
- **Error Handling**: Robust exception handling for operational errors encountered during query execution.

## Installation & Usage
1. Clone this repository:
    ```bash
    git clone https://github.com/brdx88/execute-sql-with-auto-retries.git
    ```

2. Install the required packages:
    ```bash
    pip install impyla
    ```

3. Sample usage:
    ```python
    from impala.dbapi import connect, OperationalError
    from impala.util import as_pandas
    import datetime
    import pytz
    jakarta_tz = pytz.timezone('Asia/Jakarta')

    conn = connect(host='your.big.data.address.com', port=8888, auth_mechanism='GSSAPI', use_ssl=False, kerberos_service_name='impala')
    cursor = conn.cursor()
    
    execute_query(cursor, "SELECT * FROM your_table")
    ```

## Code Explanation
```python
def execute_query(cursor, query, retry_limit=500):
    retry_count = 0
    while retry_count < retry_limit:
        try:
            cursor.execute(query)
            now = datetime.datetime.now(jakarta_tz).strftime("%Y-%m-%d %H:%M:%S")
            print(f'[{now}] Successfully executed the query after {retry_count} retries.')
            break
        except OperationalError:
            now = datetime.datetime.now(jakarta_tz).strftime("%Y-%m-%d %H:%M:%S")
            retry_count += 1
            print(f'[{now}] Encountered an OperationalError. Retry #{retry_count}. Retrying...')
    if retry_count == retry_limit:
        print(f'Failed to execute the query after {retry_limit} retries.')
```
- `retry_limit`: Limits how many times the query will retry.
- `try-except` block: Executes the query and catches operational errors.
- Logging: Provides feedback on each execution attempt with a timestamp.

## Why Retry Mechanism Matters
In real-world environments, database connections can be affected by network instability, timeouts, or temporary server issues. With a retry mechanism, we can ensure the system remains resilient, reducing the chance of manual intervention during these issues.

## Contributing
Feel free to submit pull requests to improve the script. Contributions are always welcome!
