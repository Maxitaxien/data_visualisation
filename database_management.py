import sqlite3

# Connect to the SQLite database
connect = sqlite3.connect('instance/test.db')
cur = connect.cursor()

# Execute the SQL commands to rename the column and create a new table
cur.execute('ALTER TABLE Todo RENAME TO TempTodo;')
cur.execute('CREATE TABLE Todo (id INTEGER PRIMARY KEY, filename VARCHAR(200) NOT NULL, filesize INTEGER DEFAULT 0);')

# Copy data from the temporary table to the new table
cur.execute('INSERT INTO Todo (id, filename, filesize) SELECT id, filename, date_created FROM TempTodo;')

# Drop the temporary table
cur.execute('DROP TABLE TempTodo;')

# Commit the changes and close the connection
connect.commit()
connect.close()
