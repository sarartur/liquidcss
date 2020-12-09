import cssutils
from cssutils.css import (
    CSSRule, 
    CSSStyleRule,
    CSSMediaRule,
)
from bs4 import BeautifulSoup


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
