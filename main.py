import itertools
import json
import FileStream as FileStream
from antlr4 import *
from functools import partial
from gen.TablParser import TablParser
from gen.TablVisitor import *
from gen.tablLexer import TablLexer
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import asyncio
import websockets
from globals import *
from classes import *


def spendResourceEnemy(args, activatedBy):
    target = {player.nickName: player for player in players}[args['target']]
    target.spendResource(args['resourceName'], args['number'])


def gainResourceEnemy(args, activatedBy):
    target = {player.nickName: player for player in players}[args['target']]
    target.gainResource(args['resourceName'], args['number'])


def discardEnemy(args, activatedBy):
    target = {player.nickName: player for player in players}[args['target']]
    target.discard(args['number'])


def scrap(args, activatedBy):
    activatedBy.scrap(args['number'])


def discard(args, activatedBy):
    activatedBy.discard(args['number'])


def draw(args, activatedBy):
    activatedBy.draw(args['number'])


def drawEnemy(args, activatedBy):
    target = {player.nickName: player for player in players}[args['target']]
    target.draw(args['number'])


def gainResource(args, activatedBy):
    activatedBy.gainResource(args['resourceName'], args['number'])


def spendResource(args, activatedBy):
    activatedBy.spendResource(args['resourceName'], args['number'])


async def sendResponse(connection, response):
    await connection.send(json.dumps(response, default=lambda o: o.__dict__,
                                     sort_keys=True, indent=4))


def generatePlayerInfo(playerId):
    pl = players.copy()
    currentPlayer = pl.pop(playerId)
    resourcesToSend = {otherPlayer.nickName: otherPlayer.resources for otherPlayer in pl}
    return currentPlayer, resourcesToSend


CLIENTS = set()
CLIENTSDICT = {}
ID = 0
PLAYERNUM = 2


def checkEndGameConditions():
    for player in players:
        for conditionSet in endGameConditions:
            conditionsMet = True
            for condition in conditionSet:
                if 'comparator' not in condition.keys():
                    if player.resources[condition['resource']] != condition['number']:
                        conditionsMet = False
                elif condition['comparator'] == 'more':
                    if player.resources[condition['resource']] < condition['number']:
                        conditionsMet = False
                elif condition['comparator'] == 'less':
                    if player.resources[condition['resource']] > condition['number']:
                        conditionsMet = False
            if conditionsMet:
                return True
    return False


def checkWinner():
    winner = players[0]
    winners = []
    for player in players:
        if player != winner:
            if winCon['comparator'] == 'more':
                if player.resources[winCon['resourceName']] > winner.resources[winCon['resourceName']]:
                    winner = player
                elif player.resources[winCon['resourceName']] == winner.resources[winCon['resourceName']]:
                    winners.append(winner)
                    winners.append(player)
            elif winCon['comparator'] == 'less':
                if player.resources[winCon['resourceName']] < winner.resources[winCon['resourceName']]:
                    winner = player
                elif player.resources[winCon['resourceName']] == winner.resources[winCon['resourceName']]:
                    winners.append(winner)
                    winners.append(player)
    toRet = {'winner': winners, 'tie': True} if len(winners) > 0 else {'winner': winner, 'tie': False}
    print(toRet)
    return toRet


