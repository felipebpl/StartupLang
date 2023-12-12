from abc import abstractmethod
import sys
import time


class PrePro:
    @staticmethod
    def filter(code):
        return '\n'.join([line.split('//')[0] for line in code.split('\n')])

class SymbolTable:
    def __init__(self):
        self.symbol_table = {}

    def get(self, identifier):
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]
        else:
            raise Exception(f"Variable {identifier} not declared")

    def set(self, identifier, value):
        self.symbol_table[identifier] = value

    def create(self, identifier, value):
        if identifier in self.symbol_table:
            raise Exception(f"Variable {identifier} already declared")
        self.symbol_table[identifier] = value


class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        pass

class DefinirStartup(Node):
    def evaluate(self, symbol_table):
        nome = self.children[0]
        valor_inicial = self.children[1].evaluate(symbol_table)
        symbol_table.create(nome, {'valor': valor_inicial, 'investimentos': [], 'modelo': {}})

class Investimento(Node):
    def evaluate(self, symbol_table):
        startup_nome = self.children[0]
        meta_investimento = self.children[1]['meta']
        captado_investimento = self.children[1]['captado']  
        startup = symbol_table.get(startup_nome)
        print(f"Começando uma rodada de captação com a meta de levantar R$ {meta_investimento.value}\n")
        time.sleep(1)  
        while captado_investimento.value < meta_investimento.value:
            captado_investimento.value += 5000
            print(f"Captado até agora: R$ {captado_investimento.value}")

        if captado_investimento.value < meta_investimento.value:
            print(f"Captado total: R$ {captado_investimento.value}\n")
            print("Meta de captação não atingida!\n")
        else:
            print(f"Captado total: R$ {captado_investimento.value}\nMeta de captação atingida!\n")
        startup['investimentos'].append({'meta': meta_investimento, 'captado': captado_investimento})
        time.sleep(2)  # Sleep for 2 seconds to simulate processing
        print("Rodada finalizada!\n")
        time.sleep(1)


class ModeloNegocios(Node):
    def evaluate(self, symbol_table):
        nome = self.children[0]
        modelo = self.children[1]
        startup = symbol_table.get(nome)
        startup['modelo'] = modelo

class Block(Node):
    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, symbol_table):
        return self.value

class DictVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, symbol_table):
        return self.value

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self):

        tokens = {
            "@startup": "DEFINIR_STARTUP",
            "%investimento": "INVESTIMENTO",
            "@modelo": "MODELO_NEGOCIOS",
            "(": "ABRE_PARENTESES",
            ")": "FECHA_PARENTESES",
            "{": "ABRE_CHAVES",
            "}": "FECHA_CHAVES",
            ",": "VIRGULA",
            ";": "PONTO_E_VIRGULA",
            "valor:": "LITERAL_VALOR",
            "startup:": "LITERAL_STARTUP",
            "investimentos:": "LITERAL_INVESTIMENTOS",
            "receita:": "ITEM_MODELO",
            "despesa:": "ITEM_MODELO",
            "meta:": "LITERAL_META",
            "captado:": "LITERAL_CAPTADO"  # New syntax for meta and captado
        }

        while self.position < len(self.source):
            current_char = self.source[self.position]

            if current_char.isspace():
                self.position += 1
                continue

            word = ''
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] in ['@', '%', ':', '_', '-']):
                word += self.source[self.position]
                self.position += 1

            if word in tokens:
                self.next = Token(tokens[word], word)
                return

            if word:
                if word.isdigit():
                    self.next = Token("VALOR", int(word))  # Correctly recognize numbers
                else:
                    self.next = Token("IDENTIFICADOR", word)
                return

            if current_char in tokens:
                self.next = Token(tokens[current_char], current_char)
                self.position += 1
                return

            raise ValueError(f"Invalid character at position {self.position}: '{current_char}'")

        self.next = Token("EOF", "")


