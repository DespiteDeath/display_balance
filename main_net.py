import requests
import mysql.connector
import mysql
import time
import matplotlib.pyplot as plt

headers = {                             # не нужно
    'Accept': 'application/json',
    'X-API-Key': '3PCVD89BsnM8rRFCL8Jznr6UjQgtAjS6Pgi',
}

response = requests.get('https://nodes-testnet.wavesnodes.com/addresses/balance/details/3MrjzP6Wq9nYDtPtePch1q9Jh59ZQHuArFK', headers=headers)
output = response.text.split(',')
# output = output[-1].replace("}", "")
#3PCVD89BsnM8rRFCL8Jznr6UjQgtAjS6Pgi - мой акк
#3PQDNJ2KVerxekikEdaQ9bHan56guNSBtjx

# https://nodes-testnet.wavesnodes.com/addresses/balance/details/3MrjzP6Wq9nYDtPtePch1q9Jh59ZQHuArFK  # запрос для testnet
# https://nodes.wavesnodes.com/assets/balance/3PQDNJ2KVerxekikEdaQ9bHan56guNSBtjx   # запрос для mainnet

# for x in range(0, len(output)):
#     print(output[x].split(' ')[-1])

def Make_array():

    sub = '\"balance\"'
    sub2 = '\"name\"'
    sub3 = '\"WBTC\"'
    #print ("\n".join(s for s in output if (sub in s or sub3.lower() in s.lower())))

    # print ("\n".join(s for s in output if (sub.lower() in s.lower() or sub2.lower() in s.lower())))

    balance_and_name = []
    b_app = []

    for s in output:
        if sub.lower() in s.lower() or sub2.lower() in s.lower():
            balance_and_name.append(s)
    print(balance_and_name)  # просто список list



    i = 0
    while i < len(balance_and_name):
        b_app.append(balance_and_name[i] + " " + balance_and_name[i+1])
        i = i + 2

    print(b_app)  # массив с индексами

    # for i in range(len(b_app)):
    #     b_app[i] = b_app[i].replace('\"balance\":', '')  # чистим от лишних символов
    #     b_app[i] = b_app[i].replace('\"name\":', '')
    #     b_app[i] = b_app[i].replace('\"', '')


    search_w = "\"WBTC\""           # ищем одну валюту для графика

    for y in b_app:
        if search_w in y:
            num = b_app.index(y)
            print(y , "\nindex = ", b_app.index(y))

    b_app[num] = b_app[num].replace('\"balance\":', '')  # чистим от лишних символов, но не будет похожего https://WBTC.TK
    b_app[num] = b_app[num].replace('\"name\":', '')
    b_app[num] = b_app[num].replace('\"', '')

    print(b_app[num])

    divided = b_app[num].split()
    balance = divided[0]
    name = divided[1]

    print("Balance = ", balance)
    print("Name = ", name)


    balance_and_name.clear()
    b_app.clear()

    Connect(name, balance)


#print ("\n".join(s for s in output if (sub.lower() in s.lower() or sub2.lower() in s.lower())))  варинат с name,balance
#print ("\n".join(s for s in output if sub in s))   варинат с balance

def Connect(name, balance):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="TYPE_YOUR_PASS",  # напиши пароль для бд
      database="mydatabase"
    )

    mycursor = mydb.cursor()

    # mycursor.execute("CREATE TABLE quantor_account (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), balance VARCHAR(255))")   # создание таблицы и столбцов

    sql = "INSERT INTO quantor_account (name, balance) VALUES (%s, %s)"
    val = (name, balance)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

    mycursor.execute("SELECT * FROM quantor_account")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

    inp = len(myresult)-1
    Draw_plot(myresult, inp)


def Draw_plot(_myresult, _inp):                       # Вывод графика
    X = [inp for inp in range(_myresult[_inp][0])]
    Y = [_myresult[inp][2] for inp in X]
    plt.plot(X, Y)
    plt.xlabel('Days')
    plt.ylabel('Balance')
    plt.show()

if __name__ == "__main__":
    while True:
        Make_array()
        time.sleep(5)