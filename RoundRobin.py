from itertools import combinations

class Player:
    def __init__(self, name) -> None:
        self._name = name
        self._partners = {}     # player: num
        self._opponents = {}    # player: num
        self._games = {}    # round: court
        self._north_south = {
            'north': 0,
            'south': 0
        }

    def get_name(self):
        return self._name
    
    def get_partners(self):
        return self._partners
    
    def get_opponents(self):
        return self._opponents
    
    def get_games(self):
        return self._games
    
    def get_side(self, side):
        '''
        Side either 'north' or 'south'. Returns int.
        '''
        return self._north_south[side]


class Tournament:
    def __init__(self) -> None:
        self._players = {}  # player name: Player obj
        self._tournament = {} # round: {court: [pl1, pl2],[pl3, pl4]}

    def add_players(self, name):
        '''Creates Player instance and adds to self._players dict.'''
        self._players[name] = Player(name)

    def get_players(self, show=None):
        if show == 'show':
            for player in self._players:
                print(player)
            return self._players
        else:
            return self._players

    def create_tournament(self, rounds, courts):
                        
        # ---------------------------------------------------------------------------------------------------
        # CALCULATING THE COMBINATIONS FOR GAMES (NOT PERMUTATION)
        # ---------------------------------------------------------------------------------------------------

        # Showing r-combinations for 8 players in teams of 2
        players = len(self._players)
        combo_team = combinations(range(1,players + 1),2)
        num_teams = 0
        list_teams = []
        for i in combo_team:
            list_teams.append(list(i))
            num_teams += 1
        print(f'There are {num_teams} teams possible with {players} players.')

        # Showing r-permutations for each team playing another
        num_games = 0
        list_games = []
        combo_game = combinations(list_teams, 2)
        for i in combo_game:
            list_games.append(list(i))
            num_games += 1
        print(f'There are {num_games} games possible from those {num_teams} teams.')

        # create a list of games where the north team and the south team share a team member
        game_removal_list = []
        for game in list_games:                     # iterate out each game: 2 teams, 4 players
            north_team = set(game[0])
            south_team = set(game[1])
            if (north_team & south_team):
                game_removal_list.append(game)    

        print(f'There are {len(game_removal_list)} games that share a team member, which leaves {num_games - len(game_removal_list)} games that can be played.')

        # remove the games that violate having the same player on both teams
        for removal in game_removal_list:
            list_games.remove(removal)

        # ---------------------------------------------------------------------------------------------------
        # DETERMINE HOW MANY COURTS ARE NEEDED AND HOW MANY BYES
        # ---------------------------------------------------------------------------------------------------

        # 4 players per court and extras are byes, with no player a bye more than once
        # min players = 8, min courts is 2
        # max players = 20, max courts is 5
        num_courts, byes = divmod(players, 4)


        # ---------------------------------------------------------------------------------------------------
        # CREATING PLACEHOLDERS DICTIONARIES FOR EACH ROUND AND A FULL GAME LIST
        # ---------------------------------------------------------------------------------------------------

        # initializing rounds 1 - 6; keys are "courts" and values are a list of lists where list[0] is north team, list[1] is south team
        tournament = {
            "Round 1"  : {},
            "Round 2"  : {},
            "Round 3"  : {},
            "Round 4"  : {},
            "Round 5"  : {},
            "Round 6"  : {}
            }

        # initialize a list of games to make sure none have been repeated
        full_game_list = []

        # initialize lists of players that have already been assigned to a game/court
        Player_List_per_Round = {
            "Round 1 Player List"  : [],
            "Round 2 Player List"  : [],
            "Round 3 Player List"  : [],
            "Round 4 Player List"  : [],
            "Round 5 Player List"  : [],
            "Round 6 Player List"  : []
            }
        # ---------------------------------------------------------------------------------------------------
        # ITERATE THROUGH EACH ROUND OF GAMES. TOURNAMENT DICTIONARY, FULL GAME LIST, AND ROUND PLAYER
        #   LISTS ARE ALL POPULATED.
        # ---------------------------------------------------------------------------------------------------

        round_count = 0
        for round in tournament:        # "round" is a key. tournament["round"] is the round dictionary
            round_count += 1
            which_round = "Round " + str(round_count)


        # initialize a counter for which court is being played on. 
            court_count = 0
            player_list_count = 0
            for games in list_games:

                # for the current tournament - check if the game has already been played
                if games not in full_game_list:
                    if games[0] not in full_game_list[:len(full_game_list) + 1] and games[1] not in full_game_list[:len(full_game_list) + 1]:
                        
                            which_player_list = which_round + " Player List"        

                            # for the current round - check if players on each North Team (games [0]) and South Team (games [1]) have already played 
                            # i.e., is disjoint with the player_list_per_round[]

                            if set(Player_List_per_Round[which_player_list]).isdisjoint(set(games[0])) and set(Player_List_per_Round[which_player_list]).isdisjoint(set(games[1])):
                                court_count += 1        # increment the court key
                                which_court = "court " + str(court_count)
                                tournament[which_round][which_court] = games
                                full_game_list.append(games)
                                Player_List_per_Round[which_player_list].append(tournament[which_round][which_court][0][0])
                                Player_List_per_Round[which_player_list].append(tournament[which_round][which_court][0][1])
                                Player_List_per_Round[which_player_list].append(tournament[which_round][which_court][1][0])
                                Player_List_per_Round[which_player_list].append(tournament[which_round][which_court][1][1])

        print(tournament)