class Parser:

    @staticmethod
    def parse_program(tokenizer):
        nodes = []
        while tokenizer.next.type != "EOF":
            if tokenizer.next.type == "DEFINIR_STARTUP":
                nodes.append(Parser.parse_definir_startup(tokenizer))
            elif tokenizer.next.type == "INVESTIMENTO":
                nodes.append(Parser.parse_investimento(tokenizer))
            elif tokenizer.next.type == "MODELO_NEGOCIOS":
                nodes.append(Parser.parse_modelo_negocios(tokenizer))
            else:
                raise Exception(f"Unexpected command: {tokenizer.next.value}")
        
        return Block("Block", nodes)

    @staticmethod
    def parse_definir_startup(tokenizer):
        tokenizer.select_next()  # Skip DEFINIR_STARTUP token
        if tokenizer.next.type != "IDENTIFICADOR":
            raise Exception("Identifier expected for startup name")
        nome_startup = tokenizer.next.value
        tokenizer.select_next()  # Skip identifier

        if tokenizer.next.type != "ABRE_PARENTESES":
            raise Exception("Expected '(' after startup name")
        tokenizer.select_next()  # Skip '('

        if tokenizer.next.type != "LITERAL_VALOR":
            raise Exception("Expected 'valor:'")
        tokenizer.select_next()  # Skip 'valor:'

        if tokenizer.next.type != "VALOR":
            raise Exception("Expected a numeric value after 'valor:'")

        valor_inicial = IntVal(tokenizer.next.value)

        tokenizer.select_next() # Skip numeric value

        if tokenizer.next.type != "FECHA_PARENTESES":
            raise Exception("Expected ')' after initial value")
        tokenizer.select_next()  # Skip ')'

        return DefinirStartup(None, [nome_startup, valor_inicial])

    @staticmethod
    def parse_investimento(tokenizer):
        tokenizer.select_next()  # Skip INVESTIMENTO token
        if tokenizer.next.type != "IDENTIFICADOR":
            raise Exception("Identifier expected for startup name")
        nome_startup = tokenizer.next.value
        tokenizer.select_next()  # Skip identifier

        if tokenizer.next.type != "ABRE_PARENTESES":
            raise Exception("Expected '(' after startup name")
        tokenizer.select_next()  # Skip '('

        if tokenizer.next.type != "LITERAL_META":
            raise Exception("Expected 'meta:'")
        tokenizer.select_next()  # Skip 'meta:'
        
        if tokenizer.next.type != "VALOR":
            raise Exception("Expected a numeric value after 'meta:'")
        meta_investimento = IntVal(tokenizer.next.value)
        tokenizer.select_next()  # Skip numeric value
        
        if tokenizer.next.type != "VIRGULA":
            raise Exception("Expected ',' after meta value")
        tokenizer.select_next()  # Skip ','
        
        if tokenizer.next.type != "LITERAL_CAPTADO":
            raise Exception("Expected 'captado:'", 'got', tokenizer.next.type)
        tokenizer.select_next()  # Skip 'captado:'
        
        if tokenizer.next.type != "VALOR":
            raise Exception("Expected a numeric value after 'captado:'")
        captado_investimento = IntVal(tokenizer.next.value)
        tokenizer.select_next()  # Skip numeric value
        
        if tokenizer.next.type != "FECHA_PARENTESES":
            raise Exception("Expected ')' after investment values")
        tokenizer.select_next()  # Skip ')'
        
        return Investimento(None, [nome_startup, {'meta': meta_investimento, 'captado': captado_investimento}])


    @staticmethod
    def parse_modelo_negocios(tokenizer):
        tokenizer.select_next()  # Skip MODELO_NEGOCIOS token
        if tokenizer.next.type != "IDENTIFICADOR":
            raise Exception("Identifier expected for startup name")
        nome_startup = tokenizer.next.value
        tokenizer.select_next()  # Skip identifier

        if tokenizer.next.type != "ABRE_CHAVES":
            raise Exception("Expected '{' to start business model")
        tokenizer.select_next()  # Skip '{'

        modelo = {}

        while tokenizer.next.type != "FECHA_CHAVES":
            if tokenizer.next.type not in ["ITEM_MODELO"]:
                raise Exception("Expected 'receita:' or 'despesa:' in business model")
            tipo_item = tokenizer.next.value
            tokenizer.select_next()  # Skip 'receita:' or 'despesa:'

            if tokenizer.next.type != "VALOR":
                raise Exception("Expected a numeric value after 'receita:' or 'despesa:'")
            valor_item = IntVal(tokenizer.next.value)
            modelo[tipo_item] = valor_item
            tokenizer.select_next()  # Skip numeric value

        tokenizer.select_next()  # Skip '}'

        return ModeloNegocios(None, [nome_startup, modelo])

    @staticmethod
    def run(code):
        try:
            tokenizer = Tokenizer(code)
            tokenizer.select_next()
            result = Parser.parse_program(tokenizer)
            
            if tokenizer.next.type != "EOF":
                raise Exception("Syntax error")

            symbol_table = SymbolTable()
            result.evaluate(symbol_table)

            for identifier, data in symbol_table.symbol_table.items():
                print(f"Startup: {identifier}")
                print(f"  Modelo de Negócios: ")
                for item, valor in data['modelo'].items():
                    print(f"    {item}: {valor.value}")
                print(f"  Caixa Inicial: R${data['valor']}")  # Access the 'value' attribute of IntVal
                print(f"  Investimentos: \n")
                for invest in data['investimentos']:
                    print(f"    Meta: {invest['meta'].value}")
                    print(f"    Captado: {invest['captado'].value}\n")

                final_caixa = data['valor'] + sum(invest['captado'].value for invest in data['investimentos'])
                print(f"  Caixa Final: R${final_caixa}")
                print()

            print("Teste processado com sucesso!")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        with open(sys.argv[1], 'r') as f:
            content = f.read() + "\n"
        content_filtered = PrePro.filter(content)
        root = Parser.run(content_filtered)
    except Exception as e:
        print(f"Error: {e}")