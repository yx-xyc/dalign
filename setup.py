import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'dalign'
AUTHOR = 'You'
AUTHOR_EMAIL = 'xuyanchong1999@outlook.com'
URL = 'https://github.com/yx-xyc/myPipeline'

LICENSE = 'MIT License'
DESCRIPTION = 'A simple data cleaning pipeline'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'matplotlib',
      'seaborn',
      'sklearn',
      'nltk'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
    )