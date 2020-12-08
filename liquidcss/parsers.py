import cssutils
from cssutils.css import (
    CSSRule, 
    CSSStyleRule,
    CSSMediaRule,
)


class Css_Parser(object):

    def __init__(self):
        pass


    def parse_css(self, css_string):
        css_rules = []
        sheet = cssutils.parseString(css_string)
        for rule in sheet:
            if isinstance(rule, CSSMediaRule):
                rules = rule.cssRules
                css_rules = [*css_rules, *rules]
            if isinstance(rule, CSSStyleRule):
                css_rules.append(rule)
        return css_rules, sheet


    def from_file(self, path):
        css_string = ''
        with open(path, 'r') as file:
            css_string = file.read()
        return self.parse_css(css_string = css_string)


    @staticmethod
    def to_file(sheet, path):
        with open(path, 'w') as file:
            file.write(sheet.cssText.decode('ascii'))
