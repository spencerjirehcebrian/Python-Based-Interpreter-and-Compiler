import sys


def tokenizer(file_name):
    dict_of_tokens = {
        "operator_arithmetic_addition": "+",
        "operator_arithmetic_substraction": "-",
        "operator_arithmetic_multiplication": "*",
        "operator_arithmetic_division": "/",
        "operator_output": "<<",
        "operator_less": "<",
        "operator_greater": ">",
        "operator_equal": "=",
        "delimiter_terminate": ";",
        "delimiter_left_bracket": "{",
        "delimiter_right_bracket": "}",
        "delimiter_left_paranthesis": "(",
        "delimiter_right_paranthesis": ")",
        "whitespace": " ",
        "quote": '"',
        "operator_variable_assignment": ":=",
        "operator_variable_declaration": ":",
    }

    dict_of_keywords = {
        "output": "output",
        "if": "if",
        "integer": "integer",
        "double": "double",
        "string": "string",
    }

    def is_empty(string):
        if not str.isspace(string) and not string == "":
            return False
        else:
            return True

    def evaluate_literal(string, index, stringify=False):
        if stringify:
            return {
                "token": string,
                "token_name": "string",
                "token_type": "string",
                "line": index + 1,
            }
        else:
            if string in dict_of_keywords.values():
                keyword_output.append(string)
                return {
                    "token": string,
                    "token_name": string,
                    "token_type": "keyword",
                    "line": index + 1,
                }
            else:
                return {
                    "token": string,
                    "token_name": None,
                    "token_type": "identifier",
                    "line": index + 1,
                }

    tokenized = []
    keyword_output = []

    variable_assignment = False
    output = False
    string = False
    identifier = False

    current_word = ""
    current_line = 0

    file = open(file_name, "r")
    file_string = file.read()
    file_array = file_string.split("\n")
    file = open("NOSPACES.txt", "w")

    for item in file_array:
        item = item.replace(" ", "")
        file.writelines(item)
    file.close()

    for index, line in enumerate(file_array):
        for character in line:
            if string:
                if character == dict_of_tokens["quote"]:
                    string = not string
                    if len(current_word) > 0:
                        tokenized.append(
                            evaluate_literal(current_word, index, stringify=True)
                        )
                    tokenized.append(
                        {
                            "token": dict_of_tokens["quote"],
                            "token_name": "quote",
                            "token_type": "quotes",
                            "line": index + 1,
                        }
                    )
                    current_word = ""
                else:
                    current_word += character
            else:
                if output and not character == dict_of_tokens["operator_less"]:
                    tokenized.append(
                        {
                            "token": dict_of_tokens["operator_less"],
                            "token_name": "operator_less",
                            "token_type": "bool_operator",
                            "line": index + 1,
                        }
                    )
                    current_word = ""
                    output = False
                if character == dict_of_tokens["quote"]:
                    string = not string
                    if len(current_word) > 0:
                        tokenized.append(evaluate_literal(current_word, index))
                    tokenized.append(
                        {
                            "token": dict_of_tokens["quote"],
                            "token_name": "quote",
                            "token_type": "quotes",
                            "line": index + 1,
                        }
                    )
                    current_word = ""
                elif character.isalnum() or character == ".":
                    if variable_assignment:
                        variable_assignment = False
                        tokenized.append(
                            {
                                "token": dict_of_tokens[
                                    "operator_variable_declaration"
                                ],
                                "token_name": "operator_variable_declaration",
                                "token_type": "operator",
                                "line": index + 1,
                            }
                        )
                    current_word += character
                    identifier = True
                elif character == dict_of_tokens["operator_variable_declaration"]:
                    if identifier:
                        if not is_empty(current_word):
                            tokenized.append(evaluate_literal(current_word, index))
                            current_word = ""
                            identifier = False
                    variable_assignment = True
                elif character == dict_of_tokens["operator_equal"]:
                    if variable_assignment:
                        tokenized.append(
                            {
                                "token": dict_of_tokens["operator_variable_assignment"],
                                "token_name": "operator_variable_assignment",
                                "token_type": "operator",
                                "line": index + 1,
                            }
                        )
                        variable_assignment = False
                    else:
                        tokenized.append(
                            {
                                "token": dict_of_tokens["operator_equal"],
                                "token_name": "operator_equal",
                                "token_type": "operator",
                                "line": index + 1,
                            }
                        )
                elif character == dict_of_tokens["operator_arithmetic_addition"]:
                    if not is_empty(current_word):
                        tokenized.append(evaluate_literal(current_word, index))
                        current_word = ""
                    tokenized.append(
                        {
                            "token": dict_of_tokens["operator_arithmetic_addition"],
                            "token_name": "operator_arithmetic_addition",
                            "token_type": "operator",
                            "line": index + 1,
                        }
                    )
                elif character == dict_of_tokens["operator_less"]:
                    if output:
                        current_word = ""
                        tokenized.append(
                            {
                                "token": dict_of_tokens["operator_output"],
                                "token_name": "operator_output",
                                "token_type": "operator",
                                "line": index + 1,
                            }
                        )
                        output = False
                    else:
                        if not is_empty(current_word):
                            tokenized.append(evaluate_literal(current_word, index))
                            current_word = ""
                            identifier = False
                        output = True
                elif character == dict_of_tokens["operator_greater"]:
                    if not is_empty(current_word):
                        tokenized.append(evaluate_literal(current_word, index))
                        current_word = ""
                        identifier = False
                        output = False
                    tokenized.append(
                        {
                            "token": dict_of_tokens["operator_greater"],
                            "token_name": "operator_greater",
                            "token_type": "bool_operator",
                            "line": index + 1,
                        }
                    )
                elif character == dict_of_tokens["delimiter_left_bracket"]:
                    if len(current_word) > 0:
                        tokenized.append(evaluate_literal(current_word, index))
                    tokenized.append(
                        {
                            "token": dict_of_tokens["delimiter_left_bracket"],
                            "token_name": "delimiter_left_bracket",
                            "token_type": "bracket",
                            "line": index + 1,
                        }
                    )
                    current_word = ""
                elif character == dict_of_tokens["delimiter_right_bracket"]:
                    if len(current_word) > 0:
                        tokenized.append(evaluate_literal(current_word, index))
                    tokenized.append(
                        {
                            "token": dict_of_tokens["delimiter_right_bracket"],
                            "token_name": "delimiter_right_bracket",
                            "token_type": "bracket",
                            "line": index + 1,
                        }
                    )
                    current_word = ""
                elif character == dict_of_tokens["delimiter_left_paranthesis"]:
                    if len(current_word) > 0:
                        tokenized.append(evaluate_literal(current_word, index))
                    tokenized.append(
                        {
                            "token": dict_of_tokens["delimiter_left_paranthesis"],
                            "token_name": "delimiter_left_paranthesis",
                            "token_type": "parenthesis",
                            "line": index + 1,
                        }
                    )
                    current_word = ""
                elif character == dict_of_tokens["delimiter_right_paranthesis"]:
                    if len(current_word) > 0:
                        tokenized.append(evaluate_literal(current_word, index))
                    tokenized.append(
                        {
                            "token": dict_of_tokens["delimiter_right_paranthesis"],
                            "token_name": "delimiter_right_paranthesis",
                            "token_type": "parenthesis",
                            "line": index + 1,
                        }
                    )
                    current_word = ""
                elif character == dict_of_tokens["delimiter_terminate"]:
                    if not string:
                        identifier = False
                        variable_assignment = False
                        output = False
                        if len(current_word) > 0:
                            tokenized.append(evaluate_literal(current_word, index))
                        current_word = ""
                        tokenized.append(
                            {
                                "token": dict_of_tokens["delimiter_terminate"],
                                "token_name": "delimiter_terminate",
                                "token_type": "terminator",
                                "line": index + 1,
                            }
                        )
                    else:
                        current_word += character
                elif character == dict_of_tokens["whitespace"]:
                    if string:
                        current_word += character
                    else:
                        if not str.isspace(current_word) and not current_word == "":
                            tokenized.append(evaluate_literal(current_word, index))
                            current_word = ""

            current_line = index
    
    if current_word != "":
        print("Error: Tokenization failed")
        tokenized.append(evaluate_literal(current_word, current_line))

    keyword_file = open("RES_SYM.TXT", "w+")
    keyword_file.write(str(keyword_output))

    return tokenized


