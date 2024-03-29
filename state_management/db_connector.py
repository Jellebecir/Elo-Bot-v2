import os
from mysql import connector
from datetime import date
from state import State

class DBConnector:
    
    def __init__(self) -> None:
        self.connection_pool = connector.pooling.MySQLConnectionPool(
            host = os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE'],
            port = os.environ['PORT'],
            pool_name = 'elo_bot_pool',
            pool_size = 5
        )

    def create_channel_table(self, channel_id):
        with self.connection_pool.get_connection() as cnx:
            query = "CREATE TABLE IF NOT EXISTS {} (" \
                    "match_id INT PRIMARY KEY AUTO_INCREMENT," \
                    "winner_id VARCHAR(25) NOT NULL, " \
                    "loser_id VARCHAR(25) NOT NULL, " \
                    "date DATE NOT NULL)".format(channel_id)
            cursor = cnx.cursor()
            cursor.execute(query)
            cursor.close()
            cnx.commit()
            print('- CREATED TABLE FOR CHANNEL {}'.format(channel_id))
    
    def user_has_played_match(self, user_id, channel_id):
        with self.connection_pool.get_connection() as cnx:
            query = "SELECT EXISTS(SELECT 1 FROM {channel_id} " \
                    "WHERE winner_id = '{user_id}' " \
                    "OR loser_id = '{user_id}')" \
                    .format(
                        channel_id=channel_id, 
                        user_id=user_id
                    )
            cursor = cnx.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            if data[0][0]:
                return True
            return False
    
    def get_channel_state(self, channel_id):
        matches = self.get_matches(channel_id)
        return State(matches)
        
    def get_matches(self, channel_id):
        with self.connection_pool.get_connection() as cnx:
            query = "SELECT winner_id, loser_id FROM {}".format(channel_id)
            cursor = cnx.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return data
        
    def record_match(self, winner_id, loser_id, channel_id):
        with self.connection_pool.get_connection() as cnx:
            query = "INSERT INTO {} (winner_id, loser_id, date)" \
                    "VALUES ('{}', '{}', '{}');" \
                    .format(channel_id, winner_id, loser_id, date.today().strftime("%Y%m%d"))
            cursor = cnx.cursor()
            cursor.execute(query)
            cnx.commit()
            cursor.close()
            print("- INSERTED MATCH INTO {} WITH WINNER {} AND LOSER {}".format(channel_id, winner_id, loser_id))

    def get_score_between_players(self, requester_id, opponont_id, channel_id):
        with self.connection_pool.get_connection() as cnx:
            query = f"SELECT\n" \
                    f"   SUM(CASE WHEN winner_id = '{requester_id}' THEN 1 ELSE 0 END),\n" \
                    f"   SUM(CASE WHEN winner_id = '{opponont_id}' THEN 1 ELSE 0 END)\n" \
                    "FROM\n" \
                    f"   {channel_id}\n" \
                    "WHERE\n" \
                    f"   (winner_id = '{requester_id}' AND loser_id = '{opponont_id}') OR\n" \
                    f"   (winner_id = '{opponont_id}' AND loser_id = '{requester_id}');"
            cursor = cnx.cursor()
            cursor.execute(query)
            data = cursor.fetchall()[0]
            cursor.close()
            return {requester_id: data[0], opponont_id: data[1]}
        
    def revert_latest_match(self, requester_id, channel_id):
        with self.connection_pool.get_connection() as cnx:
            # Retrieve match data
            retrieve_query = f"SELECT * FROM {channel_id} WHERE loser_id = '{requester_id}' ORDER BY match_id DESC LIMIT 1;"
            cursor = cnx.cursor()
            cursor.execute(retrieve_query)
            match = cursor.fetchone()

            # Delete match data
            delete_query = f"DELETE FROM {channel_id} WHERE loser_id = '{requester_id}' ORDER BY match_id DESC LIMIT 1;"
            cursor.execute(delete_query)

            cnx.commit()
            cursor.close()
            if match:
                print(f"- REVERTED MATCH {match[0]} FROM {channel_id} WHERE WINNER WAS {match[1]} AND LOSER {match[2]} WITH DATE {match[3]}")
            return match

    def get_history(self, requester_id, channel_id):
        with self.connection_pool.get_connection() as cnx:
            # Retrieve matches where player participated
            query = f"SELECT * FROM {channel_id} WHERE winner_id = '{requester_id}' OR loser_id = '{requester_id}' ORDER BY match_id DESC LIMIT 10;"
            cursor = cnx.cursor()
            cursor.execute(query)
            history = cursor.fetchall()
            cursor.close()
            return history