import sqlite3

#Frequency: how many times watering per day
#Duration: How long time each watering
def create_users_table(CONN, C):
    C.execute("""
    CREATE TABLE IF NOT EXISTS users
    (
        username varchar(255),
        email varchar(255),
        password varchar(255),
        latitude decimal(3, 10),
        longitude decimal(3, 10),
        frequency int,
        duration int,
        landSize int,
        PRIMARY KEY (username),
        UNIQUE (email)
    );
    """)
    CONN.commit()

def create_usage_table(CONN, C):
    C.execute("""
    CREATE TABLE IF NOT EXISTS usage
    (
        username varchar(255),
        waterDate date,
        frequency int,
        duration int,
        PRIMARY KEY (username, waterDate)
    )
    """)
    CONN.commit()


if __name__ == "__main__":

    CONN = sqlite3.connect("farmer_insights.db")
    C = CONN.cursor()
    
    create_users_table(CONN, C)
    create_usage_table(CONN, C)
    
    C.close()
    CONN.close()