grammar Tabl;

rules: title LB* contents LB* phases LB* starting LB* gameEnd LB*  listOfCards LB*;// setup, gameEnd, wincon

title: gameName playerCount;
gameName: ID (SPACE ID)*;
playerCount: PAR_OPEN numberOfPlayers PAR_CLOSE;
numberOfPlayers: NUMBER (SPACE TO  SPACE NUMBER)?;

contents: CONTENTS COLON LB contentRule;
contentRule: resourceRuleDef (LB resourceRuleDef)* LB commonDeckDef;
resourceRuleDef: TAB resourceRule RESOURCETOKENS COMMA;
resourceRule: resourceNumber SPACE resourceName SPACE;
resourceName:  NAME;
resourceNumber: NUMBER | UNLIMITED;
commonDeckDef: TAB COMMONDECKOF COLON cardList PERIOD;
cardList: numberOfCardDef (COMMA numberOfCardDef)*;
numberOfCardDef: LB TAB TAB numberOfCard;
numberOfCard: NUMBER X SPACE NAME;

phases: INATURN COLON phaseDef (phaseDef)* LB;
phaseDef: LB phase;
phase: TAB phaseName SPACE PHASE COLON LB actionDef (COMMA LB actionDef)* PERIOD;
phaseName: NAME;
actionDef: TAB TAB action;
action: actionName SPACE doTimes SPACE actionCardResource;
doTimes: (NUMBER | ANYALL);
actionName: ACTIONNAME;
actionCardResource: RESOURCEORCARDS;

starting: PLAYERSSTARTWIHT COLON LB resourceRuleDef (LB resourceRuleDef)* LB deckOfDef PERIOD;
deckOfDef: TAB DECKOF COLON personalDeckDef;
personalDeckDef: cardList;

listOfCards: LISTOFCARDS COLON LB cardDefinitions;
cardDefinitions: cardDefinition (LB* cardDefinition)*;
cardDefinition: TAB cardNameAndPicture LB cardEffect (LB cardEffect)*;
cardNameAndPicture: cardName SPACE pictureName COLON;
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
PHASE: 'phase';
TO: 'to';
GAMEENDSWHEN: 'The game ends when';
APLAYERREACHES: 'a player reaches';
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
RESOURCEORCARDS: 'cards' | 'card';
LISTOFCARDS: 'List of cards';
TARGET: 'enemy';
ANYALL: 'any' | 'all';
NUMBER: [0-9]+;
NAME: '\''[a-zA-Z]([-a-zA-Z ])*'\'';
ID: [a-zA-Z]+;
