import itertools
import json
import FileStream as FileStream
from antlr4 import *
from random import shuffle
from functools import partial
from gen.TablParser import TablParser
from gen.TablVisitor import *
from gen.tablLexer import TablLexer
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import asyncio
import websockets


def draw(args, activatedBy):
    activatedBy.draw(args['number'])


def gainResource(args, activatedBy):
    activatedBy.gainResource(args['resourceName'], args['number'])


def spendResource(args, activatedBy):
    activatedBy.spendResource(args['resourceName'], args['number'])


class MyServer(BaseHTTPRequestHandler):
    def __init__(self, market, players, *args, **kwargs):
        self.market = market
        self.players = players
        super().__init__(*args, **kwargs)

    def do_GET(self):
        path = self.path.split('/')
        print(path)
        match path[1]:
            case 'cardList':
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(cardList, default=lambda o: o.__dict__,
                    sort_keys=True, indent=4), 'utf-8'))
            case 'market':
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(market, default=lambda o: o.__dict__,
                    sort_keys=True, indent=4), 'utf-8'))
        # self.wfile.write(bytes('\n', 'utf-8'))
        # self.wfile.write(bytes(json.dumps(players, default=lambda o: o.__dict__,
        #     sort_keys=True, indent=4), 'utf-8'))

class Resource:
    def __init__(self, name, limit, picture, options = []):
        self.name = name
        self.limit = limit
        self.supply = limit
        self.picture = picture
        self.visible = 'visible' in options
        self.perTurn = 'per-turn' in options
        #response = requests.get(f"https://api.pexels.com/v1/search?query={picture}", headers={"Authorization" : "563492ad6f917000010000014363b809657648f1a8b3df00ea4eb9e2"})
        #self.pictureUrl = response.json()['photos'][0]['src']['small']
        #print(self.pictureUrl)

    def __repr__(self):
        return f'{self.name}: {self.supply}, max: {self.limit}, visible: {self.visible}, per-turn: {self.perTurn}'

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
                        case 'draw':
                            self.whenPlayedActions.append(draw)
                            self.whenPlayedArgs.append({'number': effect['num']})
                case 'resource':
                    #if effect['resourceName'] in resourcesList.keys():
                        args = {'number': int(effect['number']), 'resourceName': effect['resourceName']}
                        self.whenPlayedArgs.append(args)
                        match effect['resourceEffect']:
                            case '+':
                                self.whenPlayedActions.append(gainResource)
                            case '-':
                                self.whenPlayedActions.append(spendResource)
        self.picture = picture


    def __repr__(self):
        return f'{self.name} ({self.id})'

    def play(self, activatedBy):
        for i in range(len(self.whenPlayedArgs)):
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

    def __repr__(self):
        return f'{self.name}: {self.resources}, deck: {self.deck}'

    def draw(self, num):
        cardsDrawn = self.deck.drawNFromDeck(num)
        for card in cardsDrawn:
            if card: self.hand.append(card)
        print(f'{self.name} drew {len(cardsDrawn)} cards ({cardsDrawn})')

    def gainResource(self, resourceName, num):
        oldNum = self.resources[resourceName]
        numToTake = Player.resourcesList[resourceName].take(num)
        self.resources[resourceName] += numToTake
        print(f'{self.name} took {numToTake} {resourceName} resources, they had {oldNum} and now have {self.resources[resourceName]}')

    def spendResource(self, resourceName, num, strict = True):
        oldNum = self.resources[resourceName]
        if strict and oldNum < num:
            return False
        numToSpend = Player.resourcesList[resourceName].restore(num)
        self.resources[resourceName] -= min(self.resources[resourceName], num)
        print(f'{self.name} spent {numToSpend} {resourceName} resources, they had {oldNum} and now have {self.resources[resourceName]}')
        return True

    def beginTurn(self):
        self.draw(5)

    def endTurn(self):
        for card in self.playedCards:
            self.deck.discard.append(card)
        for card in self.hand:
            self.deck.discard.append(card)
        self.playedCards.clear()
        self.hand.clear()

    def buyCard(self, cardId):
        cardToBuy = self.market.display[cardId]
        resource, quantity = cardToBuy.cost
        if self.spendResource(resource, quantity):
            self.deck.addCard(self.market.buyFromMarket(cardId))
            print(f"bought card {cardToBuy}")
        else:
            print("not enough resources to buy")


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


CLIENTS = set()
CLIENTSDICT = {}
ID = 0
PLAYERNUM = 2


