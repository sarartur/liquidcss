from liquidcss.parsers import Css_Parser
from liquidcss.selectors import SelectorManager
from liquidcss.structure import StructureManager

import os
import sys
import inspect



parser = Css_Parser()
selector_manager = SelectorManager()
structure_manager = StructureManager(
    base_dir = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))
)


def rename_selectors(css_files, html_files):
    structure_manager.validate_structure()

    for path in css_files:
        rules, sheet = parser.from_file(path = path)


        selector_manager.toggle_selector_names(selectors = rules)
        structure_manager.create_file( 
            type_ = 'css',
            file_name = os.path.basename(path),
            string = sheet.cssText,
        )

    for path in html_files:
        pass
        