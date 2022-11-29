
from random import shuffle
from main import draw, discardEnemy, gainResource, spendResource, discard, resourcesList, gainResourceEnemy, spendResourceEnemy, drawEnemy, scrap
from globals import prepPhase, cleanupPhase


class Resource:
    def __init__(self, name, limit, picture, options = []):
        self.name = name
        self.limit = limit
        self.supply = limit
        self.picture = picture
        self.visible = 'visible' in options
        self.perTurn = 'per-turn' in options
        self.strict = 'strict' in options
        #response = requests.get(f"https://api.pexels.com/v1/search?query={picture}", headers={"Authorization" : "563492ad6f917000010000014363b809657648f1a8b3df00ea4eb9e2"})
        #self.pictureUrl = response.json()['photos'][0]['src']['small']
        #print(self.pictureUrl)

    def __repr__(self):
        return f'{self.name}: {self.supply}, max: {self.limit}, visible: {self.visible}, per-turn: {self.perTurn}, strict: {self.strict}'

    def take(self, num):
        if self.limit == 0:
            return num
        if self.supply > 0:
            toRet = min(num, self.supply)
            self.supply = max(0, self.supply - num)
            return toRet
        return 0

    def restore(self, num):
        if self.limit != 0:
            self.supply += num
        return num


class Card():
    id = 0
    def __init__(self, name, whenPlayedList, picture, effectsDisplay, cost=None):
        self.id = Card.id
        Card.id += 1
        self.effectsDisplay = effectsDisplay
        self.cost = cost
        self.name = name
        self.whenPlayedArgs = []
        self.whenPlayedActions = []
        for whenPlayed in whenPlayedList:
            effect = whenPlayed['effect']
            match whenPlayed['type']:
                case 'action':
                    match effect['actionName']:
                        case 'scrap':
                            self.whenPlayedActions.append(scrap)
                            self.whenPlayedArgs.append({'number': int(effect['num'])})
                        case 'draw':
                            if 'target' in whenPlayed.keys() and whenPlayed['target']:
                                self.whenPlayedActions.append(drawEnemy)
                                self.whenPlayedArgs.append({'target' : True, 'number': int(effect['num'])})
                            else:
                                self.whenPlayedActions.append(draw)
                                self.whenPlayedArgs.append({'number': int(effect['num'])})
                        case 'discard':
                            if 'target' in whenPlayed.keys() and whenPlayed['target']:
                                self.whenPlayedActions.append(discardEnemy)
                                self.whenPlayedArgs.append({'target' : True, 'number': int(effect['num'])})
                            else:
                                self.whenPlayedActions.append(discard)
                                self.whenPlayedArgs.append({'number': int(effect['num'])})

                case 'resource':
                    #if effect['resourceName'] in resourcesList.keys():
                        if 'target' in whenPlayed.keys() and whenPlayed['target']:
                            args = {'number': int(effect['number']), 'resourceName': effect['resourceName'], 'target': True}
                            match effect['resourceEffect']:
                                case '+':
                                    self.whenPlayedActions.append(gainResourceEnemy)
                                case '-':
                                    self.whenPlayedActions.append(spendResourceEnemy)
                        else:
                            args = {'number': int(effect['number']), 'resourceName': effect['resourceName']}
                            match effect['resourceEffect']:
                                case '+':
                                    self.whenPlayedActions.append(gainResource)
                                case '-':
                                    self.whenPlayedActions.append(spendResource)
                        self.whenPlayedArgs.append(args)

        self.picture = picture


    def __repr__(self):
        return f'{self.name} ({self.id})'

    def play(self, activatedBy, target = None):
        for i in range(len(self.whenPlayedArgs)):
            if 'target' in self.whenPlayedArgs[i].keys():
                self.whenPlayedArgs[i]['target'] = target
            self.whenPlayedActions[i](self.whenPlayedArgs[i], activatedBy)
        activatedBy.playedCards.append(self)
        activatedBy.hand.remove(self)


class Deck:
    def __init__(self, cardList = []):
        self.cardList = cardList
        self.inDeck = []
        self.discard = list.copy(cardList)
        self.shuffleDeck()

    def __repr__(self):
        cards = []
        for card in self.cardList:
            cards.append(card.__repr__())
        return f"[[{', '.join(cards)}]]"

    def shuffleDeck(self):
        self.inDeck = list.copy(self.discard)
        self.discard.clear()
        shuffle(self.inDeck)
        print('shuffling deck!')

    def drawNFromDeck(self, num):
        cardsDrawn = []
        for _ in range(int(num)):
            cardsDrawn.append(self.draw())
        return cardsDrawn

    def draw(self):
        if len(self.inDeck) == 0 and len(self.discard) != 0:
            self.shuffleDeck()
        return self.inDeck.pop() if len(self.inDeck) != 0 else False

    def addCard(self, card):
        self.discard.append(card)
        self.cardList.append(card)

    def discardCard(self, card):
        self.discard.append(card)


