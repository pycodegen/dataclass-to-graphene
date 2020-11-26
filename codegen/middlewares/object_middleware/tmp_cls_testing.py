class TestClass:
    def __init__(self, a: int):
        self.a = a

    def some_func(self, b: int):
        return self.a + b


if __name__ == '__main__':
    a = TestClass(1)
    print(TestClass.some_func(a, 1))