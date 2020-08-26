# discord_remote_for_spotify
I wrote this a while back when spotify didn't offer the party/group-feature but I think just released the ```/v1/me/player/queue``` endpoint. (Player-Docs: https://developer.spotify.com/documentation/web-api/reference/player/) <br>
*So this is a fairly old project!*

## The idea behind it
Both scripts would run on the same computer and someone logs into his/her spotify-account (http://127.0.0.1/auth) on the server (where all credentials would be stored localy only). This person would also control via spotify-connect on which device the music would be played. <br> 

Meanwhile the discord-bot would be on a dedicate discord-server to which people could be invited by simply printing out a qr-code. To add something to the queue they would share a song from the spotify app to the discord app and on the corresponding server.

## Conclusion
This system works and is in fact quite stable. The way I did it was to set up everything (including the spotify player) on a laptop. A bonus is that you are able to see which song has been added by whom.
