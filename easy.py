from typing import List, Tuple, Dict
import math
import time

def is_palindrome(n: int) -> bool:
    """Проверяет, является ли число палиндромом"""
    s = str(n)
    return s == s[::-1]


def is_prime(n: int) -> bool:
    """Проверяет, является ли число простым"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Наибольший общий делитель"""
    while b:
        a, b = b, a % b
    return a


def palindromic_squares_and_circular_primes() -> Tuple[List[int], List[int]]:
    """
    Возвращает:
    tuple:
    - список всех палиндромов a < 100000, для которых a^2 — палиндром;
    - список всех простых p < 1000000, все циклические перестановки цифр которых просты.
    """
    # Часть 1: палиндромы с палиндромными квадратами
    palindromic_squares = []
    for a in range(1, 100000):
        if is_palindrome(a) and is_palindrome(a * a):
            palindromic_squares.append(a)

    # Часть 2: циклические простые числа
    def get_cyclic_permutations(n: int) -> List[int]:
        """Возвращает все циклические перестановки числа"""
        s = str(n)
        permutations = []
        for i in range(len(s)):
            perm = int(s[i:] + s[:i])
            permutations.append(perm)
        return permutations

    circular_primes = []
    for p in range(2, 100000):
        if is_prime(p):
            permutations = get_cyclic_permutations(p)
            if all(is_prime(perm) for perm in permutations):
                circular_primes.append(p)

    return palindromic_squares, circular_primes


def palindromic_cubes_and_palindromic_primes() -> Tuple[List[int], List[int]]:
    """
    Возвращает:
    tuple:
    - список всех палиндромы a < 100000, для которых a^3 — палиндром;
    - список всех простых p <= 10000, которые являются палиндромами.
    """
    # Часть 1: палиндромы с палиндромными кубами
    palindromic_cubes = []
    for a in range(1, 100000):
        if is_palindrome(a) and is_palindrome(a ** 3):
            palindromic_cubes.append(a)

    # Часть 2: палиндромные простые числа
    palindromic_primes = []
    for p in range(2, 10001):
        if is_prime(p) and is_palindrome(p):
            palindromic_primes.append(p)

    return palindromic_cubes, palindromic_primes


def primes_with_two_digits() -> Dict[str, List[int]]:
    """
    Возвращает словарь вида:
    {
        '13': [список первых 100 простых из {1,3}],
        '15': [список первых 100 простых из {1,5}],
        '17': [список первых 100 простых из {1,7}],
        '19': [список первых 100 простых из {1,9}]
    }
    """

    def generate_primes_with_digits(digit1: int, digit2: int, count: int) -> List[int]:
        """Генерирует простые числа, состоящие только из двух заданных цифр"""
        primes = []
        # Начнем с чисел длиной 1 цифра
        numbers = [digit1, digit2] if digit1 != digit2 else [digit1]

        # Проверяем однозначные числа
        for num in numbers:
            if is_prime(num) and len(primes) < count:
                primes.append(num)

        current_length = 2
        while len(primes) < count:
            new_numbers = []
            for num in numbers:
                for digit in [digit1, digit2]:
                    new_num = num * 10 + digit
                    if is_prime(new_num) and new_num not in primes and len(primes) < count:
                        primes.append(new_num)
                    new_numbers.append(new_num)
            numbers = new_numbers
            current_length += 1

        return sorted(primes)[:count]

    result = {}
    digit_pairs = [(1, 3), (1, 5), (1, 7), (1, 9)]

    for d1, d2 in digit_pairs:
        key = f"{d1}{d2}"
        primes = generate_primes_with_digits(d1, d2, 100)
        result[key] = primes

    return result


def twin_primes_analysis(limit_pairs: int = 1000) -> Tuple[List[Tuple[int, int]], List[float]]:
    """
    Возвращает:
    - список первых `limit_pairs` пар близнецов (p, p+2);
    - список значений отношения pi_2(n) / pi(n) для n, соответствующих последним элементам каждой пары
    """

    def sieve_of_eratosthenes(limit: int) -> List[bool]:
        """Решето Эратосфена для нахождения всех простых до limit"""
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(limit ** 0.5) + 1):
            if sieve[i]:
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False
        return sieve

    # Найдем достаточно большое ограничение
    limit = 10000

    sieve = sieve_of_eratosthenes(limit)
    primes = [i for i, is_prime in enumerate(sieve) if is_prime]

    twin_pairs = []
    for i in range(len(primes) - 1):
        if primes[i + 1] - primes[i] == 2:
            twin_pairs.append((primes[i], primes[i + 1]))
        if len(twin_pairs) >= limit_pairs:
            break

    twin_pairs = twin_pairs[:limit_pairs]

    ratios = []
    prime_count = 0
    twin_count = 0

    for n in range(2, twin_pairs[-1][1] + 1):
        if sieve[n]:
            prime_count += 1
            if n >= 3 and sieve[n - 2]:
                twin_count += 1

        # Добавляем отношение для каждого n, соответствующего второму близнецу в паре
        if any(n == pair[1] for pair in twin_pairs):
            if prime_count > 0:
                ratios.append(twin_count / prime_count)
            else:
                ratios.append(0)

    return twin_pairs, ratios


def factorial_plus_one_factors() -> Dict[int, Dict[int, int]]:
    """
    Возвращает словарь вида:
    { n: {простой_делитель: степень, ...}, ... }
    для n от 2 до 50
    """

    def factorize(n: int) -> Dict[int, int]:
        """Разлагает число на простые множители"""
        factors = {}
        # Проверяем делимость на 2
        while n % 2 == 0:
            factors[2] = factors.get(2, 0) + 1
            n //= 2

        # Проверяем нечетные делители
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            while n % i == 0:
                factors[i] = factors.get(i, 0) + 1
                n //= i

        if n > 1:
            factors[n] = factors.get(n, 0) + 1

        return factors

    result = {}
    for n in range(2, 51):
        # n! + 1
        factorial = 1
        for i in range(1, n + 1):
            factorial *= i

        number = factorial + 1
        factors = factorize(number)
        result[n] = factors

    return result


def euler_phi_direct(n: int) -> int:
    """Вычисляет φ(n) прямым перебором"""
    count = 0
    for k in range(1, n + 1):
        if gcd(k, n) == 1:
            count += 1
    return count


def euler_phi_factor(n: int) -> int:
    """Вычисляет φ(n) через разложение на простые множители"""
    if n == 1:
        return 1

    result = n
    temp = n

    # Обработка делителя 2
    if temp % 2 == 0:
        result -= result // 2
        while temp % 2 == 0:
            temp //= 2

    # Обработка нечетных делителей
    for i in range(3, int(math.sqrt(temp)) + 1, 2):
        if temp % i == 0:
            result -= result // i
            while temp % i == 0:
                temp //= i

    # Если остался простой делитель
    if temp > 1:
        result -= result // temp

    return result


def compare_euler_phi_methods(test_values: List[int]) -> dict:
    """
    Сравнивает время работы трёх методов на заданных значениях.
    Возвращает словарь с тремя списками времён (в секундах).
    """
    times_direct = []
    times_factor = []

    for n in test_values:
        # Метод прямого перебора
        start = time.time()
        result1 = euler_phi_direct(n)
        times_direct.append(time.time() - start)

        # Метод через разложение
        start = time.time()
        result2 = euler_phi_factor(n)
        times_factor.append(time.time() - start)

        if result1 != result2:
            print(f"Ошибка: разные результаты для n={n}: direct={result1}, factor={result2}")

    return {
        'direct': times_direct,
        'factor': times_factor
    }