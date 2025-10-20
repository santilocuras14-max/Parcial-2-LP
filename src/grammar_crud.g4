\
grammar CRUD;

options { tokenVocab=Tokens; } 


stmtlist : stmt SEMICOL (stmt SEMICOL)* ;
stmt : selectStmt
     | insertStmt
     | updateStmt
     | deleteStmt
     ;

selectStmt : SELECT selectList FROM ID optWhere ;
selectList : STAR
           | fieldList
           ;
fieldList : ID (COMMA ID)* ;
insertStmt : INSERT INTO ID LPAREN fieldList RPAREN VALUES LPAREN valueList RPAREN ;
valueList : literal (COMMA literal)* ;
updateStmt : UPDATE ID SET assignList optWhere ;
assignList : ID EQ literal (COMMA ID EQ literal)* ;
deleteStmt : DELETE FROM ID optWhere ;
optWhere : WHERE condition
         | // epsilon
         ;
condition : ID EQ (literal | ID) ;


SELECT : 'SELECT' ;
INSERT : 'INSERT' ;
INTO   : 'INTO' ;
UPDATE : 'UPDATE' ;
DELETE : 'DELETE' ;
FROM   : 'FROM' ;
WHERE  : 'WHERE' ;
SET    : 'SET' ;
VALUES : 'VALUES' ;

STAR   : '*' ;
COMMA  : ',' ;
SEMICOL: ';' ;
LPAREN : '(' ;
RPAREN : ')' ;
EQ     : '=' ;

ID     : [A-Za-z_][A-Za-z0-9_]* ;
literal: '\'' (~'\\'')* '\'' | '\"' (~'\"')* '\"' | DIGITS ;
fragment DIGITS: [0-9]+ ('.' [0-9]+)? ;

WS : [ \\t\\r\\n]+ -> skip ;
