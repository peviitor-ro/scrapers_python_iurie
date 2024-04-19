from setuptools import setup, find_packages

setup(
    name='scraper_',
    version='0.0.1',
    description='A simple scraper',
    url="",
    author='Iurie Chigai',

    packages=find_packages(),

    install_requires=[
        'peviitor_pyscraper',
        'python-dotenv',
        'requests',
        'beautifulsoup4',
        'lxml',
        
    ],
    python_requires='>=3.10',
)