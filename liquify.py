import liquidcss


liquidcss.rename_selectors(
    css_files = [
        'example/original/css/sample001.css',
        #'tests/samples/css/bootstrap.css'
    ],
    html_files = [
        'example/original/html/sample001.html',
        #'tests/samples/html/bootstrap_template001.html'
    ],
    js_files = [
        'example/original/js/sample001.js'
    ],
)