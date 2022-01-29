from threading import Thread


def multable(number):
    for i in range(1, 10):
        print(number,":",number * i)


def Main():
    t1 = Thread(target=multable, args=(3,))
    t2 = Thread(target=multable, args=(10,))
    t1.start()
    t2.start()


if __name__ == "__main__":
    Main()
