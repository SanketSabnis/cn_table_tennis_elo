#!/usr/local/bin/python3
import dbconnection
from pprint import pprint
import datetime
import statistics
import gamehistory

K = 64
rating_default = 1200
inactive_players = ["Kim", "Lee"]


def record_elo(r1, r2):
    e1 = r1 / float(r1 + r2)
    e2 = r2 / float(r1 + r2)
    new_r1 = int(round(r1 + (K * (1 - e1))))
    new_r2 = int(round(r2 + (K * (0 - e2))))
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
        player.set_rating(result[0])
        opponent.set_rating(result[1])
        if not recorded_at:
            recorded_at = datetime.datetime.now()
        dbconnection.add_game_log(player.id, opponent.id, recorded_at)

    def show_ratings():
        ratings = dbconnection.get_ratings()
        # rating_list = sorted(ratings, key=lambda x: x["rating"], reverse=True)
        print("{0: <25} {1: <8}".format("Name", "Rating"))

        for player in ratings:
            if player["name"] in inactive_players:
                continue
            print("{0: <25} {1: <8}".format(player["name"], player["rating"]))
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

    def set_rating(self, rating):
        self.rating = rating
        self.save()

    def save(self, ):
        player = dbconnection.save_player(self.__dict__)
        if player.get("id") and not hasattr(self, "id"):
            self.id = player["id"]


if __name__ == "__main__":
    ratings = Game.show_ratings()
    gamehistory.reload_game_history()
    #find_pairings(ratings)