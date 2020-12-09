import uuid
import re
from cssutils.css import CSSStyleRule
from bs4.element import Tag

from liquidcss.re_utils import Replacement


class SelectorManager(object):

    def __init__(self):
        self.store = dict()

    def _generate_uuid(self):
        id_ = str(uuid.uuid4())
        if not id_[0].isdigit():
            return id_
        else:
            return self._generate_uuid()

    def _generate_id(self, selector_string: str) -> str:
        existing = self.store.get(selector_string)
        if not existing:
            selector_text = self._generate_uuid()
        else:
            selector_text = existing[1:]
        return selector_text

    def toggle_selector_names(self, objects):
        if all(isinstance(object_, CSSStyleRule) for object_ in objects):
            self._toggle_in_css(rules = objects)
        if all(isinstance(object_, Tag) for object_ in objects):
            self._toggle_in_html(tags = objects)
        
    def _toggle_in_css(self, rules):
        for selector in rules:
            repl = Replacement(replacement = r'\1{}', manager = self)
            new_string = re.sub(
                r"([.#])-?[_a-zA-Z]+[_a-zA-Z0-9-]*", 
                repl,
                selector.selectorText
            )
            selector.selectorText = new_string
            for matched, replaced in repl.occurrences:
                self.store[matched] = replaced

    def _toggle_in_html(self, tags):
        for tag in tags:
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

