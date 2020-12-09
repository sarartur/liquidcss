import os
import sys
import json

from liquidcss.parsers import (
    CssParser, 
    HtmlParser,
    JsParser,
)
from liquidcss.selectors import SelectorManager
from liquidcss.structure import StructureManager


selector_manager = SelectorManager()
structure_manager = StructureManager(
    base_dir = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))
)

css_parser = CssParser()
html_parser = HtmlParser()
js_parser = JsParser()


def rename_selectors(css_files: list, html_files: list, js_files: list) -> None:
    """
    **Ranames all CSS Selector**

    This function replaces all css selectors with unique identifiers found in the specified files.
    The function will create a folder structure in the same directory it is ran from and
    will write copies of the specified css and html files with unique ids in selector names.

    :param css_files: the list of relative or absolute paths to the css files.
    :param html_files: the list of relative or absolute paths to the html files.
    :param js_files: the list of relative or absolute paths to the js files.
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

    for path in js_files:
        identifiers, script_string = js_parser.from_file(path = path)
        selector_manager.toggle_selector_names(objects = identifiers)

        structure_manager.create_file(
            type_ = 'js',
            file_name = os.path.basename(path),
            string = script_string.format(*[identifier.value for identifier in identifiers])
        )

    structure_manager.create_file(
        type_ = "mapping",
        file_name = "mapping.json",
        string = json.dumps(selector_manager.store)
    )
        


"""
MIT License

Copyright (c) 2020 saradzhyanartur

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""