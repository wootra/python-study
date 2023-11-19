# initialize

```sh
pip shell
# setting environment variables
source ./env.sh
python3 ./init.py
```

# how to start

```sh
flask run --debug
```

# how to create a migration

```sh
flask db init
```

# how to migrate (upgrade)

```sh
flask db migrate -m "my migration1"
```
