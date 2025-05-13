from setuptools import setup, find_packages

setup(
    name='questpd',
    version='0.1.0',
    author='Diego Guiraldes',
    author_email='dguiraldes@gmail.com',
    description='A lightweight wrapper to interact with QuestDB using pandas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/your_username/questpd',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.2.3',
        'psycopg2-binary>=2.9.9',
        'questdb>=2.0.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
