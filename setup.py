from setuptools import setup, find_packages


deps = [
    'Flask',
    'Flask-PyMongo',
    'Click',
    'marshmallow'
]

test_packages = [
    'pytest',
    'pytest-cov',
    'pytest-env'
]
setup_packages = [
    'pytest-runner'
]

setup(
    name='songsapi',
    version='1.0',
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=deps,
    tests_require=test_packages,
    setup_requires=setup_packages,
    extras_require={
        'dev': [
            'flake8',
            'ipython',
            'ipdb'
        ] + test_packages
    }
)
