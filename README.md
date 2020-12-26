# LiquidCSS
Command line tool for hashing selectors across CSS, HTML and JavaScript files.
### Description & Implementation
The tool makes most scraping robots obsolete by dynamically hashing all selectors across the entire infrastructure of a web application. Most scraping tools 
achieve their objective by hooking onto certain HTML selector names in the response document. LiquidSel offers up a way to counter act this approach by changing the selector names without breaking any of the functionality or appearance of the web application. 


Install the package with: ```pip install liquidcss``` \
https://pypi.org/project/liquidcss/
### Usage
To begin using the tool first create a WorkSpace: ```liquid init``` \
Register files to the WorkSpace either individually or by specifying a ```txt``` document containing a list of paths: \
```liquid grab /path/to/file``` or ```liquid grab -r paths.txt```
Once files are registered, view their status inside the WorkSpace:```liquid status -a```
```
[ID: 0]
    name: sample001.css
    path: /example/original/sample001.css
    type: css
    hash: 603706f3aa0a9b7779fca2acd29d4b8e5a68796f846f955c6ac6e72b6f13081a
    staged: True
    deployed: False

```
Hash the selector names across all registered files: ```liquid stage -a```


**The selector names will be hashed only if they are present in the CSS files registered in the workspace.**
The files are now ready to be deployed. The deploy command will swap the files at the registered paths with the hashed files and create
a backup of the original files.:```liquid deploy -a```


Reverse the deployment of the files with hashed selectors and replace them with files stored in backup: ```liquid deploy -a -r```


**JavaScript files registered with the WorkSpace can only contain ```const``` or ```var``` key words and only the selector names as strings include the ```.``` or the ```#```.** See the examples in the example folder.

More extensive documentation and further features are in development.