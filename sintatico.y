%{
#include <stdio.h>
%}

%token IDENTIFICADOR VALOR TEXTO
%token DEFINIR_STARTUP INVESTIMENTO MODELO_NEGOCIOS RODADA_INVESTIMENTO RECRUTAMENTO

%%

startup:
    '{' instrucoes '}'
    ;

instrucoes:
    | instrucoes instrucao
    ;

instrucao:
    TITULO
  | DEFINIR_STARTUP
  | INVESTIMENTO
  | MODELO_NEGOCIOS
  | RODADA_INVESTIMENTO
  | RECRUTAMENTO
  ;

%%

int main() {
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
