from heapTree import heapT
from heapArray import heapA, heapAMax
from DEPS import heapAMinMax, heapATwin, Deap
import random


def run_test(heapCls, num = 10000, repeat_cnt = 5):
    print("Test for class:\t" + str(heapCls) + "\n")

    for iter in range(1,repeat_cnt+1):
        print("Test Run: ", iter, " of ", repeat_cnt, "\n")
        if heapCls == heapAMax:
            op_A, op_B = max, min
        else:
            op_A, op_B = min, max

        list = random.sample(range(1, int(num*2)), num)

        if heapCls != heapT:
            y = heapCls()
            y.insert(list)
            assert y.is_valid(), str(list) + "\n" + str(y)
            assert op_A(list) == y.peek(), str(list)
            if heapCls in [heapATwin, heapAMinMax, heapATwin, Deap]:
                assert getattr(y, op_B.__qualname__)() == op_B(list), str(op_B(list)) + "\n" + str(y)

        h = heapCls.from_list(list)
        assert h.is_valid(), str(list) + "\n" + str(h)
        assert op_A(list) == h.peek(), str(op_A(list)) + "\n" + str(h)

        list_rm = []
        for elem in range(0, num//10):
            list_rm.append(elem)
            h.pop()
            m = op_A(list)
            list.remove(m)
            assert h.peek() == op_A(list), str(list) + "\n" + str(h)

        for elem in list_rm:
            h.insert(elem)
            list.append(elem)
            assert h.peek() == op_A(list)

        if heapCls in [heapATwin, heapAMinMax, heapATwin, Deap]:
            assert h.max() == op_B(list)
            for _ in range(0,num//10):
                m1 = h.pop_max()
                m2 = op_B(list)
                list.remove(m2)
                assert getattr(h, op_B.__qualname__)() == op_B(list), str(m1) + "\t" + str(m2) + "\n" + str(list) + "\n" + str(op_B(list)) + "\n" + str(h)

def run_heapT():
    #h = heapT.from_list([3,2,1,7,8,4,10,16,12])
    h = heapT.from_list([2,4,7,5])
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
    list = random.sample(range(1, int(1000)), 20)
    #list = [823096, 372566, 122173, 838524, 73017, 618705, 544062, 972372, 878434, 986564]
    lmax = max(list)
    lmin = min(list)
    print(list)
    a = heapAMinMax.from_list(list)
    print(a)
    hmin = a.peek()
    assert lmin == hmin, str(lmin) + "\t" + str(hmin) + "\n" + str(list) + "\n" + str(a)

def run_twin():
    a = heapATwin.from_list([10,1,3,2,11,0,5, 6, 8, 9, 23])
    a.insert(4)
    a.insert(-1)
    a.insert(-2)
    a.remove()
    a.remove()
    a.remove()
    a.remove()
    a.remove()
    print(a)
    a.pop_max()
    print(a)
    a.pop_max()
    a.pop_max()
    a.pop_max()
    a.pop_max()
    a.pop_max()
    a.pop_max()
    a.pop()
    print(a)

def run_deap():
    #a = heapADeap()
    # a.insert([10,1,3,2,11,0,5, 6, 8, 9, 23])
    # print(a)
    # a.remove()
    # a.remove()
    # a.remove()
    # a.remove()
    # a.remove()
    # a.pop()
    # a.pop()
    # a.pop_max()
    # a.pop_max()
    # print(a)
    #a = Deap.from_list([8,5,13,4,10,9,7,11,0])
    #a = Deap.from_list([15,6,7,14,8,2,16,10,12])
    #a = Deap.from_list([7,88,2,58,13,87,57,36,9,83])
    list = random.sample(range(1, int(100)), 99)
    #list = [7,77,8,14,30,26]
    a = Deap.from_list(list)
    print(a)
    assert a.is_valid() is True, str(list) + "\n" + str(a)



def main():
    #run_heapA()
    #run_heapT()
    #run_heapAMinMax()
    #run_twin()
    #run_deap()
    types = [heapA, heapAMax, heapT, heapATwin, Deap, heapAMinMax ]
    #types = []
    for cls in types:
        run_test(cls)

if __name__ == "__main__":
    main()