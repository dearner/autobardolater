with open ("pg1041.txt") as k:
    # sonnets = k.readlines()
    sonnet = []
    iter = 1
    while iter < 155:
        for x in range(0, 17):
            sonnet.append(k.readline())
        with open(str(iter) + ".txt", "w") as l:
            l.writelines(sonnet)
        sonnet = []
        iter += 1
