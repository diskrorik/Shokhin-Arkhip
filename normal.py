from typing import List, Dict
import random
from sympy import symbols, Poly, isprime
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup

def get_parameters(N: int) -> Dict[str, int]:
    """Вычисляет все параметры на основе N"""
    m = 4 + (N % 5)
    n = 2 + (N % 10)
    k = 1 + (N % 7)
    n1 = N % 6
    n2 = (N + 1) % 6
    n3 = (N + 2) % 6

    # Параметры p, s, r, t в зависимости от N mod 5
    mod5 = N % 5

    if mod5 == 0:
        p, s, r, t = 29, 5, 59, 9
    elif mod5 == 1:
        p, s, r, t = 31, 4, 60, 8
    elif mod5 == 2:
        p, s, r, t = 37, 3, 38, 7
    elif mod5 == 3:
        p, s, r, t = 23, 17, 45, 12
    else:
        p, s, r, t = 19, 15, 44, 14

    # Параметры для полиномов
    if mod5 == 0:
        p_field, m_field = 5, 3
    elif mod5 == 1:
        p_field, m_field = 3, 4
    elif mod5 == 2:
        p_field, m_field = 2, 7
    elif mod5 == 3:
        p_field, m_field = 13, 2
    else:
        p_field, m_field = 11, 2

    return {
        'm': m, 'n': n, 'k': k,
        'n1': n1, 'n2': n2, 'n3': n3,
        'p': p, 's': s, 'r': r, 't': t,
        'p_field': p_field, 'm_field': m_field
    }


def gcd(a: int, b: int) -> int:
    """Наибольший общий делитель"""
    while b:
        a, b = b, a % b
    return a


def multiplicative_order(a: int, n: int) -> int:
    """Находит мультипликативный порядок a по модулю n"""
    if gcd(a, n) != 1:
        return -1

    order = 1
    power = a % n
    while power != 1:
        power = (power * a) % n
        order += 1
    return order


def get_prime_factors(n: int) -> List[int]:
    """Находит простые делители числа"""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def subgroups_of_Sm(N: int) -> dict:
    """Находит все подгруппы симметрической группы S_m"""
    params = get_parameters(N)
    m = params['m']

    try:
        # Создаем симметрическую группу S_m
        S_m = SymmetricGroup(m)

        all_subgroups = []
        all_subgroups.append(S_m)

        # Добавляем знакопеременную группу если m >= 2
        if m >= 2:
            try:
                A_m = S_m.alternating_group()
                all_subgroups.append(A_m)
            except:
                pass

        # Добавляем несколько циклических подгрупп
        elements_to_check = S_m.elements[:min(20, len(S_m.elements))]
        for el in elements_to_check:
            try:
                cyclic_sub = el.cyclic_subgroup()
                # Проверяем, что это новая подгруппа
                if not any(sub.is_subgroup(cyclic_sub) for sub in all_subgroups):
                    all_subgroups.append(cyclic_sub)
            except:
                continue

        if all_subgroups:
            random_subgroup = random.choice(all_subgroups)
            index = N % len(all_subgroups)
            selected_subgroup = all_subgroups[index]

            # Смежные классы
            try:
                left_cosets = selected_subgroup.left_coset_decomposition()
                right_cosets = selected_subgroup.right_coset_decomposition()
                left_count = len(left_cosets)
                right_count = len(right_cosets)
            except:
                left_count = right_count = 0

            subgroup_index = S_m.order() // selected_subgroup.order()
            is_normal = selected_subgroup.is_normal(S_m)
        else:
            random_subgroup = selected_subgroup = "Не найдено"
            left_count = right_count = 0
            subgroup_index = is_normal = 0

        return {
            'total_subgroups': len(all_subgroups),
            'random_subgroup': str(random_subgroup)[:100] + "...",
            'selected_subgroup': str(selected_subgroup)[:100] + "...",
            'left_cosets': left_count,
            'right_cosets': right_count,
            'subgroup_index': subgroup_index,
            'is_normal': is_normal
        }
    except Exception as e:
        return {'error': f"Ошибка: {e}"}


