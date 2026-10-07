def make_multiplier(factor):
    def multiply(n):
        return n * factor
    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5), triple(5))


def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


counter_a = make_counter()
counter_b = make_counter()
print(counter_a(), counter_a(), counter_a())
print(counter_b())
