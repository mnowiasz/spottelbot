from setuptools import setup

setup(
    name='spottelbot',
    version='0.1.0',
    description='A telegram bot implementing missing spotify features',
    author="@mnowiasz",
    author_email="nowiasz@gmail.com",
    url='https://github.com/mnowiasz/spottelbot',
    install_requires=[
        'requests>=2.3.0',
        'six>=1.10.0',
        'python-telegram-bot>=10.1.0'
    ],
    entry_points={
        'console_scripts': ['spottelbot=spottelbot.botmain:botmain'],
    },
    license='LICENSE',
    packages=['spotipy.spotipy', 'spottelbot'])
