from heapTree import heapT
from heapArray import heapA, heapAMax, heapAMinMax

def run_heapT():
    h = heapT.from_list([3,2,1,7,8,4,10,16,12])
    h.remove()
    print(h)

def run_heapA():
    y = heapA()
    y.insert([3, 2, 1, 7, 8, 4, 10, 16, 12])
    print(y)
    y.remove()
    print(y)
    h = heapA.from_list([3, 2, 1, 7, 8, 4, 10, 16, 12])
    print(h)
    h.remove()
    print(h)


def run_heapAMinMax():
    h = heapAMinMax()
    h.insert(10)
    h.insert(1)
    h.insert(3)
    h.insert(2)
    h.insert(11)
    h.insert(0)
    h.insert(5)
    print(h)
    a = heapAMinMax.from_list([10,1,3,2,11,0,5, 6, 8, 9, 23])
    print(a)
    a.pop_max()
    print(a)
    a.pop()
    print(a)

def main():
    #run_heapA()
    #run_heapT()
    run_heapAMinMax()

if __name__ == "__main__":
    main()