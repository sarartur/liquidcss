import uuid
import re

from liquidcss.store import Storage
from liquidcss.re_utils import Replacement


class SelectorManager(object):

    def __init__(self):
        self.store = Storage()


    def _generate_uuid(self):
        id_ = str(uuid.uuid4())
        if not id_[0].isdigit():
            return id_
        else:
            return self._generate_uuid()


    def _generate_id(self, selector_string):
        existing = self.store.matches_existing(string = selector_string)
        if not existing:
            selector_text = self._generate_uuid()
        else:
            selector_text = existing
        return selector_text


    def toggle_selector_names(self, selectors):
        for selector in selectors:
            repl = Replacement(replacement = r'\1{}', manager = self)
            new_string = re.sub(
                r"([.#])-?[_a-zA-Z]+[_a-zA-Z0-9-]*", 
                repl,
                selector.selectorText
            )
            selector.selectorText = new_string
            for matched, replaced in repl.occurrences:
                self.store.map_[matched] = replaced[1:]
            

        
        

