from heapTree import heapT
from heapArray import heapA

def run_heapT():
    h = heapT.from_list([3,2,1,7,8,4,10,16,12])
    h.remove()
    print(h)

def run_heapA():
    h = heapA.from_list([3, 2, 1, 7, 8, 4, 10, 16, 12])
    h.remove()
    print(h)

def main():
    run_heapA()
    run_heapT()

if __name__ == "__main__":
    main()