import math

# Black Box function that we are trying to optimize
def black_box(a, b, x, n, func_name):
    sum_ = 0
    for i in range(10, 10 + n + 1):
        if func_name == 'cos':
            trig_value = math.cos(math.log2(b**n + 1) * math.pi * x) /\
                         (n + 1) + math.sin(x)**n
        elif func_name == 'sin':
            trig_value = math.sin(math.log2(b**n + 1) * math.pi * x) /\
                         (n + 1) + math.cos(x)**n
        else:
            raise Exception(f'Unknown Function: {func_name}')
        resid = trig_value - math.log2(n + 1)
        div = ((n + 1)**2) * (1 + a + b) * (120 - x**2) * resid + 1 / 2
        if div == 0:
            raise Exception(f"a: {a} , b: {b} , x: {x} , n: {n} , func: {func_name}")
        sum_ += ((x * n + math.log(n + 1)) / div) / (10**15)
    return sum_

if __name__ == "__main__":
    # Solution from the GA
    print(black_box(0, 0.04709331981836146, -10.954410667485824, 13, 'cos'))
