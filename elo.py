#!/usr/local/bin/python3
import dbconnection
from pprint import pprint
import datetime
import statistics
import gamehistory

K = 64
C = 800
K_ = 20
C_ = 200

rating_default = 1200
inactive_players = ["Kim", "Lee", "Spencer"]


def record_elo(r1, r2):
    R1 = 10 ** (r1 / C)
    R2 = 10 ** (r2 / C)
    e1 = R1 / float(R1 + R2)
    e2 = R2 / float(R1 + R2)
    new_r1 = int(round(r1 + (K * (1 - e1))))
    new_r2 = int(round(r2 + (K * (0 - e2))))
    return new_r1, new_r2


def record_elo_(r1, r2):
    e1 = r1 + (K_ / 2) * (1 - 0 + 0.5 * ((r2 - r1) / float(C_)))
    e2 = r2 + (K_ / 2) * (0 - 1 + 0.5 * ((r1 - r2) / float(C_)))
    new_r1 = int(round(e1))
    new_r2 = int(round(e2))
    return new_r1, new_r2


def record_matches(matches, recorded_at=None):
    for winner, loser in matches:
        Game.record_match(winner, loser, recorded_at)


def check_pair(i, pair, visited, subseq, needed=4):

    p1 = pair.get("p1")
    p2 = pair.get("p2")
    if visited.get(p1) or visited.get(p2):
        return 2000, subseq[i]["players"]

    visited[p1] = 1
    visited[p2] = 1
    if len(subseq[i]["rating"]) == needed:
        subseq[i]["rating"].append(pair["rating"])
        subseq[i]["players"].append([p1, p2])
        stdev = statistics.stdev(subseq[i]["rating"])
        return stdev, subseq[i]["players"]

    return 2000, subseq[i]["players"]


def print_pairings(pairings):
    pairings = sorted(pairings, key=lambda x: x["rating"], reverse=True)
    for pair in pairings:
        print("{p1: <10} {p2: <10} Rating: {rating: <10}".format(**pair))


def find_pairings(players):
    active_players = [x for x in players if x["name"] not in inactive_players]
    LEN = len(active_players)
    pairings = []
    for i in range(LEN):
        for j in range(i + 1, LEN):
            p1 = active_players[i]
            p2 = active_players[j]
            pairings.append({
                "rating": (p1["rating"] + p2["rating"]) / 2,
                "p1": p1["name"],
                "p2": p2["name"]
            })

    optimized = []
    for i in range(LEN // 2):
        p1 = active_players[i]
        p2 = active_players[LEN - 1 - i]
        optimized.append({
            "rating": (p1["rating"] + p2["rating"]) / 2,
            "p1": p1["name"],
            "p2": p2["name"]
        })

    optimized = sorted(optimized, key=lambda x: x["rating"], reverse=True)
    print("Optimized")
    print_pairings(optimized)


class Game():
    @staticmethod
    def record_match(player, opponent, recorded_at=None):
        result = record_elo(player.rating, opponent.rating)
        player.set_rating(result[0], winner=True)
        opponent.set_rating(result[1])
        if not recorded_at:
            recorded_at = datetime.datetime.now()
        dbconnection.add_game_log(player, opponent, recorded_at)

    def show_ratings():
        ratings = dbconnection.get_ratings()
        # rating_list = sorted(ratings, key=lambda x: x["rating"], reverse=True)
        print("{0: <25} {1: <8} {2: <7} {3: <5} {4: <7} {5: <8}".format(
            "Name", "Rating", "Played", "Wins", "Losses", "Win Rate"))
        for player in ratings:
            if player["name"] in inactive_players:
                continue
            winrate = 0.0
            if player["matches_played"]:
                winrate = 100 * float((player["wins"] or 0) / player["matches_played"])
            print("{0: <25} {1: <8} {2: <7} {3: <5} {4: <7} {5: <1.2f}%".format(
                player["name"],
                player["rating"],
                player["matches_played"],
                player["wins"] or 0,
                player["losses"] or 0,
                winrate
            ))
        print("=====================================")
        return ratings


class Player():
    def __init__(self, **kwargs):
        for kw, value in kwargs.items():
            setattr(self, kw, value)
        if not hasattr(self, "rating"):
            setattr(self, "rating", rating_default)
        if hasattr(self, "name"):
            player_by_name = dbconnection.get_player_by_name(self.name)
            if player_by_name:
                player_id = player_by_name["id"]
                self.id = player_id
        if not hasattr(self, "id"):
            self.save()

    @staticmethod
    def get(player_id):
        player_dict = dbconnection.get_player(player_id)
        return Player(**player_dict)

    def set_rating(self, rating, winner=False):
        self.rating = rating
        self.matches_played = getattr(self, "matches_played", 0) + 1
        if winner:
            self.wins = getattr(self, "wins", 0) + 1
            self.losses = getattr(self, "losses", 0)
        else:
            self.losses = getattr(self, "losses", 0) + 1
            self.wins = getattr(self, "wins", 0)
        self.save()

    def save(self, ):
        player = dbconnection.save_player(self.__dict__)
        if player.get("id") and not hasattr(self, "id"):
            self.id = player["id"]

    def get_game_history(self):
        player_history = dbconnection.get_player_history(self.id)
        formatted_records = [("2017-11-1 00:00:00", 1200)]
        for record in player_history:
            if record["winner_id"] == self.id:
                formatted_records.append(
                    (record["recorded_at"], record["winner_rating"])
                )
            else:
                formatted_records.append(
                    (record["recorded_at"], record["loser_rating"])
                )
        print("{0: <25} {1: <8}".format("Date", "Rating"))
        for record in formatted_records:
            print("{0: <25} {1: <8}".format(record[0].split(" ")[0], record[1]))

        return formatted_records



if __name__ == "__main__":
    #ratings = Game.show_ratings()
    gamehistory.reload_game_history()
    #find_pairings(ratings)
