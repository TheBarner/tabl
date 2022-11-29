grammar Tabl;

rules: title LB* contents LB* phases LB* setup LB* starting LB* gameEnd LB* winCon LB* listOfCards LB*;// setup, wincon

title: gameName playerCount;
gameName: ID (SPACE ID)*;
playerCount: PAR_OPEN numberOfPlayers PAR_CLOSE;
numberOfPlayers: NUMBER;

contents: CONTENTS COLON LB contentRule;
contentRule: resourceRuleDef (LB resourceRuleDef)* LB commonDeckDef;
resourceRuleDef: TAB resourceRule RESOURCETOKENS (SPACE PAR_OPEN resourceOptions PAR_CLOSE)? COMMA;
resourceRule: resourceNumber SPACE resourceName SPACE;
resourceOptions: RESOURCEOPTION (COMMA SPACE RESOURCEOPTION)*;
resourceName:  NAME;
resourceNumber: NUMBER | UNLIMITED;
commonDeckDef: TAB COMMONDECKOF COLON cardList PERIOD;
cardList: numberOfCardDef (COMMA numberOfCardDef)*;
numberOfCardDef: LB TAB TAB numberOfCard;
numberOfCard: NUMBER X SPACE NAME;

phases: INATURN COLON LB (prepPhase LB)? playPhase LB (cleanupPhase LB)? LB;
prepPhase: TAB PREPPHASE COLON LB phase;
playPhase: TAB PLAYPHASE COLON LB phase;
cleanupPhase: TAB CLEANUPPHASE COLON LB phase;
phase: actionDef (COMMA LB actionDef)* PERIOD;

actionDef: TAB TAB action;
action: actionName SPACE doTimes SPACE CARDS;
doTimes: (NUMBER | ANYALL);
actionName: ACTIONNAME;

starting: PLAYERSSTARTWIHT COLON LB resourceRuleDef (LB resourceRuleDef)* LB deckOfDef PERIOD;
deckOfDef: TAB DECKOF COLON personalDeckDef;
personalDeckDef: cardList;

listOfCards: LISTOFCARDS COLON LB cardDefinitions;
cardDefinitions: cardDefinition (LB* cardDefinition)*;
cardDefinition: TAB cardNamePictureCost (LB cardEffect)+;
cardNamePictureCost: cardName SPACE pictureName (SPACE resourceNumber SPACE resourceName)? COLON;
cardEffect: TAB TAB resourceEffectOrActionEffect;
resourceEffectOrActionEffect: (actionWithTarget | resourceEffectWithTarget) delim;
resourceEffectWithTarget: (target SPACE)? resourceEffect;
actionWithTarget: (target SPACE)? action;
target: TARGET;
resourceEffect: resourceName SPACE modifyType modifyNumber;
delim: COMMA | PERIOD;
modifyType: ARITH;
modifyNumber: NUMBER;
cardName: NAME;
pictureName: WAVY ID (SPACE ID)* WAVY;

gameEnd: GAMEENDSWHEN COLON LB (gameEndConditionDef endOrAndOr)+;
endOrAndOr: (SPACE (AND | OR) LB) | PERIOD;
gameEndConditionDef: TAB gameEndCondition;
gameEndCondition: APLAYERREACHES SPACE gameEndConditionQuant SPACE (gameEndMoreOrLess SPACE)? gameEndResource SPACE RESOURCETOKENS;
gameEndConditionQuant: NUMBER;
gameEndMoreOrLess: OR SPACE moreOrLess;
moreOrLess: MOREORLESS;
gameEndResource: NAME;

winCon: GAMEISWONBY COLON LB TAB PLAYERWITH SPACE moreOrLess SPACE resourceName SPACE RESOURCETOKENS PERIOD;


PREPPHASE: 'preparation phase';
PLAYPHASE: 'play phase';
CLEANUPPHASE: 'cleanup phase';
PLAYERWITH: 'the player with';
GAMEISWONBY: 'The game is won by';
CONTENTS: 'Contents' | 'contents';
TAB: '\t' | '    ';
COMMA: ',';
PAR_OPEN: '(';
PAR_CLOSE: ')';
COLON: ':';
WAVY: '~';
HASH: '#';
LB: '\r' | '\n' | '\r\n';
X: 'x';
ARITH: '*' | '+' | '-' | '/';
PERIOD: '.';
SPACE: ' ';
DELIM: ',' | '.';
APOSTROPHE: '\'';
TO: 'to';
GAMEENDSWHEN: 'The game ends when';
APLAYERREACHES: 'a player reaches' | 'they reach';
OR: 'or';
AND: 'and';
MOREORLESS: 'less' | 'more';
INATURN: 'In a turn' | 'in a turn';
RESOURCETOKENS: 'resource token' | 'resource tokens';
COMMONDECKOF: 'a common deck of';
UNLIMITED: 'unlimited';
DECKOF: 'a deck of';
PLAYERSSTARTWIHT: 'Players start with';
ACTIONNAME: 'Draw' | 'draw' | 'play' | 'Play' | 'discard' | 'Discard' | 'buy' | 'Buy' | 'scrap' | 'Scrap';
CARDS: 'cards' | 'card';
LISTOFCARDS: 'List of cards';
RESOURCEOPTION: 'visible' | 'per-turn' | 'strict';
TARGET: 'enemy';
ANYALL: 'any' | 'all';
NUMBER: [0-9]+;
NAME: '\''[a-zA-Z]([-a-zA-Z ])*'\'';
ID: [a-zA-Z]+;
