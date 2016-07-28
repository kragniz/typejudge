import setuptools

setuptools.setup(
    name="typejudge",
    version="0.1.1",
    url="https://github.com/kragniz/typejudge",

    author="Louis Taylor",
    author_email="louis@kragniz.eu",

    description="Automatically check for semver compliance based on type hints",
    long_description=open('README.rst').read(),

    py_modules=['typejudge'],
    entry_points={'console_scripts':
        ['typejudge = typejudge:main',]
    ,},

    install_requires=[
        "semver",
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
