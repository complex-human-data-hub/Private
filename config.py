
ppservers = ()
ppservers_list = []
with open('ppserver.conf', 'r') as f:
    for line in f.readlines():
        s = line.strip()
        if s:
            ppservers_list.append(s)

ppservers = tuple(ppservers_list)

