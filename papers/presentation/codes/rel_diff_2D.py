def relative_diff_2D(ref, data, steps):
    relative = []
    t = 0
    if (len(ref) != len(data)):
        print("Error: relative difference not possible due to different array lengths")
        return [[0,0]]
    for i in range(len(data)):
        x = data[i][0]-ref[i][0]
        y = data[i][1]-ref[i][1]
        relative.append([t,np.sqrt(x**2+y**2)/np.sqrt(ref[i][0]**2+ref[i][1]**2)])
        t += steps
    return relative