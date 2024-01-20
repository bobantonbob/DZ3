import concurrent.futures
import logging
import time
import platform
import psutil
from multiprocessing import Pool, cpu_count

# Налаштування логера
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# Функція для виводу зеленим кольором
def print_green(text):
    print("\033[92m{}\033[0m".format(text))

def factorize(numbers: list) -> list:
    result_list = []
    for number in numbers:
        temp_list = []
        for num in range(1, number + 1):
            if number % num == 0:
                temp_list.append(num)
        result_list.append(temp_list)
    return result_list

def factorize_multy(number: int) -> list:
    result_list = []
    for num in range(1, number + 1):
        if number % num == 0:
            result_list.append(num)
    return result_list

if __name__ == "__main__":
    lst = [128, 255, 99999, 10651060, 1236585, 6543646]

    # Створення об'єкта логера
    logger = logging.getLogger(__name__)

    # Синхронна версія
    start_time = time.time()
    a, b, c, d, *_ = factorize(lst)
    end_time = time.time()
    logger.info(f"Sync time is: {end_time - start_time}")
    logger.info("Success synchron")
    # print("Sync time is:", end_time - start_time)
    # print("Success synchron")

    # Інформація про процесор
    processor_name = platform.processor()
    print_green("Processor: {}".format(processor_name))

    # Перевірка кількості фізичних і логічних ядер процесора
    num_physical_cores = psutil.cpu_count(logical=False)
    num_logical_cores = psutil.cpu_count(logical=True)
    print_green("Number of physical CPU cores: {}".format(num_physical_cores))
    print_green("Number of logical CPU cores: {}".format(num_logical_cores))

    # Тести функції factorize
    a_expected = [1, 2, 4, 8, 16, 32, 64, 128]
    b_expected = [1, 3, 5, 15, 17, 51, 85, 255]
    c_expected = [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    d_expected = [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    assert a == a_expected
    assert b == b_expected
    assert c == c_expected
    assert d == d_expected

    # Паралельна версія з multiprocessing.Pool
    start_time_multy = time.time()
    with Pool(processes=num_physical_cores) as pool:
        result = pool.map(factorize_multy, lst)
    end_time_multy = time.time()
    logger.info(f"Multy_pool time is: {end_time_multy - start_time_multy}")
    # print("Multy_pool time is:", end_time_multy - start_time_multy)

    # Паралельна версія з concurrent.futures.ProcessPoolExecutor
    start_time_multy2 = time.time()
    with concurrent.futures.ProcessPoolExecutor(num_physical_cores) as executor:
        result2 = list(executor.map(factorize_multy, lst))
    end_time_multy2 = time.time()
    logger.info(f"Sync time mylty concarent is: {end_time_multy2 - start_time_multy2}")
    # print("Sync time mylty concarent is:", end_time_multy2 - start_time_multy2)

    # Повернення результатів з функцій
    print("Results:")
    print("Sync:", a, b, c, d)
    print("Multy_pool:", result)
    print("Sync time mylty concarent:", result2)