def element_powers_in_Sm(N: int) -> dict:
    """Находит порядки элементов и циклических подгрупп в S_m"""
    params = get_parameters(N)
    m = params['m']
    n1, n2, n3 = params['n1'], params['n2'], params['n3']

    try:
        # Создаем симметрическую группу S_m
        S_m = SymmetricGroup(m)

        # Выбираем элемент g с индексом N mod |S_m|
        elements = list(S_m.elements)
        g_index = N % len(elements)
        g = elements[g_index]

        # Вычисляем степени
        g_n1 = g ** n1
        g_n2 = g ** n2
        g_n3 = g ** n3

        # Порядки элементов
        order_g_n1 = g_n1.order()
        order_g_n2 = g_n2.order()
        order_g_n3 = g_n3.order()

        return {
            'g': str(g),
            'g_n1': str(g_n1), 'order_g_n1': order_g_n1,
            'g_n2': str(g_n2), 'order_g_n2': order_g_n2,
            'g_n3': str(g_n3), 'order_g_n3': order_g_n3
        }
    except Exception as e:
        return {'error': f"Ошибка: {e}"}


def solve_sigma_power_eq(N: int) -> dict:
    """Решает уравнение σ^n = (1 2 3 ... m-1) в S_m"""
    params = get_parameters(N)
    m = params['m']
    n = params['n']

    try:
        # Целевая перестановка (1 2 3 ... m-1)
        target = Permutation(list(range(1, m)) + [0])
        S_m = SymmetricGroup(m)
        all_permutations = list(S_m.elements)

        # решения
        solutions = [sigma for sigma in all_permutations if sigma ** n == target]

        # 3 случайных решения
        if solutions:
            random_solutions = random.sample(solutions, min(3, len(solutions)))
        else:
            random_solutions = []

        # общие свойства
        common_properties = f"Все решения имеют порядок, делящий {n}, и являются {n}-ми корнями из цикла длины {m - 1}"

        return {
            'total_solutions': len(solutions),
            'random_solutions': [str(sol) for sol in random_solutions],
            'common_properties': common_properties
        }
    except Exception as e:
        return {
            'error': f"Ошибка: {e}",
            'total_solutions': 0,
            'random_solutions': [],
            'common_properties': 'Не доступно'
        }


def elements_of_order_k_in_cyclic_group(N: int) -> dict:
    """Находит элементы в циклической группе порядка m"""
    params = get_parameters(N)
    m = params['m']
    k = params['k']

    # Циклическая группа порядка m (аддитивная)
    elements_g_k_eq_e = [x for x in range(m) if (x * k) % m == 0]

    # Элементы порядка k
    elements_of_order_k = []
    if m % k == 0:
        for x in range(1, m):
            actual_order = m // gcd(x, m)
            if actual_order == k:
                elements_of_order_k.append(x)

    return {
        'elements_g_k_eq_e': elements_g_k_eq_e,
        'elements_of_order_k': elements_of_order_k,
        'note': f'Элементы порядка {k} существуют только если {k} делит {m}'
    }


