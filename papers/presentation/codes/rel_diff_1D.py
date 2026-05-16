def relative_diff_1D(ref, data, steps):
    relative = []
    t = 0
    if (len(ref) != len(data)):
        print("Error: relative difference not possible due to different array lengths")
        return [[0,0]]
    for i in range(len(data)):
        if (ref[i][1] == 0):
            print("division by 0")
            relative.append([ref[i][0],0])
        else:
            relative.append([ref[i][0],(data[i][1]-ref[i][1])/ref[i][1]])
        t += steps
    return relative