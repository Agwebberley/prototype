import psycopg2

# Completely clear the database of all data
# Including all tables, rows, and columns, the entire schema

def clear():
    double_check = input("Are you sure you want to clear the database? (y/n) ")
    if double_check != "y":
        print("Aborting.  That was a close one.")
        return
    elif double_check == "y":
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
        return
    else:
        print("Invalid input.  Aborting.")
        return

if __name__ == "__main__":
    clear()