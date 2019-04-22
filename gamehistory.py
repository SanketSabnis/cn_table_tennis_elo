from elo import Player, Game, record_matches
from dbconnection import clear_db
import datetime


def reload_game_history():
    clear_db()
    sanket = Player(name="Sanket-Right")
    spencer = Player(name="Spencer")
    aaron = Player(name="Aaron")
    vince = Player(name="Vince")
    matt = Player(name="Matt")
    hector = Player(name="Hector")
    lauren = Player(name="Lauren")
    jeff = Player(name="Jeff")
    adam = Player(name="Adam-Hua")
    lee = Player(name="Lee")
    kim = Player(name="Kim")
    jeremy = Player(name="Jeremy")
    nick = Player(name="Nick")
    allgood = Player(name="Adam-Allgood")
    sanket_left = Player(name="Sanket-Left")
    beth = Player(name="Beth")
    joel = Player(name="Joel")
    dan = Player(name="Dan")
    sean = Player(name="Sean")
    print("Initial Ratings")
    # Game.show_ratings()
    season1 = [
        [sanket, lauren],
        [aaron, vince],
        [spencer, matt],
        [adam, lee],
        [sanket, aaron],
        [spencer, adam],
        [spencer, sanket]
    ]
    print("End of Season 1\n")
    record_matches(season1, datetime.datetime(2018, 1, 21))
    # Game.show_ratings()
    season2 = [
        # Group A
        [spencer, vince],
        [spencer, kim],
        [spencer, lauren],
        [spencer, matt],
        [vince, matt],
        [vince, lauren],
        [vince, kim],
        [kim, lauren],
        [kim, matt],
        [lauren, matt],
        # Group B
        [sanket, aaron],
        [sanket, jeff],
        [sanket, adam],
        [sanket, lee],
        [aaron, jeff],
        [aaron, adam],
        [aaron, lee],
        [jeff, adam],
        [jeff, lee],
        [adam, lee],
        # PlayOff
        [spencer, aaron],
        [sanket, vince],
        [aaron, vince],
        [sanket, spencer]
    ]
    print("End of Season 2\n")
    record_matches(season2, datetime.datetime(2018, 3, 21))
    Game.show_ratings()
    season3 = [
        [sanket, hector],
        [jeff, lauren],
        [aaron, adam],
        [vince, matt],
        [hector, lauren],
        [matt, adam],
        [sanket, jeff],
        [aaron, vince],
        [vince, hector],
        [matt, jeff],
        [sanket, aaron],
        [matt, vince],
        [aaron, matt]
    ]
    print("End of Season 3\n")
    record_matches(season3, datetime.datetime(2018, 5, 21))
    Game.show_ratings()

    season4 = [
        [hector, matt],
        [matt, hector],
        [matt, hector],
        [sanket, spencer],
        [spencer, sanket],
        [spencer, sanket]
    ]
    print("End of Season 4 Misc Games")
    record_matches(season4, datetime.datetime(2018, 8, 15))
    Game.show_ratings()

    season5 = [
        [matt, jeremy],
        [nick, adam],
        [vince, matt],
        [matt, adam],
        [allgood, lauren],
        [hector, jeff],
        [allgood, aaron],
        [aaron, matt],
        [allgood, vince],
        [sanket, nick],
        [sanket, hector],
        [sanket, allgood],
        [nick, jeremy],
        [lauren, jeff],
        [nick, lauren],
        [hector, aaron],
        [nick, vince],
        [hector, nick],
        [allgood, hector],
        [sanket, allgood]
    ]
    record_matches(season5, datetime.datetime(2019, 2, 7))
    print("End of Season 5")
    Game.show_ratings()
    season6 = [
        [sanket, sanket_left],
        [matt, jeff],
        [aaron, beth],
        [sanket, matt],
        [allgood, sean],
        [nick, dan],
        [lauren, jeremy],
        [sanket_left, jeff],
        [lauren, aaron],
        [nick, hector],
        [dan, aaron],
        [jeremy, beth],
        [hector, jeremy],
        [adam, vince],
        [allgood, adam],
        [vince, sean],
        [vince, matt],
        [lauren, allgood],
        [hector, vince]

    ]
    record_matches(season6, datetime.datetime(2019, 4, 1))
    print("Season 6 -- Live")
    Game.show_ratings()

    misc_games = [
        [aaron, adam],
        [hector, adam],

    ]
    record_matches(misc_games, datetime.datetime(2019, 4, 1))
    Game.show_ratings()


