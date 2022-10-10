# Generated from C:/Users/barna/PycharmProjects/tabl\tabl.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .tablParser import tablParser
else:
    from tablParser import tablParser

# This class defines a complete generic visitor for a parse tree produced by tablParser.

class tablVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by tablParser#rules.
    def visitRules(self, ctx:tablParser.RulesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#title.
    def visitTitle(self, ctx:tablParser.TitleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#gameName.
    def visitGameName(self, ctx:tablParser.GameNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#playerCount.
    def visitPlayerCount(self, ctx:tablParser.PlayerCountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#numberOfPlayers.
    def visitNumberOfPlayers(self, ctx:tablParser.NumberOfPlayersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#contents.
    def visitContents(self, ctx:tablParser.ContentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#contentRule.
    def visitContentRule(self, ctx:tablParser.ContentRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#resourceRuleDef.
    def visitResourceRuleDef(self, ctx:tablParser.ResourceRuleDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#resourceRule.
    def visitResourceRule(self, ctx:tablParser.ResourceRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#resourceName.
    def visitResourceName(self, ctx:tablParser.ResourceNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#resourceNumber.
    def visitResourceNumber(self, ctx:tablParser.ResourceNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#commonDeckDef.
    def visitCommonDeckDef(self, ctx:tablParser.CommonDeckDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#cardList.
    def visitCardList(self, ctx:tablParser.CardListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#numberOfCardDef.
    def visitNumberOfCardDef(self, ctx:tablParser.NumberOfCardDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#numberOfCard.
    def visitNumberOfCard(self, ctx:tablParser.NumberOfCardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#phases.
    def visitPhases(self, ctx:tablParser.PhasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#phaseDef.
    def visitPhaseDef(self, ctx:tablParser.PhaseDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#phase.
    def visitPhase(self, ctx:tablParser.PhaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#phaseName.
    def visitPhaseName(self, ctx:tablParser.PhaseNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#actionDef.
    def visitActionDef(self, ctx:tablParser.ActionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#action.
    def visitAction(self, ctx:tablParser.ActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#doTimes.
    def visitDoTimes(self, ctx:tablParser.DoTimesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#actionName.
    def visitActionName(self, ctx:tablParser.ActionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#actionCardResource.
    def visitActionCardResource(self, ctx:tablParser.ActionCardResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#starting.
    def visitStarting(self, ctx:tablParser.StartingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#deckOfDef.
    def visitDeckOfDef(self, ctx:tablParser.DeckOfDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#personalDeckDef.
    def visitPersonalDeckDef(self, ctx:tablParser.PersonalDeckDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#listOfCards.
    def visitListOfCards(self, ctx:tablParser.ListOfCardsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#cardDefinitions.
    def visitCardDefinitions(self, ctx:tablParser.CardDefinitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#cardDefinition.
    def visitCardDefinition(self, ctx:tablParser.CardDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#cardNameAndPicture.
    def visitCardNameAndPicture(self, ctx:tablParser.CardNameAndPictureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#cardEffects.
    def visitCardEffects(self, ctx:tablParser.CardEffectsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#resourceEffectOrActionEffect.
    def visitResourceEffectOrActionEffect(self, ctx:tablParser.ResourceEffectOrActionEffectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#resourceEffectWithTarget.
    def visitResourceEffectWithTarget(self, ctx:tablParser.ResourceEffectWithTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#actionWithTarget.
    def visitActionWithTarget(self, ctx:tablParser.ActionWithTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#target.
    def visitTarget(self, ctx:tablParser.TargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#resourceEffect.
    def visitResourceEffect(self, ctx:tablParser.ResourceEffectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#delim.
    def visitDelim(self, ctx:tablParser.DelimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#modifyType.
    def visitModifyType(self, ctx:tablParser.ModifyTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#modifyNumber.
    def visitModifyNumber(self, ctx:tablParser.ModifyNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#cardName.
    def visitCardName(self, ctx:tablParser.CardNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#pictureName.
    def visitPictureName(self, ctx:tablParser.PictureNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#gameEnd.
    def visitGameEnd(self, ctx:tablParser.GameEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#endOrAndOr.
    def visitEndOrAndOr(self, ctx:tablParser.EndOrAndOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#gameEndConditionDef.
    def visitGameEndConditionDef(self, ctx:tablParser.GameEndConditionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#gameEndCondition.
    def visitGameEndCondition(self, ctx:tablParser.GameEndConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#gameEndConditionQuant.
    def visitGameEndConditionQuant(self, ctx:tablParser.GameEndConditionQuantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#gameEndMoreOrLess.
    def visitGameEndMoreOrLess(self, ctx:tablParser.GameEndMoreOrLessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#moreOrLess.
    def visitMoreOrLess(self, ctx:tablParser.MoreOrLessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tablParser#gameEndResource.
    def visitGameEndResource(self, ctx:tablParser.GameEndResourceContext):
        return self.visitChildren(ctx)



del tablParser