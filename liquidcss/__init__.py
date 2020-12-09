import os
import sys
import json


from liquidcss.parsers import CssParser, HtmlParser
from liquidcss.selectors import SelectorManager
from liquidcss.structure import StructureManager


selector_manager = SelectorManager()
structure_manager = StructureManager(
    base_dir = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))
)

css_parser = CssParser()
html_parser = HtmlParser()


def rename_selectors(css_files: list, html_files: list) -> None:
    """
    **Ranames all CSS Selector**

    This function replaces all css selectors with unique identifiers found in the specified files.
    The function will create a folder structure in the same directory it is ran from and
    will write copies of the specified css and html files with unique ids in selector names.

    :param css_files: the list of relative or absolute paths to the css files.
    :param html_files: the list of relative or absolute paths to the html files.
    """

    structure_manager.validate_structure()

    for path in css_files:
        rules, sheet = css_parser.from_file(path = path)

        selector_manager.toggle_selector_names(objects = rules)
        structure_manager.create_file( 
            type_ = 'css',
            file_name = os.path.basename(path),
            string = sheet.cssText.decode('utf-8'),
        )

    for path in html_files:
        tags, soup = html_parser.from_file(path = path)

        selector_manager.toggle_selector_names(objects = tags)
        structure_manager.create_file(
            type_ = 'html',
            file_name = os.path.basename(path),
            string = str(soup),
        )

    structure_manager.create_file(
        type_ = "mapping",
        file_name = "mapping.json",
        string = json.dumps(selector_manager.store)
    )
        