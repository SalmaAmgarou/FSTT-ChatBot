from setuptools import setup, find_packages

setup(
    name='rag_project',
    version='0.1.0',  # Adjust the version if necessary
    packages=find_packages(),
    install_requires=[
        'langchain_community>=0.1.0',
        'torch>=1.10.0',
        'sentence-transformers>=2.0.0',
        'pymongo>=4.0.1',
        'langchain>=0.1.0'
    ],
)
