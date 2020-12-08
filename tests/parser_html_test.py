import sys
sys.path.append('../')

from liquidcss.selectors import SelectorManager
from liquidcss.parsers import HtmlParser


def test_parse_from_file(parser):
    soup = parser.from_file('samples/html/sample001.html')
    print(soup)



if __name__ == "__main__":
    selector_manager = SelectorManager()
    parser = HtmlParser(store = selector_manager.store)
    selector_manager.store.update({
        'apple': 'replacement_apple',
        'bannana': 'replacement_bannana'
    })
    
    test_parse_from_file(parser = parser)
