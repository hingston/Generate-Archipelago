import multiprocessing
import random
from multiprocessing.pool import Pool

from ttictoc import TicToc

from Archipelago import test


def main():
    """Used to test the Archipelago class.

    Tests 3 random seeds between 0 and 65535 with weathering values of 1, 3, 5 and sea_level values between -20 and 32
    in steps of 4.
    """
    t = TicToc()
    t.tic()
    args = []
    for seed in random.sample(range(0, int("0xFFFF", 16)), 3):
        for weathering in [1, 3, 5]:
            for sea_level in range(-20, 32, 4):
                sea_level = sea_level / 100  # range() can't be used to generate a list of floats
                args.append([seed, weathering, sea_level])
    pool = Pool(multiprocessing.cpu_count())
    print("Total archipelagos being generated:", len(args))
    pool.starmap(test, args)
    pool.close()
    pool.join()
    t.toc()
    print("Total time elapsed (seconds): {0:.2f}".format(t.elapsed))


if __name__ == "__main__":
    main()