async def handler(websocket):
    CLIENTS.add(websocket)
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        message = json.loads(message)
        print(message)
        match message['action']:
            case "ready":
                global ID
                CLIENTSDICT[ID] = websocket
                print(f"player {ID} registered")
                response = {"messageType": "playerId", "playerId": ID}
                ID += 1
                await websocket.send(json.dumps(response, default=lambda o: o.__dict__,
                                                sort_keys=True, indent=4))
                if ID == PLAYERNUM:
                    players[0].beginTurn()
                    for playerId, connection in CLIENTSDICT.items():
                        pl = players.copy()
                        currentPlayer = pl.pop(playerId)
                        resourcesToSend = [otherPlayer.resources for otherPlayer in pl]
                        response = {"messageType": "beginGame", 'market': market.display, 'player': currentPlayer, 'enemies': resourcesToSend, 'activePlayer': 0}
                        await connection.send(json.dumps(response, default=lambda o: o.__dict__,
                                                    sort_keys=True, indent=4))

            case "beginGame":
                response = {"messageType": 'playerInfo', 'players': players}
                await websocket.send(json.dumps(response, default=lambda o: o.__dict__,
                                                sort_keys=True, indent=4))
            case "marketRefresh":
                response = {"messageType" : 'marketRefresh', 'market' : {'display': market.display}}
                await websocket.send(json.dumps(response, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4))
                print("sent")
            case "playerInfo":
                response = {"messageType" : 'playerInfo', 'players' : players}
                await websocket.send(json.dumps(response, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4))
                print("sent")
            case "buyCard":
                currentPlayerId = message['playerId']
                print(players[currentPlayerId].resources)
                players[currentPlayerId].buyCard(message['cardId'])
                print(players[currentPlayerId].resources)
                response = {"messageType": 'marketRefresh', 'market': {'display': market.display}}
                for connection in CLIENTS:
                    await connection.send(json.dumps(response, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4))
                for playerId, connection in CLIENTSDICT.items():
                    pl = players.copy()
                    currentPlayer = pl.pop(playerId)
                    resourcesToSend = [otherPlayer.resources for otherPlayer in pl]
                    response = {"messageType": "playerInfo", 'player': currentPlayer, 'enemies': resourcesToSend}
                    await connection.send(json.dumps(response, default=lambda o: o.__dict__,
                                                     sort_keys=True, indent=4))

            case "playCard":
                currentPlayerId = message['playerId']
                cardsInHand = {card.id : card for card in players[currentPlayerId].hand}
                print(cardsInHand)
                cardsInHand[message['cardId']].play(players[currentPlayerId])
                print(players[currentPlayerId].resources)
                for playerId, connection in CLIENTSDICT.items():
                    pl = players.copy()
                    currentPlayer = pl.pop(playerId)
                    resourcesToSend = [otherPlayer.resources for otherPlayer in pl]
                    response = {"messageType": "playerInfo", 'player': currentPlayer, 'enemies': resourcesToSend}
                    await connection.send(json.dumps(response, default=lambda o: o.__dict__,
                                                     sort_keys=True, indent=4))
                print("sent")
            case "endTurn":
                currentPlayerId = message['playerId']
                players[currentPlayerId].endTurn()
                nextPlayerId = (currentPlayerId + 1) % PLAYERNUM
                players[nextPlayerId].beginTurn()
                for playerId, connection in CLIENTSDICT.items():
                    pl = players.copy()
                    currentPlayer = pl.pop(playerId)
                    resourcesToSend = [otherPlayer.resources for otherPlayer in pl]
                    response = {"messageType": "playerInfo", 'player': currentPlayer, 'enemies': resourcesToSend}
                    await connection.send(json.dumps(response, default=lambda o: o.__dict__,
                                                     sort_keys=True, indent=4))
                for connection in CLIENTS:
                    response = {"messageType": "activePlayer", "activePlayer": nextPlayerId}
                    await connection.send(json.dumps(response, default=lambda o: o.__dict__,
                                                    sort_keys=True, indent=4))



async def main():
    async with websockets.serve(handler, '', 8000):
        await asyncio.Future()

if __name__ == '__main__':
    inputStream = FileStream("sample.txt")
    lexer = TablLexer(inputStream)
    stream = CommonTokenStream(lexer)
    parser = TablParser(stream)
    tree = parser.rules()
    visitor = TablVisitor()
    visitor.visit(tree)
    commonDeck = commonDeck[0]
    print(f'List of resources: {resourcesList}')
    print(f'Common deck: {commonDeck}')
    print(f'Players: {players}')
    myCardList = cardList
    market = Market(5, False, commonDeck)
    for player in players:
        player.market = market
    # while True:
    #     players = itertools.cycle(players)
    #     activePlayer = next(players)
    #     activePlayer.beginTurn()
    #     print(f'cards in active player\'s hand: {activePlayer.hand}')
    #     activePlayer.buyCard(1)
    #     while len(activePlayer.hand) > 0:
    #         toPlay = input('index of card to be played: ')
    #         activeHand = {card.id : card for card in activePlayer.hand}
    #         activeHand[int(toPlay)].play(activePlayer)
    #         print(f'cards in active player\'s hand: {activePlayer.hand}')
    #         print(resourcesList)
    #     activePlayer.endTurn()




    # hostName = 'localhost'
    # serverPort = 8080
    #
    #
    # handler = partial(MyServer, market, players)
    # webServer = HTTPServer((hostName, serverPort), handler)
    # print(f'server started, http://{hostName}:{serverPort}')
    # try:
    #     webServer.serve_forever()
    # except KeyboardInterrupt:
    #     pass
    #
    # webServer.server_close()
    # print('server stopped')
    asyncio.run(main())

