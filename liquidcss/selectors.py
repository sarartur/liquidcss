import uuid
import re

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

    def toggle_selector_names(self, selectors: list):
        for selector in selectors:
            repl = Replacement(replacement = r'\1{}', manager = self)
            new_string = re.sub(
                r"([.#])-?[_a-zA-Z]+[_a-zA-Z0-9-]*", 
                repl,
                selector.selectorText
            )
            selector.selectorText = new_string
            for matched, replaced in repl.occurrences:
                self.store[matched] = replaced
        
        
        

