# StartupLang

## Funcionalidades

- `DEFINIR_STARTUP` --> Define uma startup e atribui um valor inicial a ela.

- `INVESTIMENTO` --> Representa um investimento feito em uma startup específica.

- `MODELO_NEGOCIOS` --> Define um modelo de negócios para uma startup, incluindo o tipo do modelo, receitas e despesas.

- `RODADA_INVESTIMENTO` --> Representa uma rodada de investimento, listando os investidores e o valor captado de acordo com a meta da startup.

```code
STARTUP           = { INSTRUCAO } ;
INSTRUCAO          = ( TITULO | DEFINIR_STARTUP | INVESTIMENTO | MODELO_NEGOCIOS | RODADA_INVESTIMENTO | RECRUTAMENTO ) ;
TITULO             = "#", TEXTO, "\n" ;
DEFINIR_STARTUP    = "@startup", IDENTIFICADOR, "(", "valor:", VALOR, ")", "\n" ;
INVESTIMENTO       = "%investimento", IDENTIFICADOR_STARTUP, "(", "meta:", VALOR, ",", "captado:", VALOR, ")", "\n" ;
MODELO_NEGOCIOS    = "@modelo", IDENTIFICADOR, "{", { ITEM_MODELO }, "}", "\n" ;
ITEM_MODELO        = ( "receita", ":", VALOR | "despesa", ":", VALOR ), "\n" ;
RODADA_INVESTIMENTO = "@rodada", IDENTIFICADOR, "{", "startup:", IDENTIFICADOR_STARTUP, "investimentos:", "[", { IDENTIFICADOR_INVESTIDOR }, "]", "}", "\n" ;
RECRUTAMENTO       = "@vaga", IDENTIFICADOR, "(", "cargo:", TEXTO, ")", "\n" ;
IDENTIFICADOR      = LETRA, { LETRA | DIGITO | "_" } ;
IDENTIFICADOR_STARTUP = IDENTIFICADOR ;
IDENTIFICADOR_INVESTIDOR = IDENTIFICADOR ;
VALOR              = NUMERO, { NUMERO } ;
LETRA              = ( "a" | ... | "z" | "A" | ... | "Z" ) ;
DIGITO             = ( "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ) ;
TEXTO              = { LETRA | DIGITO | " " | "-" | "_" } ;
```
