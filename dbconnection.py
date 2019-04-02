import datetime
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect("sqlite3.db")
db.row_factory = dict_factory
cursor = db.cursor()


def clear_db():
    cursor.execute("DELETE FROM players")
    cursor.execute("DELETE FROM game_history")
    db.commit()


def add_game_log(winner, loser, recorded_at):
    cursor.execute("""
        INSERT into game_history
        (winner_id, loser_id, recorded_at, created_at)
        VALUES
        (?, ?, ?, ?)
    """, (winner, loser, recorded_at, datetime.datetime.now()))
    db.commit()


def get_ratings():
    cursor.execute("SELECT * from players order by rating DESC")
    result = cursor.fetchall()
    return result


def get_player_by_name(name):
    cursor.execute("SELECT * from players where name = ? LIMIT 1", (name, ))
    result = cursor.fetchone()
    return result if result else {}


def get_player(player_id):
    cursor.execute("SELECT * from players where id = ? LIMIT 1", (player_id, ))
    result = cursor.fetchone()
    return result if result else {}


def save_player(player_dict):
    keys = list(player_dict)
    supported_fields = ["id", "name", "rating", "matches_played", "wins", "losses"]
    for field in keys:
        if field not in supported_fields:
            player_dict.pop(field, None)
    if not player_dict.get("id"):
        cursor.execute("""
            INSERT into players
            (name, rating, matches_played, wins, losses, created_at)
            VALUES
            (?, ?, ?, ?, ?, ?)
        """, (
            player_dict["name"],
            player_dict["rating"],
            player_dict.get("matches_played") or 0,
            player_dict.get("wins") or 0,
            player_dict.get("losses") or 0,
            datetime.datetime.now()
        ))
        player_id = cursor.lastrowid
    else:
        player_id = player_dict.pop("id")
        cursor.execute("""
            UPDATE players
            SET name = ?, rating = ?, updated_at = ?, matches_played = ?, wins = ?, losses = ?
            WHERE id = ?
        """, (
            player_dict["name"],
            player_dict["rating"],
            datetime.datetime.now(),
            player_dict["matches_played"],
            player_dict["wins"],
            player_dict["losses"],
            player_id
        ))
    db.commit()
    return get_player(player_id)
