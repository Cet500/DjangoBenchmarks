import decimal
import time
import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.db.models import Avg, Count, DateField
from django.db.models.functions import TruncDate
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TestResult
from .utils import save_test_result, get_full_system_info
from .serializers import TestResultSerializer


def index(request):
    return render(request, 'index.html')


def test_results( request ):
    results = TestResult.objects.all().order_by( '-created_at' )[:100]

    ctx = {
        'results': results
    }

    return render( request, 'performance_tests/results.html', ctx )


def server_info( request ):
    ctx = {
        'info'        : get_full_system_info(),
        'current_time': datetime.datetime.now(),
    }

    return render( request, 'performance_tests/server_info.html', ctx )


def charts( request ):
    ctx = {

    }

    return render( request, 'performance_tests/charts.html', ctx )


def settings_color( request ):
    if request.method == 'POST':
        hue        = request.POST.get( 'hueSlider' )
        saturation = request.POST.get( 'saturationSlider' )

        request.session['user_theme_hue'] = hue
        request.session['user_theme_saturation'] = saturation

        return redirect( 'settings_color' )

    hue        = request.session.get( 'user_theme_hue', 215 )
    saturation = request.session.get( 'user_theme_saturation', 100 )

    ctx = {
        'hue'       : hue,
        'saturation': saturation,
    }

    return render( request, 'settings_color.html', ctx )


@require_GET
def pi_calculation(request, digits):
    if digits > 100000:  # Ограничим максимальное количество знаков для безопасности
        return HttpResponse("Слишком много знаков! Максимум 100000.", status=400)
    
    decimal.getcontext().prec = digits + 2
    
    start_time = time.time()

     # Крайне неэффективный метод (ряд Лейбница)
    pi = decimal.Decimal(0)
    operations = 10**6
    for k in range(1, operations):
        term = decimal.Decimal(4) / (2*k - 1)
        if k % 2 == 1:
            pi += term
        else:
            pi -= term
    
    execution_time = time.time() - start_time

    pi_str = str(pi)[:2 + digits]

    save_test_result(
        test_id = 'pi_calculation',
        test_name = 'Вычисление Pi',
        parameters = { 'digits': digits },
        execution_time = execution_time
    )

    ctx = {
        'name': f'Вычисление числа π с {digits} знаками после запятой',
        'time': f'{execution_time:.4f}',
        'result': pi_str
    }

    return render( request, 'performance_tests/universal_test.html', ctx )


