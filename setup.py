from setuptools import setup, find_packages


setup(
    name='songsapi',
    version='1.0',
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-PyMongo',
        'Click',
        'marshmallow'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'ipython',
            'ipdb'
        ]
    }
)
