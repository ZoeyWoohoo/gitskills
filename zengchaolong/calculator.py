# coding:utf-8


def cal(s):
    wtf = s.replace("-","+-")
    first = wtf.split("+")
    d = 0
    g = 0
    final = 0
    for i in range(len(first)):
        if first[i] == "":
            first[i] = "0"
        else:
             pass
    for a in range(0,len(first)):
        if "*" in first[a]:
            b = first[a].split("*")
            d = d + 1
            for c in range(0,len(b)):
                d *= float(b[c])
            first[a] = str(d)
        elif "/" in first[a]:
            g = g + 1
            e = first[a].split("/")
            for f in range(0,len(e)):
                g /= float(e[f])
            h = e[0]
            j = float(h)
            g = g*j**2
            first[a] = str(g)
        else:
            pass
    for k in range(len(first)):
        num = float(first[k])
        final += num
    return final