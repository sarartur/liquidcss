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
        pass

    def parse(self, string: str) -> (list, 'sheet'):
        css_rules = []
        sheet = cssutils.parseString(string)
        for rule in sheet:
            if isinstance(rule, CSSMediaRule):
                rules = rule.cssRules
                css_rules = [*css_rules, *rules]
            if isinstance(rule, CSSStyleRule):
                css_rules.append(rule)
        return css_rules, sheet


class HtmlParser(Parser):

    def __init__(self):
        pass

    def parse(self, string: str) -> BeautifulSoup:
        soup = BeautifulSoup(string, 'html.parser')
        tags = soup.find_all()
        return tags, soup


class JsParser(Parser):

    def __init__(self):
        pass

    def parse(self, string):
        script = parseScript(string)
        identifiers = []
        string_body = """"""
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
                identifiers.append(identifier)
                string_body += f"{variable_declaration.kind} {declaration.id.name} = " + "\"{}\"\n"
        return identifiers, string_body




