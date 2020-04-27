import the_super_tiny_compiler

input_string = "(add 2 (subtract 4 2))"
output_string = "add(2, subtract(4, 2));"

expected_tokens = [
    {
        "type": "paren",
        "value": "("
    },
    {
        "type": "name",
        "value": "add"
    },
    {
        "type": "number",
        "value": "2"
    },
    {
        "type": "paren",
        "value": "("
    },
    {
        "type": "name",
        "value": "subtract"
    },
    {
        "type": "number",
        "value": "4"
    },
    {
        "type": "number",
        "value": "2"
    },
    {
        "type": "paren",
        "value": ")"
    },
    {
        "type": "paren",
        "value": ")"
    }
]

expected_ast = {
    "type": "Program",
    "body": [
        {
            "type": "CallExpression",
            "name": "add",
            "params": [
                {
                    "type": "NumberLiteral",
                    "value": "2"
                },
                {
                    "type": "CallExpression",
                    "name": "subtract",
                    "params": [
                        {
                            "type": "NumberLiteral",
                            "value": "4"
                        },
                        {
                            "type": "NumberLiteral",
                            "value": "2"
                        }
                    ]
                }
            ]
        }
    ]
}

expected_new_ast = {
    "type": "Program",
    "body": [
        {
            "type": "ExpressionStatement",
            "expression": {
                "type": "CallExpression",
                "callee": {
                    "type": "Identifier",
                    "name": "add"
                },
                "arguments": [
                    {
                        "type": "NumberLiteral",
                        "value": "2"
                    },
                    {
                        "type": "CallExpression",
                        "callee": {
                            "type": "Identifier",
                            "name": "subtract"
                        },
                        "arguments": [
                            {
                                "type": "NumberLiteral",
                                "value": "4"
                            },
                            {
                                "type": "NumberLiteral",
                                "value": "2"
                            }
                        ]
                    }
                ]
            }
        }
    ]
}


def test_compiler():
    tokens = the_super_tiny_compiler.tokenizer(input_string)
    ast = the_super_tiny_compiler.parser(tokens)
    new_ast = the_super_tiny_compiler.transformer(ast)
    generated_code = the_super_tiny_compiler.code_generator(new_ast)
    output = the_super_tiny_compiler.compiler(input_string)

    assert tokens == expected_tokens
    assert ast == expected_ast
    assert new_ast == expected_new_ast
    assert generated_code == output_string
    assert output == output_string
