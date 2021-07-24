GUILDS=[674409360948068372] #TestingServer
GAME_STATS_FILE="data/gameStats.json"
COMMAND_STATS_FILE="data/commandStats.json"
ADMIN_FILE="data/admins.json"
WORDS_FILE="data/words.json"
SONG_FILE="data/songs.txt"
POKEMON_STATS_FILE="data/pokemonStats.json"
ANIME_STATS_FILE="data/animeStats.json"

DAILY_MESSAGE_HELP="""```
Waluigi Bot Daily Message (20:00 - 21:00 UTC)

This bot can send specific messages to this channel each day using this command.

A few things to note:
  The bot will no longer send messages to this channel message sending permissions are changed.
  The daily message is only unique to the day, not the the channel.
  The daily messages can be cancelled by using the same command that enabled the messages to be sent.
    For example:
      Using 'wah daily song' a second time.

These are the current daily message arguments that Waluigi Bot recognizes:
  - 'song' : A Spotify link on a song from one of our playlists
  - 'stat' : Information on it's on stats (most used commands, number of servers, etc.).
  - 'hmmm' : A random image from r/hmmm on Reddit (Warning: occasionally NSFW)
  - 'pokemon' : An embed from a random Pokemon
  - 'botw' : An embed from a random Legend of Zelda: Breath of the Wild Entity
  - 'info' : This argument displays the current daily messages this specific channel is signed up for.

Use 'wah daily [argument listed above]' to start getting daily messages.
The slash command version can also be used.

Ideas on how to improve this feature are greatly appreciated. 
```"""