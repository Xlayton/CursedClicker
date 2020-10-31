import psycopg2
import json
from psycopg2.errors import SerializationFailure

conn = psycopg2.connect(
    database='defaultdb',
    user='zslocum',
    password='password1234',
    sslmode='require',
    port=26257,
    host='cursed-clicker-5zg.gcp-us-west2.cockroachlabs.cloud'
)

def add_user(username, password) :
    run_sql(f'INSERT INTO users(username, password, curdmg, curbalance) VALUES (\'{username}\', \'{password}\', 100, 0)')
    data = json.loads(get_user(username))
    uid = data['id']
    run_sql(f'INSERT INTO userinventories(userid, icepack, watercooling, liquidnitrogen, damaginglaser, meltinglaser, pulverizinglaser, bomb, speedpotion, acidpot, companion) VALUES (\'{uid}\', false, false, false, false, false, false, 0, 0, 0, 0)')

def get_user(username) :
    result = run_sql_return(f'SELECT * FROM users WHERE username = \'{username}\'')
    return json.dumps({'id': result[0][0], 'username': result[0][1], 'password': result[0][2], 'curdmg': result[0][3], 'curbalance': result[0][4]})


def give_money(username, amount) :
    run_sql(f'UPDATE users SET curbalance = curbalance + {amount} WHERE username = \'{username}\'')

def get_userinventory(username) :
    data = json.loads(get_user(username))
    uid = data['id']
    result = run_sql_return(f'SELECT * FROM userinventories WHERE userid = \'{uid}\'')
    return json.dumps({'id': result[0][0], 'icepack': result[0][1], 'watercooling': result[0][2], 'liquidnitrogen' : result[0][3], 'damaginglaser': result[0][4], 'meltinglaser': result[0][5], 'pulverizinglaser' : result[0][6], 'bomb' : result[0][7], 'speedpotion' : result[0][8], 'acidpot' : result[0][9], 'companion' : result[0][10]})

def get_item(name) :
    result = run_sql_return(f'SELECT * FROM items WHERE name = \'{name}\'')
    return json.dumps({'id': result[0][0], 'name': result[0][1], 'price' : result[0][2], 'cooldowntime': result[0][3], 'dmginc': result[0][4]})

def buy_item(username, item_name) :
    data = json.loads(get_item(item_name))
    price = data['price']
    item_name = data['name']
    columnname = item_name.replace(" ", "")
    run_sql(f'UPDATE userinventories SET {columnname} = true FROM userinventories AS ui INNER JOIN users as u ON ui.userid = u.id WHERE  username = \'{username}\' AND {price} <= u.curbalance')
    run_sql(f'UPDATE users SET curbalance = curbalance - {price}')

def get_consumable(name) :
    result = run_sql_return(f'SELECT * FROM consumables WHERE name = \'{name}\'')
    return json.dumps({'id': result[0][0], 'name': result[0][1], 'price' : result[0][2], 'dmg': result[0][3], 'speedinc': result[0][4], 'dmgmult': result[0][5]})

def consume(username, consumable_name) :
    consumable_name = consumable_name.replace(" ", "")
    run_sql(f'UPDATE userinventories SET {consumable_name} = {consumable_name} - 1 FROM users AS u WHERE username = \'{username}\' AND {consumable_name} > 0')

def buy_consumable(username, consumable_name) :
    data = json.loads(get_consumable(consumable_name))
    price = data['price']
    item_name = data['name']
    columnname = item_name.replace(" ", "")
    run_sql(f'UPDATE userinventories SET {columnname} = {columnname} + 1 FROM users AS u WHERE username = \'{username}\' AND {price} <= u.curbalance')
    run_sql(f'UPDATE users SET curbalance = curbalance - {price}')

def get_boss(boss_name) :
    result = run_sql_return(f'SELECT * FROM bosses WHERE name = \'{boss_name}\'')
    return json.dumps({'id': result[0][0], 'name': result[0][1], 'health' : result[0][2], 'image': result[0][3]})

def get_boss_health(boss_name) :
    result = run_sql_return(f'SELECT health FROM bosses WHERE name = \'{boss_name}\'')
    return json.dumps({'health' : result[0][0] })

def run_sql(statement) :
    with conn.cursor() as cur:
        cur.execute(statement)
        conn.commit()

def run_sql_return(statement) :
    with conn.cursor() as cur:
        cur.execute(statement)
        result = cur.fetchall()
        conn.commit()
    return result

def create_all_tables() :
    run_sql('CREATE TABLE users(id serial PRIMARY KEY, username STRING, password STRING, curdmg int, curbalance int)')
    run_sql('CREATE TABLE userinventories(userid serial NOT NULL REFERENCES users (id), icepack BOOL, watercooling BOOL, liquidnitrogen BOOL, damaginglaser BOOL, meltinglaser BOOL, pulverizinglaser BOOL, bomb int, speedpotion int, acidpot int, companion int)')
    run_sql('CREATE TABLE items(id serial PRIMARY KEY, name STRING, price int, cooldowntime int, dmginc int)')
    run_sql('CREATE TABLE consumables(id serial PRIMARY KEY, name STRING, price int, dmg int, speedinc int, dmgmult)')
    run_sql('CREATE TABLE bosses(id serial PRIMARY KEY, name STRING, health int, image varbinary(maxlength))')
    print("all tables are created")

def fill_all_tables() :
    run_sql('INSERT INTO items(name, price, cooldowntime, dmginc) VALUES(\'ice pack\', 100, 10, 0), (\'water cooling\', 1000, 100, 0), (\'liquid nitrogen\', 100000, 1000, 0), (\'damaging laser\', 1000, 0, 1000), (\'melting laser\', 10000, 0, 10000), (\'pulverizing laser\', 10000000, 0, 100000)')
    run_sql('INSERT INTO consumables(name, price, dmg, speedinc, dmgmult) VALUES(\'bomb\', 100, 10000, 0, 0), (\'speed potion\', 1000, 0, 10000, 0), (\'acid pot\', 10000, 0, 0, 2), (\'companion\', 100000, 0, 0, 2)')
    run_sql('INSERT INTO bosses(name, health) VALUES(\'pumpkin king\', 10000000), (\'skeleton head\', 1000000), (\'candy man\', 10000000)')

def clear_all_data() :
    run_sql('DELETE FROM userinventories')
    run_sql('DELETE FROM users')
    run_sql('DELETE FROM bosses')
    run_sql('DELETE FROM items')
    run_sql('DELETE FROM consumables')
    print("all data cleared")

def drop_all_tables() :
    run_sql('DROP TABLE users')
    run_sql('DROP TABLE userinventories')
    run_sql('DROP TABLE bosses')
    run_sql('DROP TABLE items')
    run_sql('DROP TABLE consumables')
    print("all tables dropped")

def test_all_methods() :
    add_user("kilmo", "lima")
    print(get_item("water cooling"))
    print(get_consumable("bomb"))
    print(get_userinventory("kilmo"))
    give_money("kilmo", 10000000000)
    buy_item("kilmo", "water cooling")
    print(get_userinventory("kilmo"))
    buy_consumable("kilmo", "speed potion")
    print(get_userinventory("kilmo"))
    consume("kilmo", "speed potion")
    print(get_userinventory("kilmo"))
clear_all_data()
fill_all_tables()
test_all_methods()