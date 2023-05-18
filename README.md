# SourceBans-Checker
A tool written in Python to quickly look up a steam account to see if they have SourceBans across a variety of different servers.
Must provide an Steam API key if you want to be able to input CustomURLs.

# Packages Used:
* Asyncio - To speed up HTTP requests
* aiohttp - To be used with Asyncio for efficient 'threading'
* re - To capture the ban reasons and other miscellaneous stuff
* requests - For quick requests to steam to resolve customURLs via the API
* time - For timing the requests

Requires at least Python v3.6 to run for f-strings.
