y = 20
def outer():
    y = 20
    def inner():
        nonlocal y
        y = 30
        print(y)

    inner()
    print(y)


outer()
