import time


def square(x):
    print(f"start process:{x}")
    square_val = x * x
    print(f"square {x}:{square_val}")
    time.sleep(1)
    print(f"end process:{x}")
