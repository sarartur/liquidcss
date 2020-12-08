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

    def __init__(self, store):
        self.store = store

    def parse(self, string: str) -> BeautifulSoup:
        soup = BeautifulSoup(string, 'html.parser')
        for tag in soup.find_all():
            classes = tag.get('class')
            if classes:
                new_classes = []
                for class_ in classes:
                    replacment = self.store.get(f".{class_}")
                    if replacment:
                        replacment = replacment[1:]
                    else:
                        replacment = class_
                    new_classes.append(replacment)
                tag['class'] = new_classes

            id_ = tag.get('id')
            if id_:
                replacment = self.store.get(f"#{id_}")
                if replacment:
                    replacment = replacment[1:]
                else:
                    replacment = id_
                tag['id'] = replacment
                
        return soup
