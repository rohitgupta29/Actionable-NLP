from configparser import ConfigParser
import psycopg2
from typing import Dict, List
import pandas as pd
import psycopg2.extras as psql_extras
from twitter_utils import tweet_user

def load_connection_info(ini_filename: str) -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(ini_filename)
    # Create a dictionary of the variables stored under the "postgresql" section of the .ini
    conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
    return conn_info

def create_db(conn_info: Dict[str, str],) -> None:
    # Connect just to PostgreSQL with the user loaded from the .ini file
    psql_connection_string = f"user={conn_info['user']} password={conn_info['password']}"
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()

    # "CREATE DATABASE" requires automatic commits
    conn.autocommit = True
    sql_query = f"CREATE DATABASE {conn_info['database']};"

    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        cur.close()
    else:
        # Revert autocommit settings
        conn.autocommit = False

def create_table(
    sql_query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor
) -> None:
    try:
        # Execute the table creation query
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()

    # Connect to the database created
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

def alter_table(
    sql_query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor
) -> None:
    try:
        # Execute the table creation query
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()

    # Connect to the database created
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

def insert_data(
    query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    df: pd.DataFrame,
    page_size: int
) -> None:
    data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]
    try:
        psql_extras.execute_values(
            cur, query, data_tuples, page_size=page_size)
        print("Query:", cur.query)

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()

    else:
        conn.commit()


def get_column_names(
        table: str,
        cur: psycopg2.extensions.cursor) -> List[str]:
    cursor.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';")
    col_names = [result[0] for result in cursor.fetchall()]
    return col_names

def get_data_from_db(
        query: str,
        conn: psycopg2.extensions.connection,
        cur: psycopg2.extensions.cursor,
        df: pd.DataFrame,
        col_names: List[str]) -> pd.DataFrame:
    try:
        cur.execute(query)
        while True:
            #Fetch the next 100 rows
            query_results = cur.fetchmany(3)
            #If empty list is returned, then we have reached the end of the results
            if query_results == list():
                break

            # Create a list of dictionaries where each dictionary represents a single row
            results_mapped = [
                {col_names[i]:row[i] for i in range(len(col_names))}
                for row in query_results
            ]

            #Append the fetched rows to the DataFrame
            df = df.append(results_mapped, ignore_index = True)

            return df

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()




if __name__ == '__main__':
    conn_info = load_connection_info("db.ini")

    #create a desired database
    create_db(conn_info)

    # Connect to the database created
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    # Create the "employee" table
    # employee_sql = """
    #         CREATE TABLE IF NOT EXISTS Employee (
    #             id SERIAL PRIMARY KEY,
    #             Name Text NOT NULL,
    #             twitter_id VARCHAR(250),
    #             linkedin_url VARCHAR(250)
    #         )
    #     """
    #
    # create_table(employee_sql, connection, cursor)
    #
    # alter_sql = """ALTER TABLE Employee
    #                 ADD COLUMN twitter_sentiment INT """
    #
    # alter_table(alter_sql, connection,cursor)
    # Insert data into the "employee" table
    employee_df = pd.DataFrame({
        "id": [1, 2,3],
        "name": ["The Hindu", "Ajay", "Ravi"],
        "twitter_id": ["@the_hindu","@elonmusk","@lppage"],
        "linkedin_url": ["TH","A","R"],
        "tweet_sentiment": [tweet_user("@the_hindu"),tweet_user("@elonmusk"),tweet_user("@lppage")]
        })
    # employee_df["twitter_sentiment_1"] = employee_df["twitter_id"].apply(lambda x: tweet_user(x))
    print(employee_df)
    # #
    # # employee_query = "INSERT INTO employee(id, name,twitter_id,linkedin_url) VALUES %s"
    # # insert_data(employee_query, connection, cursor, employee_df, 100)
    # #
    # # print("updated table")
    #
    # col_names = get_column_names("employee", cursor)
    #
    # new_df = pd.DataFrame(columns = col_names)
    # query = "SELECT * from employee;"
    # new_df = get_data_from_db(query, connection,cursor,new_df, col_names)
    # print(new_df)



    connection.close()
    cursor.close()
