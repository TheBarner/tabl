# Generated from C:/Users/barna/PycharmProjects/tabl\Tabl.g4 by ANTLR 4.10.1
from antlr4 import *
import main
if __name__ is not None and "." in __name__:
    from .TablParser import TablParser
else:
    from TablParser import TablParser

# This class defines a complete generic visitor for a parse tree produced by TablParser.

cardList = []
cardArgs = {}
resourcesList = {}
commonDeckCardList = []
commonDeck = []
playerCount = 2
players = []


class TablVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TablParser#rules.
    def visitRules(self, ctx:TablParser.RulesContext):
        self.visit(ctx.listOfCards())
        self.visit(ctx.contents())
        self.visit(ctx.starting())
        print(cardArgs)


    # Visit a parse tree produced by TablParser#title.
    def visitTitle(self, ctx:TablParser.TitleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#gameName.
    def visitGameName(self, ctx:TablParser.GameNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#playerCount.
    def visitPlayerCount(self, ctx:TablParser.PlayerCountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#numberOfPlayers.
    def visitNumberOfPlayers(self, ctx:TablParser.NumberOfPlayersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#contents.
    def visitContents(self, ctx:TablParser.ContentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#contentRule.
    def visitContentRule(self, ctx:TablParser.ContentRuleContext):
        for resourceRule in ctx.resourceRuleDef():
            resourceArgs = self.visit(resourceRule)
            resource = main.Resource(*resourceArgs)
            resourcesList[resource.name] = resource
        commonDeckDef = self.visit(ctx.commonDeckDef())
        for cardName in commonDeckDef.keys():
            for __ in range(commonDeckDef[cardName]):
                commonDeckCardList.append(main.Card(*cardArgs[cardName]))
        commonDeck.append(main.Deck(commonDeckCardList))



    # Visit a parse tree produced by TablParser#resourceRuleDef.
    def visitResourceRuleDef(self, ctx:TablParser.ResourceRuleDefContext):
        options = []
        if ctx.resourceOptions(): options = self.visit(ctx.resourceOptions())
        name, maxNum = self.visit(ctx.resourceRule())
        if maxNum == "unlimited": maxNum = 0
        return name, int(maxNum), 'placeholder', options


    # Visit a parse tree produced by TablParser#resourceRule.
    def visitResourceRule(self, ctx:TablParser.ResourceRuleContext):
        return self.visit(ctx.resourceName()), self.visit(ctx.resourceNumber())


    # Visit a parse tree produced by TablParser#resourceOptions.
    def visitResourceOptions(self, ctx:TablParser.ResourceOptionsContext):
        options = [option.getText() for option in ctx.RESOURCEOPTION()]
        return options



    # Visit a parse tree produced by TablParser#resourceName.
    def visitResourceName(self, ctx:TablParser.ResourceNameContext):
        return ctx.getText().strip('\'')


    # Visit a parse tree produced by TablParser#resourceNumber.
    def visitResourceNumber(self, ctx:TablParser.ResourceNumberContext):
        return ctx.getText()


    # Visit a parse tree produced by TablParser#commonDeckDef.
    def visitCommonDeckDef(self, ctx:TablParser.CommonDeckDefContext):
        return self.visit(ctx.cardList())


    # Visit a parse tree produced by TablParser#cardList.
    def visitCardList(self, ctx:TablParser.CardListContext):
        cardDict = {}
        for numCardDef in ctx.numberOfCardDef():
            number, name = self.visit(numCardDef)
            cardDict[name] = number
        return cardDict


    # Visit a parse tree produced by TablParser#numberOfCardDef.
    def visitNumberOfCardDef(self, ctx:TablParser.NumberOfCardDefContext):
        return self.visit(ctx.numberOfCard())


    # Visit a parse tree produced by TablParser#numberOfCard.
    def visitNumberOfCard(self, ctx:TablParser.NumberOfCardContext):
        return int(ctx.NUMBER().getText()), ctx.NAME().getText().strip('\'')


    # Visit a parse tree produced by TablParser#phases.
    def visitPhases(self, ctx:TablParser.PhasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#phaseDef.
    def visitPhaseDef(self, ctx:TablParser.PhaseDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#phase.
    def visitPhase(self, ctx:TablParser.PhaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#phaseName.
    def visitPhaseName(self, ctx:TablParser.PhaseNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#actionDef.
    def visitActionDef(self, ctx:TablParser.ActionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#action.
    def visitAction(self, ctx:TablParser.ActionContext):
        return {'actionName': self.visit(ctx.actionName()), 'num': self.visit(ctx.doTimes()), 'cardOrResource': self.visit(ctx.actionCardResource())}


    # Visit a parse tree produced by TablParser#doTimes.
    def visitDoTimes(self, ctx:TablParser.DoTimesContext):
        return ctx.getText()


    # Visit a parse tree produced by TablParser#actionName.
    def visitActionName(self, ctx:TablParser.ActionNameContext):
        return ctx.getText()


    # Visit a parse tree produced by TablParser#actionCardResource.
    def visitActionCardResource(self, ctx:TablParser.ActionCardResourceContext):
        return ctx.getText()


    # Visit a parse tree produced by TablParser#starting.
    def visitStarting(self, ctx:TablParser.StartingContext):
        startingResources = {}
        for resourceRule in ctx.resourceRuleDef():
            name, num, _, _ = self.visit(resourceRule)
            startingResources[name] = num
        personalDeckDef = self.visit(ctx.deckOfDef())
        for i in range(playerCount):
            personalDeckList = []
            for cardName in personalDeckDef.keys():
                for __ in range(personalDeckDef[cardName]):
                    personalDeckList.append(main.Card(*cardArgs[cardName]))
            players.append(main.Player(startingResources.copy(), 'player ' + str(i), resourcesList, main.Deck(personalDeckList)))
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#deckOfDef.
    def visitDeckOfDef(self, ctx:TablParser.DeckOfDefContext):
        return self.visit(ctx.personalDeckDef())


    # Visit a parse tree produced by TablParser#personalDeckDef.
    def visitPersonalDeckDef(self, ctx:TablParser.PersonalDeckDefContext):
        return self.visit(ctx.cardList())


    # Visit a parse tree produced by TablParser#listOfCards.
    def visitListOfCards(self, ctx:TablParser.ListOfCardsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#cardDefinitions.
    def visitCardDefinitions(self, ctx:TablParser.CardDefinitionsContext):
        for cardDef in ctx.cardDefinition():
            self.visit(cardDef)


    # Visit a parse tree produced by TablParser#cardDefinition.
    def visitCardDefinition(self, ctx:TablParser.CardDefinitionContext):
        cardInfo = {}
        namePicInfo = self.visit(ctx.cardNameAndPicture())
        cardInfo['cardName'] = namePicInfo['name']
        cardInfo['cardPicture'] = namePicInfo['pic']
        cardInfo['effects'] = []
        for cardEffect in ctx.cardEffect():
            cardInfo['effects'].append(self.visit(cardEffect))
        cardList.append(main.Card(cardInfo['cardName'], cardInfo['effects'], cardInfo['cardPicture']))
        cardArgs[cardInfo['cardName']] = cardInfo['cardName'], cardInfo['effects'], cardInfo['cardPicture']



    # Visit a parse tree produced by TablParser#cardNameAndPicture.
    def visitCardNameAndPicture(self, ctx:TablParser.CardNameAndPictureContext):
        namePicInfo = {}
        namePicInfo['name'] = self.visit(ctx.cardName())
        namePicInfo['pic'] = self.visit(ctx.pictureName())
        return namePicInfo


    # Visit a parse tree produced by TablParser#cardEffect.
    def visitCardEffect(self, ctx:TablParser.CardEffectContext):
        return self.visit(ctx.resourceEffectOrActionEffect())


    # Visit a parse tree produced by TablParser#resourceEffectOrActionEffect.
    def visitResourceEffectOrActionEffect(self, ctx:TablParser.ResourceEffectOrActionEffectContext):
        if ctx.actionWithTarget(): return self.visit(ctx.actionWithTarget())
        elif ctx.resourceEffectWithTarget(): return self.visit(ctx.resourceEffectWithTarget())


    # Visit a parse tree produced by TablParser#resourceEffectWithTarget.
    def visitResourceEffectWithTarget(self, ctx:TablParser.ResourceEffectWithTargetContext):
        info = {}
        info['type'] = 'resource'
        if ctx.target(): info['target'] = self.visit(ctx.target())
        info['effect'] = self.visit(ctx.resourceEffect())
        return info


    # Visit a parse tree produced by TablParser#actionWithTarget.
    def visitActionWithTarget(self, ctx:TablParser.ActionWithTargetContext):
        info = {}
        info['type'] = 'action'
        if ctx.target(): info['target'] = self.visit(ctx.target())
        info['effect'] = self.visit(ctx.action())
        return info


    # Visit a parse tree produced by TablParser#target.
    def visitTarget(self, ctx:TablParser.TargetContext):
        return ctx.getText()


    # Visit a parse tree produced by TablParser#resourceEffect.
    def visitResourceEffect(self, ctx:TablParser.ResourceEffectContext):
        return {'resourceName': self.visit(ctx.resourceName()), 'resourceEffect': self.visit(ctx.modifyType()), 'number': self.visit(ctx.modifyNumber())}


    # Visit a parse tree produced by TablParser#delim.
    def visitDelim(self, ctx:TablParser.DelimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#modifyType.
    def visitModifyType(self, ctx:TablParser.ModifyTypeContext):
        return ctx.getText()


    # Visit a parse tree produced by TablParser#modifyNumber.
    def visitModifyNumber(self, ctx:TablParser.ModifyNumberContext):
        return ctx.getText()


    # Visit a parse tree produced by TablParser#cardName.
    def visitCardName(self, ctx:TablParser.CardNameContext):
        return ctx.getText().strip('\'')


    # Visit a parse tree produced by TablParser#pictureName.
    def visitPictureName(self, ctx:TablParser.PictureNameContext):
        return ctx.getText().strip('\'').strip('~')


    # Visit a parse tree produced by TablParser#gameEnd.
    def visitGameEnd(self, ctx:TablParser.GameEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#endOrAndOr.
    def visitEndOrAndOr(self, ctx:TablParser.EndOrAndOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#gameEndConditionDef.
    def visitGameEndConditionDef(self, ctx:TablParser.GameEndConditionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#gameEndCondition.
    def visitGameEndCondition(self, ctx:TablParser.GameEndConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#gameEndConditionQuant.
    def visitGameEndConditionQuant(self, ctx:TablParser.GameEndConditionQuantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#gameEndMoreOrLess.
    def visitGameEndMoreOrLess(self, ctx:TablParser.GameEndMoreOrLessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#moreOrLess.
    def visitMoreOrLess(self, ctx:TablParser.MoreOrLessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TablParser#gameEndResource.
    def visitGameEndResource(self, ctx:TablParser.GameEndResourceContext):
        return self.visitChildren(ctx)



del TablParser