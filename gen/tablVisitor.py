# Generated from C:/Users/barna/PycharmProjects/tabl\Tabl.g4 by ANTLR 4.10.1
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .TablParser import TablParser
else:
    from TablParser import TablParser


# This class defines a complete generic visitor for a parse tree produced by TablParser.

class TablVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TablParser#rules.
    def visitRules(self, ctx: TablParser.RulesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#title.
    def visitTitle(self, ctx: TablParser.TitleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#gameName.
    def visitGameName(self, ctx: TablParser.GameNameContext):
        print("the title of the game is " + ctx.getText())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#playerCount.
    def visitPlayerCount(self, ctx: TablParser.PlayerCountContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#numberOfPlayers.
    def visitNumberOfPlayers(self, ctx: TablParser.NumberOfPlayersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#contents.
    def visitContents(self, ctx: TablParser.ContentsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#contentRule.
    def visitContentRule(self, ctx: TablParser.ContentRuleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#resourceRuleDef.
    def visitResourceRuleDef(self, ctx: TablParser.ResourceRuleDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#resourceRule.
    def visitResourceRule(self, ctx: TablParser.ResourceRuleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#resourceName.
    def visitResourceName(self, ctx: TablParser.ResourceNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#resourceNumber.
    def visitResourceNumber(self, ctx: TablParser.ResourceNumberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#commonDeckDef.
    def visitCommonDeckDef(self, ctx: TablParser.CommonDeckDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#cardList.
    def visitCardList(self, ctx: TablParser.CardListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#numberOfCardDef.
    def visitNumberOfCardDef(self, ctx: TablParser.NumberOfCardDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#numberOfCard.
    def visitNumberOfCard(self, ctx: TablParser.NumberOfCardContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#phases.
    def visitPhases(self, ctx: TablParser.PhasesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#phaseDef.
    def visitPhaseDef(self, ctx: TablParser.PhaseDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#phase.
    def visitPhase(self, ctx: TablParser.PhaseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#phaseName.
    def visitPhaseName(self, ctx: TablParser.PhaseNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#actionDef.
    def visitActionDef(self, ctx: TablParser.ActionDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#action.
    def visitAction(self, ctx: TablParser.ActionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#doTimes.
    def visitDoTimes(self, ctx: TablParser.DoTimesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#actionName.
    def visitActionName(self, ctx: TablParser.ActionNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#actionCardResource.
    def visitActionCardResource(self, ctx: TablParser.ActionCardResourceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#starting.
    def visitStarting(self, ctx: TablParser.StartingContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#deckOfDef.
    def visitDeckOfDef(self, ctx: TablParser.DeckOfDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#personalDeckDef.
    def visitPersonalDeckDef(self, ctx: TablParser.PersonalDeckDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#listOfCards.
    def visitListOfCards(self, ctx: TablParser.ListOfCardsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#cardDefinitions.
    def visitCardDefinitions(self, ctx: TablParser.CardDefinitionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#cardDefinition.
    def visitCardDefinition(self, ctx: TablParser.CardDefinitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#cardNameAndPicture.
    def visitCardNameAndPicture(self, ctx: TablParser.CardNameAndPictureContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#cardEffects.
    def visitCardEffects(self, ctx: TablParser.CardEffectsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#resourceEffectOrActionEffect.
    def visitResourceEffectOrActionEffect(self, ctx: TablParser.ResourceEffectOrActionEffectContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#resourceEffectWithTarget.
    def visitResourceEffectWithTarget(self, ctx: TablParser.ResourceEffectWithTargetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#actionWithTarget.
    def visitActionWithTarget(self, ctx: TablParser.ActionWithTargetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#target.
    def visitTarget(self, ctx: TablParser.TargetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#resourceEffect.
    def visitResourceEffect(self, ctx: TablParser.ResourceEffectContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#delim.
    def visitDelim(self, ctx: TablParser.DelimContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#modifyType.
    def visitModifyType(self, ctx: TablParser.ModifyTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#modifyNumber.
    def visitModifyNumber(self, ctx: TablParser.ModifyNumberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#cardName.
    def visitCardName(self, ctx: TablParser.CardNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#pictureName.
    def visitPictureName(self, ctx: TablParser.PictureNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#gameEnd.
    def visitGameEnd(self, ctx: TablParser.GameEndContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#endOrAndOr.
    def visitEndOrAndOr(self, ctx: TablParser.EndOrAndOrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#gameEndConditionDef.
    def visitGameEndConditionDef(self, ctx: TablParser.GameEndConditionDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#gameEndCondition.
    def visitGameEndCondition(self, ctx: TablParser.GameEndConditionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#gameEndConditionQuant.
    def visitGameEndConditionQuant(self, ctx: TablParser.GameEndConditionQuantContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#gameEndMoreOrLess.
    def visitGameEndMoreOrLess(self, ctx: TablParser.GameEndMoreOrLessContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#moreOrLess.
    def visitMoreOrLess(self, ctx: TablParser.MoreOrLessContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TablParser#gameEndResource.
    def visitGameEndResource(self, ctx: TablParser.GameEndResourceContext):
        return self.visitChildren(ctx)


del TablParser
