def regula_falsi(f: callable, a: float, b: float, epsilon: float):
    c = a - (b-a)/(f(b)-f(a)) * f(a)
    while abs(f(c)) > epsilon:
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        c = a - (b-a)/(f(b)-f(a)) * f(a)
    
    return c





    
    