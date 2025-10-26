from collections import OrderedDict
import random
import time


# --- LRU Cache ---
class LRUCache:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# --- Функції для роботи з масивом ---
def range_sum_no_cache(array, left, right):
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right, cache: LRUCache):
    key = (left, right)
    cached_value = cache.get(key)
    if cached_value == -1:
        calc_sum = sum(array[left : right + 1])
        cache.put(key, calc_sum)
        return calc_sum
    return cached_value


def update_with_cache(array, index, value, cache: LRUCache):
    for key in list(cache.cache.keys()):
        left, right = key
        if left <= index <= right:
            del cache.cache[key]
    array[index] = value


# --- Генератор запитів ---
def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


# --- Тест ---
if __name__ == "__main__":
    n = 100_000
    q = 50_000
    array = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)

    cache = LRUCache(capacity=1000)

    # --- Без кешу ---
    start = time.time()
    for qtype, *params in queries:
        if qtype == "Range":
            range_sum_no_cache(array, *params)
        else:
            update_no_cache(array, *params)
    time_no_cache = time.time() - start

    # --- З кешем ---
    start = time.time()
    for qtype, *params in queries:
        if qtype == "Range":
            range_sum_with_cache(array, params[0], params[1], cache)
        else:
            update_with_cache(array, params[0], params[1], cache)
    time_with_cache = time.time() - start

    # --- Вивід ---
    print(f"Без кешу : {time_no_cache:.2f} c")
    print(
        f"LRU-кеш  : {time_with_cache:.2f} c  (прискорення ×{time_no_cache/time_with_cache:.2f})"
    )
