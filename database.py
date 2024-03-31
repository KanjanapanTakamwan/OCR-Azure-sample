import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace "your_password" with your actual MySQL root password
            database="teamject"   # Replace "your_database" with the name of your database
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            return connection

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL:", e)
        return None

def close_connection(connection):
    if connection:
        connection.close()
        print("MySQL connection is closed")



def get_or_insert_player(name):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Prepare SQL query to select player by name
            sql_query = "SELECT * FROM player WHERE name = %s"
            player_data = (name,)

            # Execute the SQL query
            cursor.execute(sql_query, player_data)

            # Fetch the first row
            row = cursor.fetchone()

            # If player exists, return player details
            if row:
                print("Player '{}' already exists.".format(name))
                return "id:{}, name:{}".format(row[0], row[1])

            # If player does not exist, insert player and return player details
            else:
                print("Player '{}' does not exist. Inserting...".format(name))
                insert_sql_query = "INSERT INTO player (name) VALUES (%s)"
                cursor.execute(insert_sql_query, player_data)
                connection.commit()
                print("Player '{}' inserted successfully.".format(name))
                return "id:{}, name:{}".format(cursor.lastrowid, name)

        except mysql.connector.Error as e:
            print("Error while retrieving/inserting player data from MySQL:", e)

        finally:
            if 'cursor' in locals():
                cursor.close()
            close_connection(connection)

# Example usage
# player_name = "123"
# player_details = get_or_insert_player(player_name)
# print("Player details:", player_details)

def insert_board(player_id, level, suit, by, result, score):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Prepare SQL query to insert a new record into the board table
            sql_query = "INSERT INTO board (player_id, level, suit, `by`, result, score) VALUES (%s, %s, %s, %s, %s, %s)"
            board_data = (player_id, level, suit, by, result, score)

            # Execute the SQL query
            cursor.execute(sql_query, board_data)

            # Commit the transaction
            connection.commit()

            # Return the ID of the last inserted row
            return cursor.lastrowid

        except mysql.connector.Error as e:
            print("Error while inserting record into MySQL:", e)
            return None

        finally:
            if 'cursor' in locals():
                cursor.close()
            close_connection(connection)

# Example usage
# player_id = 1
# level = 1
# suit = 1
# by = 1
# result = 1
# score = 1

# inserted_id = insert_board(player_id, level, suit, by, result, score)
# print("Inserted board ID:", inserted_id)

def insert_game(host_id, guest_id, host_board_id, guest_board_id, imps, board):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Find the maximum match value in the game table
            cursor.execute("SELECT MAX(`match`) FROM game")
            max_match = cursor.fetchone()[0]

            # If max_match is None, set it to 1, otherwise increment by 1
            if max_match is None:
                max_match = 1
            else:
                max_match += 1

            # Prepare SQL query to insert a new record into the game table
            sql_query = "INSERT INTO game (host_id, guest_id, host_board_id, guest_board_id, IMPs, `match`, board) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            game_data = (host_id, guest_id, host_board_id, guest_board_id, imps, max_match, board)

            # Execute the SQL query
            cursor.execute(sql_query, game_data)

            # Commit the transaction
            connection.commit()

            # Return True if insertion is successful
            return True

        except mysql.connector.Error as e:
            print("Error while inserting record into MySQL:", e)
            return False

        finally:
            if 'cursor' in locals():
                cursor.close()
            close_connection(connection)

# Example usage
# host_id = 1
# guest_id = 1
# host_board_id = 1
# guest_board_id = 1
# imps = 1
# board = 1

# inserted_successfully = insert_game(host_id, guest_id, host_board_id, guest_board_id, imps, board)
# if inserted_successfully:
#     print("Game record inserted successfully")
# else:
#     print("Failed to insert game record")