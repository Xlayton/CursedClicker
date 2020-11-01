import random
from datetime import datetime
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

def add_user(email, username, password) :
    run_sql(f'INSERT INTO users(email, username, password, curdmg, curbalance) VALUES (\'{email}\', \'{username}\', \'{password}\', 100, 0)')
    data = json.loads(get_user(email))
    uid = data['id']
    run_sql(f'INSERT INTO userinventories(userid, icepack, watercooling, liquidnitrogen, damaginglaser, meltinglaser, pulverizinglaser, bomb, speedpotion, acidpot, companion) VALUES (\'{uid}\', false, false, false, false, false, false, 0, 0, 0, 0)')
    run_sql(f'INSERT INTO api_keys(key, userid) VALUES(\'{generate_api_key()}\', {uid})')

def get_api_key(email) :
    data = json.loads(get_user(email))
    uid = data['id']
    result = run_sql_return(f'SELECT key FROM api_keys WHERE userid = {uid}')
    return json.dumps({'key' : result[0][0]})

def confirm_key(api_key) :
    result = run_sql_return(f'SELECT * FROM api_keys WHERE key = \'{api_key}\'')
    if result is not None:
        return True
    else :
        return False

def get_user(email) :
    result = run_sql_return(f'SELECT * FROM users WHERE email = \'{email}\'')
    return json.dumps({'id': result[0][0], 'email': result[0][1], 'username': result[0][2], 'password': result[0][3], 'curdmg': result[0][4], 'curbalance': result[0][5]})

def get_users() :
    result = run_sql_return(f'SELECT * FROM users')
    items = []
    for row in result :
        item = ({'id': row[0], 'email': row[1], 'username': row[2], 'password': row[3], 'curdmg': row[4], 'curbalance': row[5]})
        items.append(item)
    return json.dumps(items)

def give_money(email, amount, api_key) :
    run_sql(f'UPDATE users SET curbalance = curbalance + {amount} WHERE email = \'{email}\'')

