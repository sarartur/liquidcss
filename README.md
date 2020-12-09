# LiquidCSS
Python package for altering CSS selector names across multiple files.
### Description & Implementation
The package offers up a way to counteract targeted scraping by changing all CSS selector names across multiple files to unique identifiers. \
\
Install the package with: ```pip install liquidcss``` \
https://pypi.org/project/liquidcss/
### Usage
Create a python file of any name and place it in your working directory. For the sake of this example we will call the file ```liquify.py```. The ```liquidcss``` package offers one main function ```rename_selectors```. The function takes in a list of paths to the CSS files, a list of paths to the HTML files and a list of paths to JavaScript files. \

The JavaScript file must containe exclusively ```var``` and ```const``` declarations and the selector prefix (either ```.``` or ```#```). Please refer to the **example** folder for demonstration. The idea is to export all selector names to their own files and assign them to variables.
 
Contents of ```liquify.py``` file.
``` python
import liquidcss

liquidcss.rename_selectors(
    css_files = ['example/original/css/sample001.css', ],
    html_files = ['example/original/html/sample001.html', ],
    js_files = ['example/original/js/sample001.js', ],
)
```
 
Execute the file with ```python liquify.py```
 
The function will create a directory structure with the base folder ```liquidcss_``` inside the directory where the ```liquify.py``` file is located. Inside the directory structure the function will place copies of the specified CSS JavaScript and HTML files with substituted selector names. The ```mapping.json``` file will include all substitution relationships.

**Important**: The resulting folder structure maybe different from the original one, so HTML files' references to JavaScript and CSS files may be broken in the process.
