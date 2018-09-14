from setuptools import setup, find_packages


setup(
    name='p4dcli',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'p4d',
    ],
    dependency_links=[
        'https://github.com/ibrewster/p4d.git@v1.5#egg=p4d-1.5',
    ],
    entry_points='''
        [console_scripts]
        p4dcli=p4dcli:main
    ''',
)
