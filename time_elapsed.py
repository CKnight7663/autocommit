reshuffle_method = []
scan_method = []



reshuffle_method.append([0.16112542152404785, 100])

reshuffle_method.append([0.1607363224029541, 100])

reshuffle_method.append([0.16616058349609375, 100])

reshuffle_method.append([0.16493463516235352, 100])

reshuffle_method.append([0.15279841423034668, 100])

reshuffle_method.append([0.1660904884338379, 100])

reshuffle_method.append([0.1678476333618164, 100])

reshuffle_method.append([0.18563199043273926, 100])

reshuffle_method.append([0.1726055145263672, 100])

reshuffle_method.append([0.17061424255371094, 100])

reshuffle_method.append([0.1770172119140625, 100])

reshuffle_method.append([0.17369890213012695, 100])

reshuffle_method.append([0.17420411109924316, 100])


scan_method.append([0.21445536613464355, 100])

scan_method.append([0.20615053176879883, 100])

scan_method.append([0.22427082061767578, 100])

scan_method.append([0.21225857734680176, 100])

scan_method.append([0.22568249702453613, 100])

scan_method.append([0.22971510887145996, 100])

scan_method.append([0.22121977806091309, 100])

scan_method.append([0.2181546688079834, 100])

scan_method.append([0.2783188819885254, 100])

scan_method.append([0.21743130683898926, 100])

scan_method.append([0.2282395362854004, 100])

scan_method.append([0.21164488792419434, 100])

scan_method.append([0.19872355461120605, 100])



def avg(times):
    sum = 0
    for i in range(len(times)):
        a, b = times[i]
        sum += a/b
    average = sum/len(times)
    return average



print('Shuffle = {0}\nScan = {1}'.format(avg(reshuffle_method), avg(scan_method)))