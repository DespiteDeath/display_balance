import requests
import mysql.connector
import mysql
import time
import matplotlib.pyplot as plt
from decimal import Decimal
import datetime

response = requests.get('https://nodes-testnet.wavesnodes.com/addresses/balance/details/3MtN7bbr8sNsqNA1m9XemxKEdpMAUauosAX')
output = response.text.split(',')
print(output)


def Make_array():

    sub = '\"regular\"'

    balance_and_name = []


    for s in output:
        if sub.lower() in s.lower():
            balance_and_name.append(s)
    print(balance_and_name)         # просто список list



    for y in balance_and_name:
        if sub in y:
            num = balance_and_name.index(y)
            print(y , "\nindex = ", balance_and_name.index(y))

    balance_and_name[num] = balance_and_name[num].replace('\"', '')  # чистим от лишних символов
    balance_and_name[num] = balance_and_name[num].replace(':', ' ')

    print(balance_and_name[num])

    divided = balance_and_name[num].split()

    name = divided[0]
    balance = divided[1]

    print("Balance = ", balance)
    print("Name = ", name)

    balance_and_name.clear()

    Connect(name, int(balance))



def Connect(name, balance):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="TYPE_YOUR_PASS",  # напиши пароль для бд
      database="mydatabase"
    )

    mycursor = mydb.cursor()                                             # создание бд
    # mycursor.execute("CREATE TABLE test_network (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), balance INT(255), timestamp TIMESTAMP(6))")   # создание таблицы и столбцов

    mycursor.execute(
        "CREATE TABLE balances (id INT AUTO_INCREMENT PRIMARY KEY, id_balance VARCHAR(255), id_acсount VARCHAR(255), balance_date VARCHAR(255),"
        "amount VARCHAR(255), id_currency VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE accounts (id INT AUTO_INCREMENT PRIMARY KEY, id_acсount VARCHAR(255), id_trader VARCHAR(255), key_adress VARCHAR(255),"
        "id_currency VARCHAR(255), api_key1 VARCHAR(255), api_key2 VARCHAR(255), id_marketplace VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE currences (id INT AUTO_INCREMENT PRIMARY KEY, id_currency VARCHAR(255), name VARCHAR(255), ticker VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE trader (id INT AUTO_INCREMENT PRIMARY KEY, id_trader VARCHAR(255), name VARCHAR(255), id_country VARCHAR(255),"
        "email VARCHAR(255), login VARCHAR(255), pass VARCHAR(255), phone_nbr VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE depo_amounts (id INT AUTO_INCREMENT PRIMARY KEY, id_amount VARCHAR(255), id_acсount VARCHAR(255), id_currency VARCHAR(255),"
        " sum VARCHAR(255), direction VARCHAR(255), sum_date VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE countries (id INT AUTO_INCREMENT PRIMARY KEY, id_country VARCHAR(255), country_name VARCHAR(255), shortname VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE marketplaces (id INT AUTO_INCREMENT PRIMARY KEY, id_marketplace VARCHAR(255), marketplace VARCHAR(255))")


    # sql = "INSERT INTO test_network (name, balance, timestamp) VALUES (%s, %s, %s)"
    # now = datetime.datetime.now().timestamp()
    # print(now)
    # val = (name, int(balance), now)
    # mycursor.execute(sql, val)
    # mydb.commit()
    # print(mycursor.rowcount, "record inserted.")
    #
    # mycursor.execute("SELECT * FROM test_network")
    # myresult = mycursor.fetchall()
    # for x in myresult:
    #     print(x)
    #
    # Draw_plot(myresult, now)



def Draw_plot(_myresult, _now):                       # Вывод графика
    X = [i for i in range(int(_now))]
    Y = [_myresult[i][2] for i in X]
    plt.plot(X, Y)
    plt.xlabel('Days')
    plt.ylabel('Balance')
    plt.show()

if __name__ == "__main__":
    # while True:
        Make_array()
        #time.sleep(1)