import uuid
import re

from liquidcss.store import Storage


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
        return existing if existing else self._generate_uuid()


    def toggle_selector_names(self, selectors):
        for selector in selectors:
            selector.selectorText = re.sub(
                r"([.#])-?[_a-zA-Z]+[_a-zA-Z0-9-]*", 
                r'\1{}'.format(
                    self._generate_id(selector_string = selector.selectorText)
                ), 
                selector.selectorText
            )
        return selectors

        

