import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liquidcss", 
    version="0.3.1",
    author="Artur Saradzhyan",
    author_email="saradzhyanartur@gmail.com",
    description="Alters css selector names across css files and html templates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saradzhyanartur/liquidcss",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'liquid = liquidcss.__main__:main',                  
        ], 
        'liquidcss.registered_commands': [
            'grab = liquidcss.commands.grab:main',
            'init = liquidcss.commands.init:main',
            'deploy = liquidcss.commands.deploy:main',
            'stage = liquidcss.commands.stage:main',
            'drop = liquidcss.commands.drop:main',
            'status = liquidcss.commands.status:main'
        ]         
    },
    install_requires=['cssutils==1.0.2', 'bs4==0.0.1', "esprima==4.0.1"],
    setup_requires=['cssutils==1.0.2', 'bs4==0.0.1', "esprima==4.0.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)