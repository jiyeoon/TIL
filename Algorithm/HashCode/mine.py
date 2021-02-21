
def get_xyz(n, a, b, c):
    for z in range(c, -1, -1):
        for y in range(b, -1, -1):
            for x in range(a, -1, -1):
                if 2*x + 3*y + 4*z <= n:
                    yield x, y, z

def main(file_path):
    f = open(file_path, "r")
    line = f.readline()
    n, a, b, c = list(map(int, line.split()))
    pizza = []
    while True:
        try:
            line = f.readline()
            tmp = line.split()
            pizza.append(tmp[1:])
        except:
            break