class Player:
    resourcesList = []
    def __init__(self, resources, playerName, allResources, deck = Deck()):
        Player.resourcesList = allResources
        self.resources = {}
        for resource, number in resources.items():
            self.resources[resource] = number
        self.name = playerName
        self.playedCards = []
        self.hand = []
        self.deck = deck
        self.active = False
        self.toDiscard = 0
        self.toScrap = 0
        self.cardsPlayedThisTurn = 0
        self.cardsBoughtThisTurn = 0

    def __repr__(self):
        return f'{self.name}: {self.resources}, deck: {self.deck}'

    def draw(self, num):
        cardsDrawn = self.deck.drawNFromDeck(num)
        for card in cardsDrawn:
            if card: self.hand.append(card)
        print(f'{self.name} drew {len(cardsDrawn)} cards ({cardsDrawn})')

    def gainResource(self, resourceName, num):
        print(self.resources)
        oldNum = self.resources[resourceName]
        numToTake = Player.resourcesList[resourceName].take(num)
        self.resources[resourceName] += numToTake
        print(f'{self.name} took {numToTake} {resourceName} resources, they had {oldNum} and now have {self.resources[resourceName]}')

    def spendResource(self, resourceName, num):
        oldNum = self.resources[resourceName]
        strict = Player.resourcesList[resourceName].strict
        if strict and oldNum < num:
            return False
        numToSpend = Player.resourcesList[resourceName].restore(num)
        self.resources[resourceName] -= min(self.resources[resourceName], num)
        print(f'{self.name} spent {numToSpend} {resourceName} resources, they had {oldNum} and now have {self.resources[resourceName]}')
        return True

    def beginGame(self):
        for action in prepPhase:
            if action['actionName'] == 'draw':
                self.draw(action['num'])
                return
        for action in cleanupPhase:
            if action['actionName'] == 'draw':
                self.draw(action['num'])
                return

    def beginTurn(self):
        self.active = True
        self.phaseActions("preparation")

    def endTurn(self):
        for card in self.playedCards:
            self.deck.discard.append(card)
        self.active = False
        self.losePerTurns()
        self.phaseActions('cleanup')

    def phaseActions(self, phase):
        currentPhase = False
        if phase == 'preparation':
            currentPhase = prepPhase
        elif phase == 'cleanup':
            currentPhase = cleanupPhase
        if currentPhase:
            for action in currentPhase:
                if action['actionName'] == 'discard':
                    if action['num'] == 'all':
                        for card in self.hand:
                            self.deck.discard.append(card)
                        self.playedCards.clear()
                        self.hand.clear()
                if action['actionName'] == 'draw':
                    self.draw(action['num'])

    def buyCard(self, cardId):
        cardToBuy = self.market.display[cardId]
        resource, quantity = cardToBuy.cost
        if self.spendResource(resource, quantity):
            self.deck.addCard(self.market.buyFromMarket(cardId))
            self.cardsBoughtThisTurn += 1
            print(f"bought card {cardToBuy}")
        else:
            print("not enough resources to buy")

    def discard(self, number):
        self.toDiscard += number

    def discardCard(self, cardId):
        cardToDiscard = {card.id: card for card in self.hand}[cardId]
        self.hand.remove(cardToDiscard)
        self.deck.discardCard(cardToDiscard)
        self.toDiscard -= 1

    def losePerTurns(self):
        print(resourcesList)
        self.cardsBoughtThisTurn = 0
        self.cardsPlayedThisTurn = 0
        for resource in resourcesList.keys():
            if resourcesList[resource].perTurn:
                self.resources[resource] = 0

    def scrap(self, number):
        self.toScrap += number

    def scrapCard(self, cardId):
        cardToScrap = {card.id: card for card in self.hand}[cardId]
        self.hand.remove(cardToScrap)
        self.deck.cardList.remove(cardToScrap)
        self.toScrap -= 1
        return cardToScrap


class Market:
    def __init__(self, numOfCards, permanent, deck):
        self.numOfCards = numOfCards
        self.permanent = permanent
        self.deck = deck
        self.display = {}
        for i in range(0, numOfCards):
            drawnCard = self.deck.draw()
            self.display[drawnCard.id] = drawnCard

    def buyFromMarket(self, cardId):
        toBuy = self.display[cardId]
        print(f'{self.permanent}')
        if not self.permanent:
            drawnCard = self.deck.draw()
            self.display[drawnCard.id] = drawnCard
            del self.display[cardId]
            print(f'{self.display}')
        return toBuy

