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

class Document(object):

    def __init__(self, to_string_method):
        self.to_string_method = to_string_method
        self.obj = None
        self.selector_objs = []

    def to_string(self):
        return self.to_string_method()

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


    def _to_string(self):
        """
        Method has to be overwritten from 
        child class
        """
        pass

class CssParser(Parser):

    def __init__(self):
        pass

    def parse(self, string: str) -> (list, 'sheet'):
        document = Document(to_string_method = self._to_string)
        document.obj = cssutils.parseString(string)
        for rule in document.obj:
            if isinstance(rule, CSSMediaRule):
                rules = rule.cssRules
                document.selector_objs = [*document.selector_objs, *rules]
            if isinstance(rule, CSSStyleRule):
                document.selector_objs.append(rule)
        return document


class HtmlParser(Parser):

    def __init__(self):
        pass

    def parse(self, string: str) -> BeautifulSoup:
        document = Document(to_string_method = self._to_string)
        document.obj = BeautifulSoup(string, 'html.parser')
        document.selector_objs = document.obj.find_all()
        return document


class JsParser(Parser):

    def __init__(self):
        pass

    def parse(self, string):
        document = Document(to_string_method = self._to_string)
        script = parseScript(string)
        for variable_declaration in script.body:
            if not isinstance(variable_declaration, VariableDeclaration):
                continue
            for declaration in variable_declaration.declarations:
                #print(declaration)
                if not isinstance(declaration, VariableDeclarator):
                    continue
                identifier = declaration.init
                if not isinstance(identifier, Literal):
                    continue
                document.selector_objs.append(identifier)
                document.obj += f"{variable_declaration.kind} {declaration.id.name} = " + "\"{}\"\n"
        return document
