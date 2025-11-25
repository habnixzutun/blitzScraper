# The Setup

### Configuring the .env file
I'd recomment using this as your template to make sure you don't forget any env vars.
If you want to change the code a litte you can also combine some of them
```
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB=""
POSTGRES_PORT=5432
USR=""
PASSWD=""
SERVER=""
PORT="5432"
DB_NAME=""
```

### Start Docker
Just run `docker-compose up` and maybe check port 5432 for availability beforehand


# The Websocket
There are at least four websockets to choose from, all giving you the same data at the about same time

```
wss://ws1.blitzortung.org/
wss://ws2.blitzortung.org/
wss://ws7.blitzortung.org/
wss://ws8.blitzortung.org/
```

# Used Diskspace

From my experience those were the average usages of diskspace:

```
24.2 MB / hour
7188 Entries / hour
```