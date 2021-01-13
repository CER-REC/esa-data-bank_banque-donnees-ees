import time
from multiprocessing import Pool
from Codes.Section_04_Final_Data_Merge_and_Visualization.square import square


def run():
    starttime = time.time()
    pool = Pool()
    pool.map(square, range(0, 5))
    pool.close()
    endtime = time.time()
    print(f"Time taken {endtime-starttime} seconds")


if __name__ == "__main__":
    run()
