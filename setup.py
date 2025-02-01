from setuptools import setup, find_packages

setup(
    name="chargehub_berlin",
    version="0.1",
    packages=find_packages(where="bounded_contexts"),
    package_dir={"": "bounded_contexts"},
    install_requires=[
        'dash', 'firebase-admin', 'flask', 'numpy', 'openpyxl', 'pandas', 'plotly', 'pytest', 'geopandas', 'coverage'
    ],
)
