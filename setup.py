from setuptools import setup, find_packages

setup(
    name="housing_market",
    packages=find_packages(),
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'flex'
    ],
    install_requires=[
        'sqlalchemy',
        'sqlalchemy_utils',
        'flask',
        'flask_restful',
        'flask_cors',
        'flask_sqlalchemy',
        'flask_httpauth',
        'webargs<4.0.0',
        'shapely',
        'requests',
        'pyshp'
    ]
)
