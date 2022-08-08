from setuptools import setup

setup(
    name='myPipeline',
    version='0.0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3"',
    ],
    description='functions that help user to build machine learning pipeline',
    author='Vincent',
    author_email='xuyanchong1999@outlook.com',
    license='MIT',
    packages=['myPipeline']
)
