%{
#include "y.tab.h"
%}


TITULO              "#"
IDENTIFICADOR       [a-zA-Z_][a-zA-Z_0-9]*
VALOR               [0-9]+
TEXTO               [a-zA-Z_0-9 -]+

// Palavras-chave
"DEFINIR_STARTUP"   { return DEFINIR_STARTUP; }
"INVESTIMENTO"      { return INVESTIMENTO; }
"MODELO_NEGOCIOS"   { return MODELO_NEGOCIOS; }
"RODADA_INVESTIMENTO" { return RODADA_INVESTIMENTO; }
"RECRUTAMENTO"      { return RECRUTAMENTO; }

// Outros tokens
[ \t\n]             { /* Ignorar espaços em branco e novas linhas */ }
.                   { return yytext[0]; }

%%

int yywrap() { return 1; }
