import cssutils
from cssutils.css import (
    CSSStyleRule,
    CSSMediaRule,
)
from bs4 import BeautifulSoup
from esprima import parseScript
from esprima.nodes import (
    VariableDeclaration,
    VariableDeclarator,
    Literal,
)

class Parser(object):

    def from_file(self, path: str):
        string = ''
        with open(path, 'r') as file:
            string = file.read()
        return self.parse(string = string)

    def parse(self, string):
        """
        Method has to be overwritten from 
        child class
        """
        pass

class CssParser(Parser):

    def __init__(self):
        self._doc_to_string_method = lambda document: document.obj.cssText.decode('utf-8')

    @classmethod
    def is_parser_for(cls, type_):
        return type_ == 'css'

    def parse(self, string: str) -> (list, 'sheet'):
        document = Document(to_string_method = self._doc_to_string_method)
        document.obj = cssutils.parseString(string)
        for rule in document.obj:
            if isinstance(rule, CSSMediaRule):
                rules = rule.cssRules
                document.selectors = [*document.selectors, *rules]
            if isinstance(rule, CSSStyleRule):
                document.selectors.append(rule)
        return document

class HtmlParser(Parser):

    def __init__(self):
        self._doc_to_string_method = lambda document: str(document.obj)

    @classmethod
    def is_parser_for(cls, type_):
        return type_ == 'html'

    def parse(self, string: str) -> BeautifulSoup:
        document = Document(to_string_method = self._doc_to_string_method)
        document.obj = BeautifulSoup(string, 'html.parser')
        document.selectors = document.obj.find_all()
        return document

class JsParser(Parser):

    def __init__(self):
        self._doc_to_string_method = lambda document, : document.obj.format(
            *[selector.value for selector in document.selectors]
        )

    @classmethod
    def is_parser_for(cls, type_):
        return type_ == 'js'

    def parse(self, string):
        document = Document(to_string_method = self._doc_to_string_method)
        document.obj = """"""
        script = parseScript(string)
        for variable_declaration in script.body:
            if not isinstance(variable_declaration, VariableDeclaration):
                continue
            for declaration in variable_declaration.declarations:
                if not isinstance(declaration, VariableDeclarator):
                    continue
                identifier = declaration.init
                if not isinstance(identifier, Literal):
                    continue
                document.selectors.append(identifier)
                document.obj += f"{variable_declaration.kind} {declaration.id.name} = " + "\"{}\"\n"
        return document

class Document(object):

    def __init__(self, to_string_method):
        self._to_string_method = to_string_method
        self.obj = None
        self.selectors = []

    def to_string(self):
        return self._to_string_method(self)

def create_parser(type_):
    for cls in Parser.__subclasses__():
        if cls.is_parser_for(type_):
            return cls()
