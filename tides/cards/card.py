class Card:
    suits = ('Outer Gods', 'Locations', 'Manuscripts', 'Great Old Ones', 'Races')

    def __init__(self, id, name, suit, madness):
        self.id = id
        self.name = name
        self.suit = suit
        self.madness = madness
        self.ability = self.ability_score(id)
    
    def __str__(self):
        return self.name

    def ability_score(self, id):
        if id == 'NYA':
            return self.ability_nya
        elif id == 'YOG':
            return self.ability_yog
        elif id == 'AZA':
            return self.ability_aza
        
        elif id == 'RLY':
            return self.ability_rly
        elif id == 'INN':
            return self.ability_inn
        elif id == 'MOU':
            return self.ability_mou

        elif id == 'UNA':
            return self.ability_una
        elif id == 'PNA':
            return self.ability_pna
        elif id == 'NEC':
            return self.ability_nec

        elif id == 'DAG':
            return self.ability_dag
        elif id == 'CTH':
            return self.ability_cth
        elif id == 'HAS':
            return self.ability_has

        elif id == 'DEE':
            return self.ability_dee
        elif id == 'ELD':
            return self.ability_eld
        elif id == 'GRE':
            return self.ability_gre
        
        elif id == 'MIS':
            return self.ability_mis
        elif id == 'DRE':
            return self.ability_dre
        elif id == 'SHU':
            return self.ability_shu

        else:
            raise Exception('Invalid card')
    
    def ability_nya(self, board):
        '''
        For a set of Outer Gods, Locations, Manuscripts, Great Old Ones, and 
        Races, gain 13 VP
        '''
        cards = dict.fromkeys(self.suits, 0)
        
        for card in board.player_cards:
            if card.suit in self.suits:
                cards[card.suit] += 1

        if min(cards.values()) > 0:
            return 13

        return 0
    
    def ability_yog(self, board):
        '''
        For majority in Locations, gain 7 VP
        '''
        player_count = 0
        opponent_count = 0

        for player_card, opponent_card in zip(board.player_cards, board.opponent_cards):
            if player_card.suit == 'Locations':
                player_count += 1
            if opponent_card.suit == 'Locations':
                opponent_count += 1
        
        return 7 if player_count > opponent_count else 0
    
    def ability_aza(self, board):
        '''
        For each Great Old Ones, gain 3 VP
        '''
        count = 0

        for card in board.player_cards:
            if card.suit == 'Great Old Ones':
                count += 1

        return count * 3
    
    def ability_rly(self, board):
        '''
        For majority in Great Old Ones, gain 7 VP
        '''
        player_count = 0
        opponent_count = 0

        for player_card, opponent_card in zip(board.player_cards, board.opponent_cards):
            if player_card.suit == 'Great Old Ones':
                player_count += 1
            if opponent_card.suit == 'Great Old Ones':
                opponent_count += 1
        
        return 7 if player_count > opponent_count else 0
    
    def ability_inn(self, board):
        '''
        For each suit you don't have, gain 3 VP
        '''
        count = 0
        cards = dict.fromkeys(self.suits, 0)

        for card in board.player_cards:
            if card.suit != 'None':
                cards[card.suit] += 1

        for suit_count in cards.values():
            if suit_count == 0:
                count += 1

        return count * 3
    
    def ability_mou(self, board):
        '''
        For each Races, gain 3 VP
        '''
        count = 0

        for card in board.player_cards:
            if card.suit == 'Races':
                count += 1

        return count * 3
    
    def ability_una(self, board):
        '''
        For each Locations, gain 3 VP
        '''
        count = 0

        for card in board.player_cards:
            if card.suit == 'Locations':
                count += 1

        return count * 3
    
    def ability_pna(self, board):
        '''
        For majority in Outer Gods, gain 7 VP
        '''
        player_count = 0
        opponent_count = 0

        for player_card, opponent_card in zip(board.player_cards, board.opponent_cards):
            if player_card.suit == 'Outer Gods':
                player_count += 1
            if opponent_card.suit == 'Outer Gods':
                opponent_count += 1
        
        return 7 if player_count > opponent_count else 0
    
    def ability_nec(self, board):
        '''
        For each Madness, gain 1 VP
        '''
        count = 0
        for card in board.player_cards:
            count += card.madness

        return count
    
    def ability_dag(self, board):
        '''
        For majority in Races, gain 7 VP
        '''
        player_count = 0
        opponent_count = 0

        for player_card, opponent_card in zip(board.player_cards, board.opponent_cards):
            if player_card.suit == 'Races':
                player_count += 1
            if opponent_card.suit == 'Races':
                opponent_count += 1
        
        return 7 if player_count > opponent_count else 0
    
    def ability_cth(self, board):
        '''
        For each set of Outer Gods, Locations, and Races, gain 9 VP
        '''
        cards = dict.fromkeys(['Outer Gods', 'Locations', 'Races'], 0)
        
        for card in board.player_cards:
            if card.suit in cards:
                cards[card.suit] += 1

        return min(cards.values()) * 9
    
    def ability_has(self, board):
        '''
        For each Manuscripts, gain 3 VP
        '''
        count = 0

        for card in board.player_cards:
            if card.suit == 'Manuscripts':
                count += 1

        return count * 3
    
    def ability_dee(self, board):
        '''
        For each set of Great Old Ones and Manuscripts, gain 6 VP
        '''
        cards = dict.fromkeys(['Great Old Ones', 'Manuscripts'], 0)
        
        for card in board.player_cards:
            if card.suit in cards:
                cards[card.suit] += 1

        return min(cards.values()) * 6
    
    def ability_eld(self, board):
        '''
        For each Outer Gods, gain 3 VP
        '''
        count = 0

        for card in board.player_cards:
            if card.suit == 'Outer Gods':
                count += 1

        return count * 3
    
    def ability_gre(self, board):
        '''
        For majority in Manuscripts, gain 7 VP
        '''
        player_count = 0
        opponent_count = 0

        for player_card, opponent_card in zip(board.player_cards, board.opponent_cards):
            if player_card.suit == 'Manuscripts':
                player_count += 1
            if opponent_card.suit == 'Manuscripts':
                opponent_count += 1
        
        return 7 if player_count > opponent_count else 0
    
    def ability_mis(self, board):
        '''
        For each majority, gain 4 VP
        '''
        count = 0

        player = dict.fromkeys(self.suits, 0)
        opponent = dict.fromkeys(self.suits, 0)

        for player_card, opponent_card in zip(board.player_cards, board.opponent_cards):
            if player_card.suit in self.suits:
                player[player_card.suit] += 1
            if opponent_card.suit in self.suits:
                opponent[opponent_card.suit] += 1

        for suit in player:
            if player[suit] > opponent[suit]:
                count += 1

        return count * 4
    
    def ability_dre(self, board):
        '''
        For each minority, gain 1 VP
        Note: this ability has been modified due to difficulty of implementing
              original ability
        '''
        count = 0

        player = dict.fromkeys(self.suits, 0)
        opponent = dict.fromkeys(self.suits, 0)

        for player_card, opponent_card in zip(board.player_cards, board.opponent_cards):
            if player_card.suit in self.suits:
                player[player_card.suit] += 1
            if opponent_card.suit in self.suits:
                opponent[opponent_card.suit] += 1

        for suit in player:
            if player[suit] < opponent[suit]:
                count += 1

        return count
    
    def ability_shu(self, board):
        '''
        Double the VP of your previously played card
        '''
        if board.player_cards[0].id == 'SHU':
            return 0

        previous_card = None

        for index, card in enumerate(board.player_cards):
            if card.id == 'SHU':
                previous_card = board.player_cards[index - 1]

        return self.ability_score(previous_card.id)(board)
        