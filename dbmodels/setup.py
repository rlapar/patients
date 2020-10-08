from setuptools import find_packages, setup

with open('requirements/requirements.in') as f:
    REQUIREMENTS = [
        item
        for item in f.read().splitlines()
        if item.strip() and not item.startswith('--extra')
    ]

with open('VERSION') as f:
    VERSION = f.readline().strip()

setup(
    name='patients.dbmodels',
    version=VERSION,
    # url='http://127.0.0.1:8000',
    # download_url='http://127.0.0.1:8000',
    author='radovanlapar',
    author_email='laparradovan@gmail.com',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS,
    include_package_data=True,
    classifiers=[
        'Private :: Do Not Upload',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
