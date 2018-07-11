from setuptools import setup

setup(
    name='spottelbot',
    version='0.2.2',
    description='A telegram bot implementing missing spotify features',
    author="@mnowiasz",
    author_email="mark+spottelbot@nowiasz.de",
    url='https://github.com/mnowiasz/spottelbot',
    install_requires=[
        'future>=0.16.0',
        'requests>=2.3.0',
        'six>=1.10.0',
        'python-dateutil>=2.7.3',
        'python-telegram-bot>=10.1.0'
    ],
    entry_points={
        'console_scripts': ['spottelbot=spottelbot.botmain:botmain'],
    },
    license='LICENSE',
    packages=['spotipy.spotipy', 'spottelbot'])
