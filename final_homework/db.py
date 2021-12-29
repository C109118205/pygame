import mariadb
import sys

try:
    conn = mariadb.connect(
        

    )
    print('DB connected OK')
except mariadb.Error as e:
    print(f"DB connected error: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()