def get_userinventory(email, api_key) :
    data = json.loads(get_user(email))
    userid = data['id']
    result = run_sql_return(f'SELECT * FROM userinventories WHERE userid = \'{userid}\'')
    return json.dumps({'id': result[0][0], 'icepack': { "value" : result[0][1], "type" : "upgrade", "imgpath" : "/upgrades/ice-pack/icepack1.png"}, 'watercooling': { "value" : result[0][2], "type" : "upgrade", "imgpath" : "/upgrades/water-cooling/water-cooling1.png"}, 'liquidnitrogen' : { "value" : result[0][3], "type" : "upgrade", "imgpath" : "/upgrades/nitrogen/nitrogen1.png"}, 'damaginglaser': { "value" : result[0][4], "type" : "upgrade", "imgpath" : "/upgrades/laser/laser1.png"}, 'meltinglaser': { "value" : result[0][5], "type" : "upgrade", "imgpath" : "/upgrades/laser/laser2.png"}, 'pulverizinglaser' : { "value" : result[0][6], "type" : "upgrade", "imgpath" : "/upgrades/laser/laser3.png"}, 'bomb' : { "value" : result[0][7], "type" : "consumable", "imgpath" : "/consumable/bomb/bomb1.png"}, 'speedpotion' : {"value" : result[0][8], "type" : "consumable", "imgpath" : "/consumable/potion/potion1.png"}, 'acidpot' : {"value" : result[0][9], "type" : "consumable"}, 'companion' : { "value" : result[0][10], "type" : "consumable", "imgpath" : "/consumable/companion/companion1.png"})

def get_item(name) :
    result = run_sql_return(f'SELECT * FROM items WHERE name = \'{name}\'')
    return json.dumps({'id': result[0][0], 'name': result[0][1], 'price' : result[0][2], 'cooldowntime': result[0][3], 'dmginc': result[0][4]})

def buy_item(email, item_name, api_key) :
    data = json.loads(get_item(item_name))
    price = data['price']
    item_name = data['name']
    columnname = item_name.replace(" ", "")
    run_sql(f'UPDATE userinventories SET {columnname} = true FROM userinventories AS ui INNER JOIN users as u ON ui.userid = u.id WHERE  email = \'{email}\' AND {price} <= u.curbalance')
    run_sql(f'UPDATE users SET curbalance = curbalance - {price}')

def get_consumable(name) :
    result = run_sql_return(f'SELECT * FROM consumables WHERE name = \'{name}\'')
    return json.dumps({'id': result[0][0], 'name': result[0][1], 'price' : result[0][2], 'dmg': result[0][3], 'speedinc': result[0][4], 'dmgmult': result[0][5]})

def get_consumables() :
    result = run_sql_return(f'SELECT * FROM consumables')
    items = []
    for row in result :
        item = (row[0], row[1], row[2], row[3], row[4], row[5])
        items.append(item)
    return json.dumps(items)

def consume(email, consumable_name, api_key) :
    consumable_name = consumable_name.replace(" ", "")
    run_sql(f'UPDATE userinventories SET {consumable_name} = {consumable_name} - 1 FROM users AS u WHERE email = \'{email}\' AND {consumable_name} > 0')

def buy_consumable(email, consumable_name, api_key) :
    data = json.loads(get_consumable(consumable_name))
    price = data['price']
    item_name = data['name']
    columnname = item_name.replace(" ", "")
    run_sql(f'UPDATE userinventories SET {columnname} = {columnname} + 1 FROM users AS u WHERE email = \'{email}\' AND {price} <= u.curbalance')
    run_sql(f'UPDATE users SET curbalance = curbalance - {price}')

def get_boss(boss_name) :
    result = run_sql_return(f'SELECT * FROM bosses WHERE name = \'{boss_name}\'')
    return json.dumps({'id': result[0][0], 'name': result[0][1], 'health' : result[0][2]})

def get_boss_health(boss_name) :
    result = run_sql_return(f'SELECT health FROM bosses WHERE name = \'{boss_name}\'')
    return json.dumps({'health' : result[0][0] })

def boss_take_dmg(boss_name, amount, api_key) :
    run_sql(f'UPDATE bosses SET health = health - {amount} WHERE name = \'{boss_name}\'')

def set_boss_health(boss_name, amount) :
    run_sql(f'UPDATE bosses SET health = {amount} WHERE name = \'{boss_name}\'')

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
    run_sql('CREATE TABLE users(id serial PRIMARY KEY, email STRING UNIQUE, username STRING, password STRING, curdmg int, curbalance int)')
    run_sql('CREATE TABLE userinventories(userid serial NOT NULL REFERENCES users (id), icepack BOOL, watercooling BOOL, liquidnitrogen BOOL, damaginglaser BOOL, meltinglaser BOOL, pulverizinglaser BOOL, bomb int, speedpotion int, acidpot int, companion int)')
    run_sql('CREATE TABLE items(id serial PRIMARY KEY, name STRING, price int, cooldowntime int, dmginc int)')
    run_sql('CREATE TABLE consumables(id serial PRIMARY KEY, name STRING, price int, dmg int, speedinc int, dmgmult int)')
    run_sql('CREATE TABLE bosses(id serial PRIMARY KEY, name STRING, health int)')
    run_sql('CREATE TABLE api_keys(key STRING PRIMARY KEY, userid serial REFERENCES users (id))')
    print("all tables are created")

def fill_all_tables() :
    run_sql('INSERT INTO items(name, price, cooldowntime, dmginc) VALUES(\'ice pack\', 100, 200, 0), (\'water cooling\', 1000, 300, 0), (\'liquid nitrogen\', 100000, 400, 0), (\'damaging laser\', 1000, 0, 200), (\'melting laser\', 10000, 0, 300), (\'pulverizing laser\', 10000000, 0, 400)')
    run_sql('INSERT INTO consumables(name, price, dmg, speedinc, dmgmult) VALUES(\'bomb\', 100, 10000, 0, 0), (\'speed potion\', 1000, 0, 10000, 0), (\'acid pot\', 10000, 0, 0, 2), (\'companion\', 100000, 0, 0, 2)')
    run_sql('INSERT INTO bosses(name, health) VALUES(\'pumpkin king\', 10000000), (\'skeleton head\', 10000000), (\'candy man\', 10000000)')
    print("all tables have been filled")

def clear_all_data() :
    run_sql('DELETE FROM userinventories')
    run_sql('DELETE FROM users')
    run_sql('DELETE FROM bosses')
    run_sql('DELETE FROM items')
    run_sql('DELETE FROM consumables')
    run_sql('DELETE FROM api_keys')
    print("all data cleared")

def drop_all_tables() :
    run_sql('DROP TABLE api_keys')
    run_sql('DROP TABLE userinventories')
    run_sql('DROP TABLE users')
    run_sql('DROP TABLE bosses')
    run_sql('DROP TABLE items')
    run_sql('DROP TABLE consumables')
    print("all tables dropped")

def test_all_methods() :
    add_user("kilmo@gmail.com", "kilmo", "lima")
    print(get_users())
    print(get_item("water cooling"))
    print(get_consumable("bomb"))
    print(get_userinventory("kilmo@gmail.com"))
    give_money("kilmo@gmail.com", 100000)
    buy_item("kilmo@gmail.com", "water cooling")
    print(get_userinventory("kilmo@gmail.com"))
    buy_consumable("kilmo@gmail.com", "speed potion")
    print(get_userinventory("kilmo@gmail.com"))
    consume("kilmo@gmail.com", "speed potion")
    print(get_userinventory("kilmo@gmail.com"))
    boss_take_dmg("pumpkin king", 100)
    print(get_boss_health("pumpkin king"))

def avg(value_list):
	num = 0
	length = len(value_list)
	for val in value_list:
		num += val
	return num/length

def generate_api_key() :
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789`!@#$%^&*"
    result = ""
    for x in range(12):
        time = get_time()
        avg = int(time)
        avg = int(avg)
        avg = str(avg)
        new_avg = avg[len(avg)-1] + avg[len(avg)-2]
        new_avg = int(new_avg)
        if new_avg > 70 :
            new_avg = new_avg % 70
        result += alphabet[new_avg]
    return result

#def generate_api_key() :
#    api_key = get_random()
#    print(api_key)
#    secret_code = get_random()
#    print(secret_code)
#    encrypted = ""
#    for x in range(12):
#        encrypted += chr(ord(api_key[x]) + ord(secret_code[x]))
#    return encrypted

def get_time() :
    dt = datetime.now()
    return dt.microsecond