@require_GET
def matrix_mult(request, size):
    if size > 1000:
        return HttpResponse("Слишком большая матрица! Максимум 1000x1000.", status=400)
    
    start_time = time.time()
    
    # Создаём "тяжёлые" матрицы
    matrix = [[i * j for j in range(size)] for i in range(size)]
    
    # Бесполезное перемножение (O(n^3) сложность)
    result = [[0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += matrix[i][k] * matrix[k][j]
                # Искусственное замедление
                if k % 100 == 0:
                    _ = sum(x for x in range(100))
    
    execution_time = time.time() - start_time

    save_test_result(
        test_id = 'matrix_mult',
        test_name = 'Перемножение матриц',
        parameters = { 'size': size },
        execution_time = execution_time
    )

    ctx = {
        'name'  : f'Перемножение матриц {size}x{size}',
        'time'  : f'{execution_time:.4f}',
        'result': result
    }

    return render( request, 'performance_tests/universal_test.html', ctx )


@require_GET
def generate_primes(request, count):
    if count > 1000000:
        return HttpResponse("Слишком много! Максимум 1 000 000 простых чисел.", status=400)
    
    start_time = time.time()
    primes = []
    num = 2
    
    while len(primes) < count:
        is_prime = True

        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        
        if is_prime:
            primes.append(num)

        num += 1
    
    execution_time = time.time() - start_time

    save_test_result(
        test_id = 'generate_primes',
        test_name = 'Простые числа',
        parameters = { 'count': count },
        execution_time = execution_time
    )

    ctx = {
        'name'  : f'Первые {count} простых чисел',
        'time'  : f'{execution_time:.4f}',
        'result': primes
    }

    return render( request, 'performance_tests/universal_test.html', ctx )


@require_GET
def calc_factorial(request, n):
    if n > 10000:
        return HttpResponse("Слишком большое n! Максимум 10000.", status=400)

    _fact_cache = {}    
    start_time = time.time()
    
    def bad_factorial(x):
        if x in _fact_cache:
            return _fact_cache[x]
        if x == 0:
            result = 1
        else:
            result = x * bad_factorial(x - 1)
        _fact_cache[x] = result
        return result
    
    fact = bad_factorial(n)
    execution_time = time.time() - start_time

    save_test_result(
        test_id = 'calc_factorial',
        test_name = 'Факториал числа',
        parameters = { 'n': n },
        execution_time = execution_time
    )

    ctx = {
        'name'  : f'Факториал числа {n}!',
        'time'  : f'{execution_time:.4f}',
        'result': str(fact)
    }

    return render( request, 'performance_tests/universal_test.html', ctx )


@require_GET
def calc_fibonacci(request, n):
    if n > 40:
        return HttpResponse("Слишком большое n! Максимум 40 (алгоритм O(2^n)).", status=400)
    
    start_time = time.time()
    
    def terrible_fib(k):
        if k <= 1:
            return k
        return terrible_fib(k - 1) + terrible_fib(k - 2)

    fib = terrible_fib(n)
    execution_time = time.time() - start_time

    save_test_result(
        test_id = 'calc_fibonacci',
        test_name = 'Число Фибоначчи',
        parameters = { 'n': n },
        execution_time = execution_time
    )

    ctx = {
        'name'  : f'Число Фибоначчи F({n})',
        'time'  : f'{execution_time:.4f}',
        'result': fib
    }

    return render( request, 'performance_tests/universal_test.html', ctx )


@require_GET
def calc_power( request, a, b ):
    if b > 500:
        return HttpResponse( "Слишком большая степень! Не больше 500.", status = 400 )

    start_time = time.time()

    def naive_power( a, b ):
        if b == 0:
            return 1
        return a * naive_power( a, b - 1 )

    result = naive_power( a, b )

    execution_time = time.time() - start_time

    save_test_result(
        test_id = 'calc_power',
        test_name = 'Возведение в степень',
        parameters = { 'a': a, 'b': b },
        execution_time = execution_time
    )

    ctx = {
        'name'  : f'Возведение в степень {a}^{b}',
        'time'  : f'{execution_time:.4f}',
        'result': result
    }

    return render( request, 'performance_tests/universal_test.html', ctx )


@require_GET
def calc_partitions( request, n ):
    if n > 80:
        return HttpResponse( "Слишком большое n! Максимум 80.", status = 400 )

    start_time = time.time()

    def terrible_partitions( n, m = None ):
        if m is None:
            m = n
        if n == 0:
            return 1
        if n < 0 or m == 0:
            return 0
        return terrible_partitions( n - m, m ) + terrible_partitions( n, m - 1 )

    result = terrible_partitions( n )

    execution_time = time.time() - start_time

    save_test_result(
        test_id = 'calc_partitions',
        test_name = 'Вычисление разбиений',
        parameters = { 'n': n },
        execution_time = execution_time
    )

    ctx = {
        'name'  : f'Вычисление разбиений для числа {n}',
        'time'  : f'{execution_time:.4f}',
        'result': result
    }

    return render( request, 'performance_tests/universal_test.html', ctx )


@require_GET
def list_permutations( request, n ):
    if n > 15:
        return HttpResponse( "Слишком большое n! Максимум 15.", status = 400 )

    start_time = time.time()

    def terrible_permutations( lst ):
        if len( lst ) <= 1:
            return [lst]
        perms = []
        for i in range( len( lst ) ):
            rest = lst[:i] + lst[i + 1:]
            for p in terrible_permutations( rest ):
                perms.append( [lst[i]] + p )
        return perms

    result = terrible_permutations( list( range(1, n + 1) ) )

    execution_time = time.time() - start_time

    save_test_result(
        test_id = 'list_permutations',
        test_name = 'Перестановки списка',
        parameters = { 'n': n },
        execution_time = execution_time
    )

    ctx = {
        'name'  : f'Перестановки для списка от 1 до {n}',
        'time'  : f'{execution_time:.4f}',
        'result': result
    }

    return render( request, 'performance_tests/universal_test.html', ctx )


class TestResultViewSet( ModelViewSet ):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

    # 1. Количество тестов по версии Python
    @action( detail = False, methods = ['get'] )
    def count_by_python( self, request ):
        data = TestResult.objects.values( 'python_version' ) \
                .annotate( count = Count( 'id' ) ) \
                .order_by( 'python_version' )
        return Response( data )

    # 2. Среднее время выполнения по версии Python и тесту
    @action( detail = False, methods = ['get'] )
    def time_by_python_test( self, request ):
        data = TestResult.objects.values( 'python_version', 'test_name' ) \
                .annotate( avg_time = Avg( 'execution_time' ) ) \
                .order_by( 'python_version', 'test_name' )
        return Response( data )

    # 3.1. Распределение тестов по CPU (для круговой диаграммы)
    @action(detail=False, methods=['get'])
    def count_by_cpu(self, request):
        data = TestResult.objects.values('cpu') \
               .annotate(count=Count('id')) \
               .order_by('-count')[:10]  # Топ-10
        return Response(data)

    # 3.2. Распределение тестов по RAM (диапазоны)
    @action(detail=False, methods=['get'])
    def count_by_ram(self, request):
        ram_bins = {
            '<=4GB': (0, 4),
            '4-8GB': (4, 8),
            '8-16GB': (8, 16),
            '16-32GB': (16, 32),
            '>32GB': (32, 999)
        }
        result = []
        for label, (min_val, max_val) in ram_bins.items():
            count = TestResult.objects.filter(
                memory__gte=min_val*1024,
                memory__lt=max_val*1024
            ).count()
            result.append({'ram': label, 'count': count})
        return Response(result)

    # 3.3. Распределение тестов по GPU
    @action( detail = False, methods = ['get'] )
    def count_by_gpu( self, request ):
        data = TestResult.objects.values( 'gpu' ) \
                   .annotate( count = Count( 'id' ) ) \
                   .order_by( '-count' )[:5]  # Топ-5
        return Response( data )

    # 4. Количество тестов по дням
    @action( detail = False, methods = ['get'] )
    def count_by_day( self, request ):
        data = TestResult.objects.annotate(
            date = TruncDate( 'created_at', output_field = DateField() )
        ).values( 'date' ) \
            .annotate( count = Count( 'id' ) ) \
            .order_by( 'date' )
        return Response( data )