async def handler(websocket):
    CLIENTS.add(websocket)
    global market
    global commonDeck
    global tablParsed
    global scrapPile
    global endGameConditions
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        message = json.loads(message)
        print(message)
        match message['action']:

            case "gameFile":
                lexer = TablLexer(InputStream(message['tablText']))
                stream = CommonTokenStream(lexer)
                parser = TablParser(stream)
                tree = parser.rules()
                visitor = TablVisitor()
                visitor.visit(tree)
                commonDeck = commonDeck[0]
                endGameConditions = endGameConditions[0]
                print(f'List of resources: {resourcesList}')
                print(f'Common deck: {commonDeck}')
                print(f'Players: {players}')
                print(f'end game conditions: {endGameConditions}')
                market = Market(5, False, commonDeck)
                for player in players:
                    player.market = market
                tablParsed = True
                response = {"messageType": "tablParsed", "success": True}
                for connection in CLIENTS:
                    await sendResponse(connection, response)

            case "ready":
                global ID
                CLIENTSDICT[ID] = websocket
                print(f"player {ID} registered")
                players[ID].nickName = message['nickName']
                response = {"messageType": "playerId", "playerId": ID}
                ID += 1
                await sendResponse(websocket, response)
                if ID == PLAYERNUM:
                    for pl in players:
                        pl.beginGame()
                    players[0].active = True
                    for playerId, connection in CLIENTSDICT.items():
                        currentPlayer, resourcesToSend = generatePlayerInfo(playerId)
                        response = {"messageType": "beginGame", 'market': market.display, 'player': currentPlayer,
                                    'enemies': resourcesToSend, 'activePlayer': 0, 'scrap': scrapPile, 'limits': playLimits}
                        await sendResponse(connection, response)

            case "buyCard":
                currentPlayerId = message['playerId']
                print(players[currentPlayerId].resources)
                currentPlayer = players[currentPlayerId]
                if 'buy' in playLimits.keys() and currentPlayer.cardsBoughtThisTurn >= playLimits['buy']:
                    response = {'messageType': 'buyLimitReached'}
                    await sendResponse(websocket, response)
                else:
                    currentPlayer.buyCard(message['cardId'])
                    print(players[currentPlayerId].resources)
                    response = {"messageType": 'marketRefresh', 'market': {'display': market.display}}
                    for connection in CLIENTS:
                        await sendResponse(connection, response)
                    for playerId, connection in CLIENTSDICT.items():
                        currentPlayer, resourcesToSend = generatePlayerInfo(playerId)
                        response = {"messageType": "playerInfo", 'player': currentPlayer, 'enemies': resourcesToSend,
                                    'scrap': scrapPile}
                        await sendResponse(connection, response)

            case "playCard":
                currentPlayerId = message['playerId']
                currentPlayer = players[currentPlayerId]
                if 'play' in playLimits.keys() and currentPlayer.cardsPlayedThisTurn >= playLimits['play']:
                    response = {'messageType': 'playLimitReached'}
                    await sendResponse(websocket, response)
                else:
                    cardsInHand = {card.id: card for card in currentPlayer.hand}
                    if 'target' in message.keys():
                        cardsInHand[message['cardId']].play(currentPlayer, message['target'])
                    else:
                        cardsInHand[message['cardId']].play(currentPlayer)
                    currentPlayer.cardsPlayedThisTurn += 1
                    for playerId, connection in CLIENTSDICT.items():
                        currentPlayer, resourcesToSend = generatePlayerInfo(playerId)
                        response = {"messageType": "playerInfo", 'player': currentPlayer, 'enemies': resourcesToSend,
                                    'scrap': scrapPile}
                        await sendResponse(connection, response)

            case "endTurn":
                if checkEndGameConditions():
                    winDict = checkWinner()
                    response = {"messageType": "endGame", "tie": winDict['tie'], "winner": winDict['winner']}
                    for connection in CLIENTS:
                        await sendResponse(connection, response)
                else:
                    currentPlayerId = message['playerId']
                    players[currentPlayerId].endTurn()
                    nextPlayerId = (currentPlayerId + 1) % PLAYERNUM
                    players[nextPlayerId].beginTurn()
                    for playerId, connection in CLIENTSDICT.items():
                        currentPlayer, resourcesToSend = generatePlayerInfo(playerId)
                        response = {"messageType": "playerInfo", 'player': currentPlayer, 'enemies': resourcesToSend,
                                    'scrap': scrapPile}
                        await sendResponse(connection, response)
                    for connection in CLIENTS:
                        response = {"messageType": "activePlayer", "activePlayer": nextPlayerId,
                                    "discard": players[nextPlayerId].toDiscard}
                        await sendResponse(connection, response)

            case "checkTablParsed":
                if tablParsed:
                    response = {"messageType": "tablParsed", "success": True}
                    await sendResponse(websocket, response)

            case 'discard':
                players[message['playerId']].discardCard(message['cardId'])
                for playerId, connection in CLIENTSDICT.items():
                    currentPlayer, resourcesToSend = generatePlayerInfo(playerId)
                    response = {"messageType": "playerInfo", 'player': currentPlayer, 'enemies': resourcesToSend,
                                'scrap': scrapPile}
                    await sendResponse(connection, response)

            case 'scrap':
                scrapPile.append(players[message['playerId']].scrapCard(message['cardId']))
                for playerId, connection in CLIENTSDICT.items():
                    currentPlayer, resourcesToSend = generatePlayerInfo(playerId)
                    response = {"messageType": "playerInfo", 'player': currentPlayer, 'enemies': resourcesToSend,
                                'scrap': scrapPile}
                    await sendResponse(connection, response)


async def main():
    async with websockets.serve(handler, '', 8000):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