def subgroups_of_Zm_star(N: int) -> list:
    """Находит все подгруппы мультипликативной группы Z_m^*"""
    params = get_parameters(N)
    m = params['m']

    # Мультипликативная группа Z_m^*
    Zm_star = [x for x in range(1, m) if gcd(x, m) == 1]

    if not Zm_star:
        return []

    # Для простого m группа циклическая
    if isprime(m):
        order = len(Zm_star)
        divisors = [d for d in range(1, order + 1) if order % d == 0]
        subgroups = []

        for d in divisors:
            for g in Zm_star:
                if pow(g, d, m) == 1:
                    is_minimal = True
                    prime_factors = [p for p in get_prime_factors(d) if p != 1]
                    for p in prime_factors:
                        if d % p == 0 and pow(g, d // p, m) == 1:
                            is_minimal = False
                            break
                    if is_minimal:
                        subgroup = sorted([pow(g, i, m) for i in range(d)])
                        subgroups.append(subgroup)
                        break
        return subgroups
    else:
        # Для составного m возвращаем саму группу и тривиальную подгруппу
        return [Zm_star, [1]]


def order_of_sr(N: int) -> int:
    """Находит порядок элемента s^r в Z_p^*"""
    params = get_parameters(N)
    p, s, r = params['p'], params['s'], params['r']

    # Порядок s^r mod p
    order_s = multiplicative_order(s, p)
    if order_s == -1:
        return -1
    gcd_val = gcd(r, order_s)
    order_sr = order_s // gcd_val

    return order_sr


def order_and_primitivity_of_t(N: int) -> dict:
    """Находит порядок элемента t и проверяет, является ли он образующим"""
    params = get_parameters(N)
    p, t = params['p'], params['t']

    order_t = multiplicative_order(t, p)
    is_primitive = order_t == p - 1

    return {
        'order': order_t,
        'is_primitive': is_primitive
    }


def generators_of_Zm_star(N: int) -> list:
    """Находит все образующие (примитивные корни) циклической группы Z_m^*"""
    params = get_parameters(N)
    m = params['m']

    Zm_star = [x for x in range(1, m) if gcd(x, m) == 1]

    if not Zm_star:
        return []

    generators = []
    group_order = len(Zm_star)

    for g in Zm_star:
        if multiplicative_order(g, m) == group_order:
            generators.append(g)

    return generators


def cyclic_subgroup_in_Zm_additive(N: int) -> dict:
    """Находит циклическую подгруппу в аддитивной группе Z_m"""
    params = get_parameters(N)
    m, t = params['m'], params['t']

    # Циклическая подгруппа порожденная t mod m
    t_mod = t % m
    gcd_val = gcd(m, t_mod)
    subgroup_size = m // gcd_val
    subgroup = [(i * t_mod) % m for i in range(subgroup_size)]
    order = len(subgroup)

    # Порождающие элементы подгруппы
    generators = [x for x in subgroup if gcd(x, m) == gcd_val]

    return {
        'subgroup': subgroup,
        'order': order,
        'generators': generators
    }


def isomorphism_of_cyclic_subgroup_Zm_star(N: int) -> dict:
    """Находит изоморфизм циклической подгруппы в Z_m^*"""
    params = get_parameters(N)
    m, t = params['m'], params['t']

    # Циклическая подгруппа, порожденная t в Z_m^*
    if gcd(t, m) != 1:
        return {'error': 't не взаимно просто с m'}

    order_t = multiplicative_order(t, m)
    subgroup = [pow(t, i, m) for i in range(order_t)]

    # Изоморфна циклической группе порядка order_t
    isomorphic_to = f"Z_{order_t}"

    return {
        'subgroup': subgroup,
        'order': order_t,
        'isomorphic_to': isomorphic_to
    }


def polynomial_roots(N: int) -> dict:
    """Находит корни полиномов над конечными полями"""
    results = {}

    # Полином 1: f(x) = x^9 + sum(a_i x^i) над F_4
    try:
        coeffs1 = [((i + N) % 4) for i in range(9)]
        coeffs1 = [1] + coeffs1  # x^9 + ...

        # полином над F_4
        x = symbols('x')
        poly1 = Poly(coeffs1, x, modulus=4)

        # Находим корни
        poly1_roots = []
        for i in range(4):
            try:
                if poly1.eval(i) % 4 == 0:
                    poly1_roots.append(i)
            except:
                pass
        results['poly1_roots_F4'] = poly1_roots
    except Exception as e:
        results['poly1_error'] = str(e)

    # Полином 2: f(x) = sum(b_i x^i) над F_7
    try:
        coeffs2 = [((i + N) % 7) for i in range(7)]
        x = symbols('x')
        poly2 = Poly(coeffs2, x, modulus=7)

        poly2_roots = []
        for i in range(7):
            try:
                if poly2.eval(i) % 7 == 0:
                    poly2_roots.append(i)
            except:
                pass
        results['poly2_roots_F7'] = poly2_roots
    except Exception as e:
        results['poly2_error'] = str(e)

    return results


def polynomial_factorization(N: int) -> dict:
    """Исследует полиномы на приводимость и факторизует их"""
    results = {}

    # Полином 1 над F_5
    try:
        coeffs1 = [((i + N) % 5) for i in range(5)]
        coeffs1 = [1] + coeffs1  # x^5 + ...
        x = symbols('x')
        poly1 = Poly(coeffs1, x, modulus=5)

        # Проверка на приводимость
        roots1 = []
        for i in range(5):
            if poly1.eval(i) % 5 == 0:
                roots1.append(i)

        results['poly1_reducible'] = len(roots1) > 0
        results['poly1_roots'] = roots1
        results['poly1_degree'] = poly1.degree()
    except Exception as e:
        results['poly1_error'] = str(e)

    # Полином 2 над F_9
    try:
        coeffs2 = [((i + N) % 9) for i in range(4)]
        coeffs2 = [1] + coeffs2  # x^4 + ...
        x = symbols('x')
        poly2 = Poly(coeffs2, x, modulus=9)

        # Для F_9 проверяем корни в простом подполе
        roots2 = []
        for i in range(3):  # F_3 подполе F_9
            if poly2.eval(i) % 3 == 0:
                roots2.append(i)

        results['poly2_has_roots_in_F3'] = len(roots2) > 0
        results['poly2_roots_in_F3'] = roots2
    except Exception as e:
        results['poly2_error'] = str(e)

    return results


def polynomial_gcd(N: int) -> dict:
    """Находит НОД полиномов и его линейное представление"""

    try:
        # Коэффициенты для полиномов над F_11
        coeffs_f = [((i + N) % 11) for i in range(8)]
        coeffs_g = [((i + N) % 11) for i in range(4)]

        x = symbols('x')
        f = Poly(coeffs_f, x, modulus=11)
        g = Poly(coeffs_g, x, modulus=11)

        # Находим НОД
        gcd_poly = f.gcd(g)

        return {
            'f': str(f),
            'g': str(g),
            'gcd': str(gcd_poly),
            'gcd_degree': gcd_poly.degree()
        }
    except Exception as e:
        return {'error': str(e)}


def polynomial_inverse(N: int) -> dict:
    """Находит обратный полином по модулю"""

    try:
        # Полиномы над F_13
        s_coeffs = [((i + N) % 11) % 13 for i in range(3)]
        x = symbols('x')
        f = Poly(s_coeffs, x, modulus=13)

        # x^8 + x^4 + x^3 + 6x + 2
        g = Poly([1, 0, 0, 0, 1, 0, 0, 1, 6, 2], x, modulus=13)
        # Находим обратный
        inverse = f.invert(g)

        return {
            'f': str(f),
            'g': str(g),
            'inverse': str(inverse),
            'verification': str((f * inverse) % g)
        }
    except Exception as e:
        return {'error': f'Обратный элемент не существует или ошибка: {e}'}


def generate_irreducible_polynomials(q: int, d: int) -> list:
    """Генерирует все неприводимые полиномы степени d над F_q"""
    from itertools import product

    irreducible_polys = []
    x = symbols('x')

    # Генерируем все возможные полиномы степени d
    for coeffs in product(range(q), repeat=d + 1):
        if coeffs[0] != 0:
            poly = Poly(coeffs, x, modulus=q)

            # Проверяем на неприводимость
            is_irred = True
            for i in range(q):
                if poly.eval(i) % q == 0:
                    is_irred = False
                    break

            if is_irred:
                irreducible_polys.append(str(poly))

    return irreducible_polys