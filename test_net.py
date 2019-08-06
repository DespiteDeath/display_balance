import requests
import mysql.connector
import mysql
import time
import matplotlib.pyplot as plt


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

    Connect(name, balance)



def Connect(name, balance):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="TYPE_YOUR_PASS",  # напиши пароль для бд
      database="mydatabase"
    )

    mycursor = mydb.cursor()
                                             # создание бд
    # mycursor.execute("CREATE TABLE test_network (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), balance VARCHAR(255))")   # создание таблицы и столбцов

    sql = "INSERT INTO test_network (name, balance) VALUES (%s, %s)"
    val = (name, balance)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

    mycursor.execute("SELECT * FROM test_network")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

    Draw_plot(myresult)



def Draw_plot(_myresult):                       # Вывод графика
    X = [i for i in range(len(_myresult))]
    Y = [_myresult[i][2] for i in X]
    plt.plot(X, Y)
    plt.xlabel('Days')
    plt.ylabel('Balance')
    plt.show()

if __name__ == "__main__":
    # while True:
        Make_array()
        #time.sleep(1)