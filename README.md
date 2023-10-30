# StartupLang
```bash
program = { statement } ;

statement = variable_declaration 
          | function_declaration 
          | expression_statement 
          | business_model_declaration 
          | investment_round_declaration 
          | recruitment_declaration ;

variable_declaration = "let", identifier, "=", expression ;

function_declaration = "function", identifier, "(", [ parameters ], ")", "{", { statement }, "}" ;

parameters = identifier, { ",", identifier } ;

expression_statement = expression, ";" ;

expression = term, { ("+" | "-"), term } ;

term = factor, { ("*" | "/"), factor } ;

factor = number | identifier | "(", expression, ")" ;

business_model_declaration = "businessModel", identifier, "{", { revenue_or_expense_declaration }, "}" ;

revenue_or_expense_declaration = ("revenue" | "expense"), identifier, "=", expression ;

investment_round_declaration = "investmentRound", identifier, "{", "valuation", "=", expression, "investments", "=", "[", { investment_declaration }, "]", "}" ;

investment_declaration = "{", "investor", "=", string, "amount", "=", expression, "}" ;

recruitment_declaration = "recruitment", identifier, "{", { job_declaration }, "}" ;

job_declaration = "job", string, "{", "description", "=", string, "candidates", "=", "[", { candidate_declaration }, "]", "}" ;

candidate_declaration = "{", "name", "=", string, "skills", "=", "[", { string }, "]", "}" ;

identifier = letter, { letter | digit } ;

number = digit, { digit } ;

string = """" , { character }, """" ;

letter = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;

digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

character = letter | digit | other_characters ;

other_characters = " " | "!" | "#" | "$" | "%" | "&" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "]" | "^" | "_" | "`" | "{" | "}" | "|" | "~" | """ ;
```
