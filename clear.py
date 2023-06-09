import psycopg2

# Completely clear the database of all data
# Including all tables, rows, and columns, the entire schema

def clear():
    conn = psycopg2.connect("dbname=postgres user=postgres password=XE7FK9WBC3TjVDkyF2Wj host=database-1.ctdw8b5nynwk.us-west-2.rds.amazonaws.com port=5432")
    cur = conn.cursor()
    cur.execute("DROP SCHEMA public CASCADE")
    cur.execute("CREATE SCHEMA public")
    cur.execute("GRANT ALL ON SCHEMA public TO postgres")
    cur.execute("GRANT ALL ON SCHEMA public TO public")
    conn.commit()
    cur.close()
    conn.close()
    print("It is done.")

clear()