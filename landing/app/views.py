from collections import Counter
from pprint import pprint

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


class AdTest():

    def __init__(self):
        self.counter_show_original = 0
        self.counter_show_test = 0

    def process_transition(self, request):
        value = request.GET.get('ab_test_arg', 'None')

        if value == 'original':
            self.counter_show_original += 1

        elif value == 'test':
            self.counter_show_test += 1


    def counting_relationships(self):
        summ = self.counter_show_test + self.counter_show_original

        if summ == 0:
            self.test_conversion = 0
            self.original_conversion = 0
        else:
            self.test_conversion = self.counter_show_test / summ
            self.original_conversion = self.counter_show_original / summ

    def print_class(self):
        print(f'ORIGINAL = {self.counter_show_original}       TEST = {self.counter_show_test}')
        print('----------------------------------------------')


AD_TEST = AdTest()


def index(request):
        AD_TEST.process_transition(request)
        AD_TEST.print_class()

        return render(None, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов

    index(request)
    # AD_TEST.process_transition(request)
    if request.GET.get('ab_test_arg') == 'original':
        return render(None, 'landing.html')

    else:
        return render(None, 'landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:

    AD_TEST.counting_relationships()

    return render(None, 'stats.html', context={
        'test_conversion': AD_TEST.test_conversion,
        'original_conversion': AD_TEST.original_conversion,
    })
