import threading
import time
def multiple(num):
    for i in range (10):
        print(num," : ",num*i)
def multiple1(num):
    for i in range (10):
        print(num," : ",num*i)
threads=[]
thread=multiple(3)
thread=multiple(10)