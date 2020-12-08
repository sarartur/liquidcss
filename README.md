# LiquidCSS
Python package for altering CSS selector names across multiple files.
### Description & Implementation
The package offers up a way to counteract targeted scraping by changing all CSS selector names across multiple files to unique identifiers. \
\
Install the package with: ```pip install liquidcss``` \
https://pypi.org/project/liquidcss/
### Usage
Create a python file of any name and place it in your working directory. For the sake of this example we will call the file ```liquify.py```. The ```liquidcss``` package offers one main function ```rename_selectors```. The function takes in a list of paths to the CSS files and a list of paths to the HTML files.
 
Contents of ```liquify.py``` file.
``` python
import liquidcss
 
liquidcss.rename_selectors(
    css_files = [
        'tests/samples/css/sample001.css',
        #'tests/samples/css/bootstrap.css'
    ],
    html_files = [
        'tests/samples/html/sample001.html',
        #'tests/samples/html/bootstrap_template001.html'
    ]
)
```
 
Execute the file with ```python liquify.py```
 
The function will create a directory structure with the base folder ```liquidcss_``` inside the directory where the ```liquify.py``` file is located. Inside the directory structure the function will place copies of the specified CSS and HTML files with substituted selector names. The ```mapping.json``` file will include all substitution relationships.

