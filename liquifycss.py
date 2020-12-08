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