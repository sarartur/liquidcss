# LiquidCSS
Python package for alterning css selector names and html templates across multiple files.
## Description & Implementation
Alters css selector names across css files and html templates.
## Usage
The package is currently under constructiom and has limited features.

Contents of ```liquify.py``` file.
``` python
import liquidcss

liquidcss.rename_selectors(
    css_files = [
        'css/sample001.css',
        'css/sample002.css'
    ],
    html_files = None
)
```

Execute the file with ```python liquify.py```