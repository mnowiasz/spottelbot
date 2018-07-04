# Installing spottelbot
You need to have python, version 3.5+ installed (tested with python 3.6.*, the current version)

But before installing/starting it, you have to manually do two steps which can't be done
by the software:

## 1. Register a telegram bot
This is rather easy - you need to contact @botfather and request a bot. The steps necessary
are described [here](https://core.telegram.org/bots#6-botfather). You'll received a auth
token which you you need later, so don't forget saving it - otherwise you need to create
a new token.

## 2. Register your app at "My Applications"
Basically you create your own app at spotify. You have to register it at 
[My Applications](https://developer.spotify.com/my-applications/#!/applications). In the
process you'll be asked for an URL where your app will receive a token (we'll come to that later).
Since this is meant for web apps and the bot is not a webserver, just supply something like "http://localhost/myapp",
where myapp ist the name of your app. You'll be given a client_id and a client_secret.
Again, write this down, because you'll need it

## 3. Install spottelbot
Clone the repository using git or download it (either the master branch or one of the 
releases) and unpack it in your home directory. run "pip install --user ." in the unpacked 
directory (where setup.py resides). After this, you should have in $HOME/.local/bin/ an
executable named spottelbot. Do not start it yet, because you have to configure it first :-)

## 4. Configure spottelbot
Create a configfile, use example.config as a template. The bot will look at several locations,
starting at the local directory and then your homedirectory:

* spottelbot.config"
* spottelbot/config
* .spottelbot/config

So for example, create $HOME/spottelbot/config.

You have to fill out the options described in example.config (remove the #)
* The token you obtained from botfather in the first step
* Your spotify username/E-Mail
* The client_id from step 2
* The client_secret (step 2)
* The redirect_uri (see step 2, something like http://localhost/..)
* Oh, and your Telegram username, since most of the functions will be restricted. If you
are unsure about that, no problem: There's a command called /whoami which is available to
all users for this very purpose

When the config is ready, start the bot ($HOME/.local/bin/spottelbot). The first time you run
it (or if the bot needs more permissions in future versions) the following will happen:

>            User authentication requires interaction with your
>            web browser. Once you enter your credentials and
>            give authorization, you will be redirected to
>            a url.  Paste that url you were directed to to
>            complete the authorization.
> Opened  https://accounts.spotify.com/authorize?client_id.....

And your browser should open automatically the URL shown in "Opened" (if not, copy & paste 
it into your browser). Login with your user account into spotify. Then you'll probably get
and error, because you'll be redirected to http://localhost.../ which is perfectly fine:

> Enter the URL you were redirected to:

Copy the complete URL from your browser (http://localhost/...........) into this. After
that you're finished, because the auth token created by this procedure will be cached
and automatically renewed. *Note*: If you move the bot - i.e. let it run on another server - 
you'll be asked again. BTW, running the bot twice will result in a couple of exceptions. 
You only can run it once at a time, so if you want to run it somewhere else, make sure that
the currently running instance is shut down (/bye, or ctrl+c).








