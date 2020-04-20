from string import digits
from string import ascii_lowercase


def tokenizer(string):
    current = 0
    tokens = []

    while current < len(string):
        char = string[current]

        if char == '(':
            tokens.append({
                'type': 'paren',
                'value': '('
            })
            current += 1
            continue

        if char == ')':
            tokens.append({
                'type': 'paren',
                'value': ')'
            })
            current += 1
            continue

        if char == ' ':
            current += 1
            continue

        numbers = [i for i in digits]
        if char in numbers:
            value = ''
            while char in numbers:
                value += char
                current += 1
                char = string[current]

            tokens.append({
                'type': 'number',
                'value': value
            })
            continue

        if char == '"':
            value = ''
            current += 1
            char = string[current]

            while char != '"':
                value += char
                current += 1
                char = string[current]

            tokens.append({
                'type': 'string',
                'value': value
            })
            continue

        letters = [i for i in ascii_lowercase]
        if char in letters:
            value = ''
            while char in letters:
                value += char
                current += 1
                char = string[current]

            tokens.append({
                'type': 'name',
                'value': value
            })
            continue

        raise TypeError(f'I dont know what this character is {char}')

    return tokens


def parser(tokens):
    global current
    current = 0

    def walk():
        global current
        token = tokens[current]

        if token['type'] == 'number':
            current += 1
            return {
                'type': 'NumberLiteral',
                'value': token['value']
            }

        if token['type'] == 'string':
            current += 1
            return {
                'type': 'StringLiteral',
                'value': token['value']
            }

        if token['type'] == 'paren' and token['value'] == '(':
            current += 1
            token = tokens[current]
            node = {
                'type': 'CallExpression',
                'name': token['value'],
                'params': []
            }

            current += 1
            token = tokens[current]
            while not token['type'] == 'paren' or (token['type'] == 'paren' and token['value'] != ')'):
                node['params'].append(walk())
                token = tokens[current]

            current += 1
            return node

        raise TypeError(token['type'])

    ast = {
        'type': 'Program',
        'body': []
    }

    while current < len(tokens):
        ast['body'].append(walk())

    return ast


def traverser(ast, visitor):
    def traverse_array(array, parent):
        for child in array:
            traverse_node(child, parent)

    def traverse_node(node, parent):
        method = visitor.get(node['type'])
        if method:
            method(node, parent)

        if node['type'] == 'Program':
            traverse_array(node['body'], node)
        elif node['type'] == 'CallExpression':
            traverse_array(node['params'], node)
        elif node['type'] == 'NumberLiteral' or 'StringLiteral':
            pass
        else:
            raise TypeError(node['type'])

    traverse_node(ast, None)


def transformer(ast):
    new_ast = {
        'type': 'Program',
        'body': []
    }
    ast['_context'] = new_ast.get('body')

    def number_literal(node, parent):
        parent['_context'].append({
                'type': 'NumberLiteral',
                'value': node['value'],
            })

    def string_literal(node, parent):
        parent['_context'].append({
                'type': 'StringLiteral',
                'value': node['value'],
            })

    def call_expression(node, parent):
        expression = {
            'type': 'CallExpression',
            'callee': {
                'type': 'Identifier',
                'name': node['name']
            },
            'arguments': []
        }
        node['_context'] = expression['arguments']

        if parent['type'] != 'CallExpression':
            expression = {
                'type': 'ExpressionStatement',
                'expression': expression
            }

        parent['_context'].append(expression)


    traverser(ast, {
        'NumberLiteral': number_literal,
        'StringLiteral': string_literal,
        'CallExpression': call_expression,
    })

    return new_ast


def code_generator(node):
    if node['type'] == 'Program':
        return '\n'.join([code for code in map(code_generator, node['body'])])
    elif node['type'] == 'ExpressionStatement':
        return code_generator(node['expression']) + ';'
    elif node['type'] == 'CallExpression':
        callee = code_generator(node['callee'])
        params = ', '.join([code for code in map(code_generator, node['arguments'])])
        return f'{callee}({params})'
    elif node['type'] == 'Identifier':
        return node['name']
    elif node['type'] == 'NumberLiteral':
        return node['value']
    elif node['type'] == 'StringLiteral':
        return '"' + node['value'] + '"'
    else:
        raise TypeError(node['type'])


def compiler(string):
    tokens = tokenizer(string)
    ast = parser(tokens)
    new_ast = transformer(ast)
    output = code_generator(new_ast)
    return output


if __name__ == '__main__':
    output = compiler('(add 2 (subtract 4 2))')
    print(output)
