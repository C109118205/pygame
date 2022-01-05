import mariadb
import sys,re

try:
    conn = mariadb.connect(
        user="root",
        password="Skills39",
        host="mbeut.ml",
        port=3306,
        database="pygame_db"
    )
    print('DB connected OK')
except mariadb.Error as e:
    print(f"DB connected error: {e}")
    sys.exit(1)

class connect():
    conn = mariadb.connect(
        user="root",
        password="Skills39",
        host="mbeut.ml",
        port=3306,
        database="pygame_db"
    )
def select_user(name,password):
    accountcheck = conn.cursor()
    accountcheck.execute('SELECT name FROM account where binary name = ?', (name,))
    accountresult = accountcheck.fetchall()

    passwordcheck = conn.cursor()
    passwordcheck.execute('SELECT password FROM account where binary password = ?', (password,))
    passwordresult = passwordcheck.fetchall()

    if len(accountresult) != 0:
        if len(passwordresult) != 0:
            return 1
        else:
            return 2
    else:
        return 0

def login(name,password):
    connect()

    if select_user(name,password) == 1:
        print('password correct')
        return 1
    elif select_user(name,password)== 2:
        print('password error')
        return 0            
    else:
        print('account does not exist')            
        return 0            

def register(name,password):
    if select_user(name,password) == 0:
        account_create = conn.cursor()
        account_create.execute('INSERT INTO account (name,password) VALUES (?, ?)',(name,password))
    # account_result = account_create.fetchall()
        conn.commit()
        print('account Created OK!!!!')

    else:
        print('account already Created')

def create_score(name,score):

    created_score = conn.cursor()
    created_score.execute('INSERT INTO score (name,score) VALUES (?, ?)',(name,score))
    conn.commit()
    print('insert OK')

def select_score(name):
    # show_score_name = conn.cursor()
    # show_score_name.execute('SELECT name FROM score where binary name = ?', (name,))
    # show_score_name_result = show_score_name.fetchall()
    # print(show_score_name_result)
    show_score = conn.cursor()
    show_score.execute('SELECT score FROM score where binary name = ?', (name,))
    show_score_result = show_score.fetchall()
    # for i in show_score_result:
    #     meg = re.sub(r"[^a-zA-Z0-9]","",str(i))
        # message="user:",name, "score:",meg
    return show_score_result

    
# select_score('user01')    
    # return show_score_result
# Get Cursor
cur = conn.cursor()