def parser(list_of_tokens):
    reserved_keywords = ["output", "if", "integer", "double", "string"]

    class UnexpectedSyntaxException(Exception):
        def __init__(self, expected_token, token):
            self.expected_token = expected_token
            self.token = token
            super().__init__(
                "Line {}: Unexpected Syntax Exception - Expected {} but got {} instead".format(
                    token["line"], expected_token, token["token"]
                )
            )

    class InvalidDataTypeException(Exception):
        def __init__(self, token, current_token):
            self.token = token
            super().__init__(
                "Line {}: Invalid Data Type Exception - {} connot be given the following data type: {} ".format(
                    token["line"], token["token"], current_token["token"]
                )
            )

    class Parser:
        def __init__(self, tokens):
            self.tokens = tokens
            self.token_index = 0
            self.target_code = ""

        def peek(self):
            if self.token_index < len(self.tokens):
                return self.tokens[self.token_index]

        def consume(self):
            token_to_return = self.peek()
            if token_to_return != False:
                self.token_index += 1
                return token_to_return

        def parse_num(self):
            current_token = self.peek()
            try:
                if str.isnumeric(current_token["token"]):
                    self.consume()
                    return True
                elif float(current_token["token"]):
                    self.consume()
                    return True
                else:
                    return False
            except ValueError:
                return False

        def parse_id(self):
            current_token = self.peek()

            if str.isalnum(current_token["token"]):
                if str.isalpha(current_token["token"][0]):
                    if current_token["token"] not in reserved_keywords:
                        self.consume()
                        return True
                    else:
                        raise Exception(
                            'Line {}: Reserved Keyword "{}"'.format(
                                current_token["line"], current_token["token"]
                            )
                        )
                else:
                    return False

        def parse_string(self):
            current_token = self.peek()
            if current_token["token_type"] == "string":
                self.consume()
                return True
            else:
                raise Exception(
                    "Line {}: Invalid string".format(current_token["line"])
                )

        def parse_expr_tail(self):
            if self.match("+"):
                if self.parse_expr():
                    return True
                else:
                    raise Exception(
                        "Line {}: Missing operand for + operator".format(
                            self.tokens[self.token_index]["line"] 
                        )
                    )
            elif self.match("-"):
                if self.parse_expr():
                    return True
                else:
                    raise Exception(
                        "Line {}: Missing operand for - operator".format(
                            self.tokens[self.token_index]["line"] 
                        )
                    )
            elif self.match("*"):
                if self.parse_expr():
                    return True
                else:
                    raise Exception(
                        "Line {}: Missing operand for * operator".format(
                            self.tokens[self.token_index]["line"] 
                        )
                    )
            elif self.match("/"):
                if self.parse_expr():
                    return True
                else:
                    raise Exception(
                        "Line {}: Missing operand for / operator".format(
                            self.tokens[self.token_index]["line"] 
                        )
                    )
            elif self.tokens[self.token_index]["token_type"] == "bool_operator":
                raise Exception(
                    "Line {}: Variable assignments do not accept boolean operators".format(
                        self.tokens[self.token_index]["line"]
                    )
                )
            else:
                return False

        def parse_expr(self):
            if self.parse_id():
                if self.parse_expr_tail():
                    return True
                else:
                    return True
            elif self.parse_num():
                if self.parse_expr_tail():
                    return True
                return True
            elif self.match('"'):
                if self.parse_string():
                    if self.match('"'):
                        return True
                    else:
                        raise UnexpectedSyntaxException('"', self.peek())
                else:
                    current_token = self.peek()
                    raise Exception(
                        "Line {}: Invalid string".format(current_token["line"])
                    )

        def match(self, toMatch):
            current_token = self.peek()
            if current_token["token"] == toMatch:
                self.consume()
                return True
            else:
                return False

        def parse_data_type(self):
            current_token = self.peek()
            token = current_token["token"]

            if token == "integer" or token == "double" or token == "string":
                self.consume()
                return True
            else:
                return False

        def parse_bool_op(self):
            current_token = self.peek()

            if self.match("<") or self.match("=") or self.match(">"):
                return True
            else:
                raise UnexpectedSyntaxException("boolean operator", current_token)

        def parse_bool_expr(self):
            current_token = self.peek()

            if self.parse_id():
                if self.parse_bool_op():
                    if self.parse_id():
                        return True
                    elif self.parse_num():
                        return True
                    else:
                        raise Exception(
                            "Line {}: Invalid right hand operand for boolean expression".format(
                                current_token["line"]
                            )
                        )
                else:
                    return False
            elif self.parse_num():
                if self.parse_bool_op():
                    if self.parse_id():
                        return True
                    elif self.parse_num():
                        return True
                    else:
                        raise Exception(
                            "Line {}: Invalid right hand operand for boolean expression".format(
                                current_token["line"]
                            )
                        )
            else:
                return False

        def parse_statement(self):
            current_token = self.peek()
            if self.match("if"):
                if self.match("("):
                    if self.parse_bool_expr():
                        if self.match(")"):
                            if self.parse_statement():
                                return True
                            else:
                                raise Exception(
                                    "Line {}: Invalid statement".format(
                                        current_token["line"]
                                    )
                                )
                        else:
                            raise UnexpectedSyntaxException(")", self.peek())
                    else:
                        raise Exception(
                            "Line {}: Invalid boolean expression".format(
                                current_token["line"]
                            )
                        )
                else:
                    raise UnexpectedSyntaxException("(", self.peek())
            elif self.match("output"):
                if self.match("<<"):
                    if self.match('"'):
                        if self.parse_string():
                            if self.match('"'):
                                if self.match(";"):
                                    return True
                                else:
                                    raise UnexpectedSyntaxException(";", self.peek())
                            else:
                                raise UnexpectedSyntaxException('"', self.peek())
                        else:
                            return False
                    elif self.parse_id():
                        if self.match(";"):
                            return True
                        elif self.parse_expr_tail():
                            if self.match(";"):
                                return True
                        else:
                            raise Exception(
                                'Line {}: Invalid output operand. Valid operands are: <identifier>, "<string>", or <numeric>'.format(
                                    current_token["line"]
                                )
                            )
                    else:
                        raise Exception(
                            'Line {}: Invalid output operand. Valid operands are: <identifier>, "<string>", or <numeric>'.format(
                                current_token["line"]
                            )
                        )
                else:
                    raise UnexpectedSyntaxException("<<", self.peek())
            elif self.parse_id():
                if self.match(":"):
                    if self.parse_data_type():
                        if self.match(";"):
                            return True
                        else:
                            raise UnexpectedSyntaxException(";", current_token)
                    else:
                        raise InvalidDataTypeException(
                            current_token, self.tokens[self.token_index]
                        )
                elif self.match(":="):
                    if self.parse_expr():
                        if self.match(";"):
                            return True
                        else:
                            raise UnexpectedSyntaxException(
                                ";", self.tokens[self.token_index]
                            )
                    else:
                        raise Exception(
                            "Line {}: Invalid Expression".format(
                                self.tokens[self.token_index]["line"]
                            )
                        )
                else:
                    raise UnexpectedSyntaxException(":", current_token)
            else:
                raise UnexpectedSyntaxException("identifier", current_token)

        def parse_statements(self):
            if self.parse_statement():
                return True
            else:
                return True

        def parse(self):
            if self.parse_statements():
                if self.peek():
                    self.parse()

    parser = Parser(list_of_tokens)
    try:
        parser.parse()
        return True
    except Exception as e:
        print("ERROR(S) FOUND:\n-------------------\n")
        print("\t{}".format(e))
        return False


