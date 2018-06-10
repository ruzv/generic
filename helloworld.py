
def helloworld(i):
    print(i, "Hello World!")

def iter(i, proc, args):
    for a in range(i):
        proc(args)

iter(10, helloworld, 1)