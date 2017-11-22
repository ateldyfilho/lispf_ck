import ox
import click
import pprint

lexer = ox.make_lexer([
	('NAME', r'[-a-zA-Z]+'),
	('NUMBER', r'\d+(\.\d*)?'),
	('PARENTHESES_OPEN', r'\('),
	('PARENTHESES_CLOSE', r'\)'),
	('COMMENT', r';(.)*'),
	('NEWLINE', r'\n+'),
])

tokens = ['NAME', 'NUMBER', 'PARENTHESES_OPEN', 'PARENTHESES_CLOSE']

parser = ox.make_parser([

	    ('term : PARENTHESES_OPEN term PARENTHESES_CLOSE', lambda parentheses_open, term, parentheses_close: term),
	('atom : PARENTHESES_OPEN PARENTHESES_CLOSE', lambda parentheses_open, parentheses_close: ()),
	('term : term term', lambda term, other_term: (term, other_term)),
	('term : term atom', lambda term, atom: (term, atom)),
	('term : atom term', lambda atom, term: (atom, term)),
	('term : atom', lambda term: term),
	('atom : NAME', lambda name: name),
	('atom : NUMBER', lambda x: float(x)),
	
], tokens)


@click.command()
@click.argument('source', type=click.File('r'))


def make_tree(source):

    lp_code = source.read()
    print( lp_code)
    tokens = lexer(lp_code)

    parser_tokens = lexer(lp_code)

    parser_tokens = [token for token in tokens if token.type !=
                     'COMMENT' and token.type != 'NEWLINE']

    tree = parser(parser_tokens)
    pprint.pprint(tree)

if __name__ == '__main__':
    make_tree()