def generator(file_to_open):
    file = open(file_to_open, "r").read()

    def execute_code():
        generated = ""
        statements = file.split(";")
        current_statement = statements[0]
        ctr = 0
        while ctr < len(statements) - 1:
            if ":=" in current_statement:
                to_generate = current_statement.replace(":=", " ")
                generated_list = to_generate.split(" ")
                generated += "\n{} = {}".format(generated_list[0], generated_list[1])
                ctr += 1
                current_statement = statements[ctr]
            elif ":" in current_statement:
                ctr += 1
                current_statement = statements[ctr]
                pass

            elif "if" in current_statement:
                to_generate = current_statement.replace("if", "")
                to_generate = to_generate.replace("(", " ")
                to_generate = to_generate.replace(")", "+terminator")
                to_generate = to_generate.split("+terminator")

                to_generate2 = to_generate[1].replace("output", "")
                to_generate2 = to_generate2.replace("<<", "")
                generated += "\nif {}:\n\tprint({})".format(
                    to_generate[0], to_generate2
                )
                ctr += 1
                current_statement = statements[ctr]

            elif "output" in current_statement:
                to_generate = current_statement.replace("output", "")
                to_generate = to_generate.replace("<<", "")
                generated += "\nprint({})".format(to_generate)
                ctr += 1
                current_statement = statements[ctr]
            else:
                ctr += 1
                current_statement = statements[ctr]
                pass

        return generated

    generated_code = execute_code()
    exec(generated_code)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Correct Usage: python HLint.Python.py <file_name.HL>")
        sys.exit(1)

    try:
        list_of_tokens = tokenizer(sys.argv[1])
        print("Tokenizing complete...")
        no_errors_found = parser(list_of_tokens)
        print("Parsing complete...")
        if no_errors_found == True:
            print("Code generation complete...")
            print("NO ERROR(S) FOUND\n-------------------\n")
            generator("NOSPACES.txt")
    except Exception as e:
        print(e)
