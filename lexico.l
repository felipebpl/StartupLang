%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sintatico.tab.h"
%}

DIGITO [0-9]
LETRA [a-zA-Z]

%%

"#"                                    { printf("Token TITULO\n"); return TITULO; }
"@startup"                             { printf("Token DEFINIR_STARTUP\n"); return DEFINIR_STARTUP; }
"%investimento"                        { printf("Token INVESTIMENTO\n"); return INVESTIMENTO; }
"@modelo"                              { printf("Token MODELO_NEGOCIOS\n"); return MODELO_NEGOCIOS; }
"@rodada"                              { printf("Token RODADA_INVESTIMENTO\n"); return RODADA_INVESTIMENTO; }
"@vaga"                                { printf("Token RECRUTAMENTO\n"); return RECRUTAMENTO; }
"valor:"                               { printf("Token LITERAL_VALOR\n"); return LITERAL_VALOR; }
"startup:"                             { printf("Token LITERAL_STARTUP\n"); return LITERAL_STARTUP; }
"investimentos:"                       { printf("Token LITERAL_INVESTIMENTOS\n"); return LITERAL_INVESTIMENTOS; }
"cargo:"                               { printf("Token LITERAL_CARGO\n"); return LITERAL_CARGO; }                          
"receita:"                             { printf("Token ITEM_MODELO\n"); return ITEM_MODELO; }  
"despesa:"                             { printf("Token ITEM_MODELO\n"); return ITEM_MODELO; }      
[a-zA-Z][a-zA-Z0-9]*                   { printf("Token IDENTIFICADOR\n"); return IDENTIFICADOR; }
{DIGITO}+                              { printf("Token VALOR\n"); return VALOR; }
"("                                    { printf("Token ABRE_PARENTESES\n"); return ABRE_PARENTESES; }
")"                                    { printf("Token FECHA_PARENTESES\n"); return FECHA_PARENTESES; }
"{"                                    { printf("Token ABRE_CHAVES\n"); return ABRE_CHAVES; }
"}"                                    { printf("Token FECHA_CHAVES\n"); return FECHA_CHAVES; }
","                                    { printf("Token VIRGULA\n"); return VIRGULA; }
\"([^\\\"]|\\.)*\"                     { printf("Token TEXTO\n"); return TEXTO; }
[ \t\n]                                { /* Ignora espaços embranco */ }
.                                      { fprintf(stderr, "Caractere não reconhecido: %c\n", yytext[0]); }

%%
