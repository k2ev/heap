from heapTree import heapTree

def main():
    h = heapTree.from_list([3,2,1,7,8,4,10,16,12])
    h.remove()
    print(h)

if __name__ == "__main__":
    main()