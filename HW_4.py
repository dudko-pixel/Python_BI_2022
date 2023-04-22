#!/usr/bin/env python
# coding: utf-8

# В формулировке заданий будет использоваться понятие **worker**. Это слово обозначает какую-то единицу параллельного выполнения, в случае питона это может быть **поток** или **процесс**, выбирайте то, что лучше будет подходить к конкретной задаче
# 
# В каждом задании нужно писать подробные аннотиции типов для:
# 1. Аргументов функций и классов
# 2. Возвращаемых значений
# 3. Классовых атрибутов (если такие есть)
# 
# В каждом задании нужно писать докстроки в определённом стиле (какой вам больше нравится) для всех функций, классов и методов

# # Задание 1 (7 баллов)

# В одном из заданий по ML от вас требовалось написать кастомную реализацию Random Forest. Её проблема состоит в том, что она работает медленно, так как использует всего один поток для работы. Добавление параллельного программирования в код позволит получить существенный прирост в скорости обучения и предсказаний.
# 
# В данном задании от вас требуется добавить возможность обучать случайный лес параллельно и использовать параллелизм для предсказаний. Для этого вам понадобится:
# 1. Добавить аргумент `n_jobs` в метод `fit`. `n_jobs` показывает количество worker'ов, используемых для распараллеливания
# 2. Добавить аргумент `n_jobs` в методы `predict` и `predict_proba`
# 3. Реализовать функционал по распараллеливанию в данных методах
# 
# В результате код `random_forest.fit(X, y, n_jobs=2)` и `random_forest.predict(X, y, n_jobs=2)` должен работать в ~1.5-2 раза быстрее, чем `random_forest.fit(X, y, n_jobs=1)` и `random_forest.predict(X, y, n_jobs=1)` соответственно
# 
# Если у вас по каким-то причинам нет кода случайного леса из ДЗ по ML, то вы можете написать его заново или попросить у однокурсника. *Детали* реализации ML части оцениваться не будут, НО, если вы поломаете логику работы алгоритма во время реализации параллелизма, то за это будут сниматься баллы
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона, а также функции и классы из **sklearn** при помощи которых вы изначально писали лес

# In[1]:


from sklearn.base import BaseEstimator
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor
from sklearn.base import BaseEstimator
import multiprocessing
SEED = 111


class RandomForestClassifierCustom(BaseEstimator):
    def __init__(self, n_estimators=10, max_depth=None, max_features=None, random_state=SEED):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.random_state = random_state

        self.trees = [None] * n_estimators
        self.feat_ids_by_tree = [None] * n_estimators
        self.probas = [None] * n_estimators
        
        self.X = None
        self.y = None

    def fit_idx(self, start_idx=0, finish_idx=10):
        for i in range(start_idx, finish_idx):
            np.random.seed(self.random_state + i)
            feature_idx = np.random.choice(self.X.shape[1], size=self.max_features, replace=False)
            self.feat_ids_by_tree[i] = feature_idx 
            bootstrap_idx = np.random.choice(self.X.shape[0], size=self.X.shape[0], replace=True)
            X_bootstrap = self.X[bootstrap_idx][:, feature_idx]
            y_bootstrap = self.y[bootstrap_idx]
            classifier = DecisionTreeClassifier(max_depth=self.max_depth, max_features=self.max_features, random_state=self.random_state)
            classifier.fit(X_bootstrap, y_bootstrap)
            self.trees[i] = classifier
        return self
    
    def caluclate_iterable_idx(self, n_jobs):
        self.iterable_idx = []
        estimator_step = self.n_estimators // n_jobs
        cur_l_idx = 0
        cur_r_idx = estimator_step
        for i in range(0, n_jobs):
            if cur_r_idx <= self.n_estimators:
                self.iterable_idx.append((cur_l_idx, cur_r_idx))
                cur_l_idx = cur_r_idx
                cur_r_idx += estimator_step
            else:
                self.iterable_idx.append((cur_l_idx, self.n_estimators))
    
    def fit(self, X, y, n_jobs=1):
        self.X = X
        self.y = y
        self.caluclate_iterable_idx(n_jobs)

        with multiprocessing.Pool(n_jobs) as pool:
            result = pool.starmap(self.fit_idx, self.iterable_idx)
            self.trees = result[0].trees
            self.feat_ids_by_tree = result[0].feat_ids_by_tree
        return self
    
    def predict_idx(self, start_idx=0, finish_idx=10):
        for i in range(start_idx, finish_idx):
            self.probas[i] = self.trees[i].predict_proba(self.X[:, self.feat_ids_by_tree[i]])
        return self
    
    def predict(self, X, n_jobs=1):
        self.X = X
        self.caluclate_iterable_idx(n_jobs)
        
        with multiprocessing.Pool(n_jobs) as pool:
            result = pool.starmap(self.predict_idx, self.iterable_idx)
            self.probas = result[0].probas
        
        probas = np.mean(self.probas, axis=0)
        predictions = np.argmax(probas, axis=1)
        return predictions
        
    

X, y = make_classification(n_samples=100000)


# In[2]:


random_forest = RandomForestClassifierCustom(max_depth=30, n_estimators=10, max_features=2, random_state=42)


# In[ ]:


get_ipython().run_cell_magic('time', '', '\n_ = random_forest.fit(X, y, n_jobs=1)')


# In[11]:


get_ipython().run_cell_magic('time', '', '\npreds_1 = random_forest.predict(X, n_jobs=1)')


# In[12]:


get_ipython().run_cell_magic('time', '', '\n_ = random_forest.fit(X, y, n_jobs=2)')


# In[13]:


get_ipython().run_cell_magic('time', '', '\npreds_2 = random_forest.predict(X, n_jobs=2)')


# In[7]:


(preds_1 == preds_2).all()   # Количество worker'ов не должно влиять на предсказания


# #### Какие есть недостатки у вашей реализации параллельного Random Forest (если они есть)? Как это можно исправить? Опишите словами, можно без кода (+1 дополнительный балл)

# Ответ пишите тут

# # Задание 2 (9 баллов)

# Напишите декоратор `memory_limit`, который позволит ограничивать использование памяти декорируемой функцией.
# 
# Декоратор должен принимать следующие аргументы:
# 1. `soft_limit` - "мягкий" лимит использования памяти. При превышении функцией этого лимита должен будет отображён **warning**
# 2. `hard_limit` - "жёсткий" лимит использования памяти. При превышении функцией этого лимита должно будет брошено исключение, а функция должна немедленно завершить свою работу
# 3. `poll_interval` - интервал времени (в секундах) между проверками использования памяти
# 
# Требования:
# 1. Потребление функцией памяти должно отслеживаться **во время выполнения функции**, а не после её завершения
# 2. **warning** при превышении `soft_limit` должен отображаться один раз, даже если функция переходила через этот лимит несколько раз
# 3. Если задать `soft_limit` или `hard_limit` как `None`, то соответствующий лимит должен быть отключён
# 4. Лимиты должны передаваться и отображаться в формате `<number>X`, где `X` - символ, обозначающий порядок единицы измерения памяти ("B", "K", "M", "G", "T", ...)
# 5. В тексте warning'ов и исключений должен быть указан текщий объём используемой памяти и величина превышенного лимита
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона, можно писать вспомогательные функции и/или классы
# 
# В коде ниже для вас предопределены некоторые полезные функции, вы можете ими пользоваться, а можете не пользоваться

# In[1]:


pip install psutil


# In[5]:


import os
import psutil
import time
import warnings
from typing import Callable
import multiprocessing


def get_memory_usage(pid):    # Показывает текущее потребление памяти процессом
    process = psutil.Process(pid)
    mem_info = process.memory_info()
    return mem_info.rss


def bytes_to_human_readable(n_bytes):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for idx, s in enumerate(symbols):
        prefix[s] = 1 << (idx + 1) * 10
    for s in reversed(symbols):
        if n_bytes >= prefix[s]:
            value = float(n_bytes) / prefix[s]
            return f"{value:.2f}{s}"
    return f"{n_bytes}B"


def human_readable_to_bytes(human_readable):
    size_name = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    num, unit = float(human_readable[:-1]), human_readable[-1] 
    idx = size_name.index(unit)
    factor = 1024 ** idx
    return num * factor


def memory_limit(soft_limit = None, hard_limit = None, poll_interval = 1):
    def decorator(func: Callable):
        def inner_function():
            process = multiprocessing.Process(target=func)
            process.start()
            soft_limit_only_once = True
            while True:
                mem_usage = get_memory_usage(process.pid)
                if  hard_limit and mem_usage > human_readable_to_bytes(hard_limit):
                    print(f'Memory limit is reached! Memory used: {bytes_to_human_readable(mem_usage)}')
                    process.terminate()
                    return
                elif soft_limit and soft_limit_only_once and mem_usage > human_readable_to_bytes(soft_limit):
                    print(f'Warning! Memory used: {bytes_to_human_readable(mem_usage)}')
                    soft_limit_only_once = False

                time.sleep(poll_interval)
        
        return inner_function
    return decorator


# In[8]:


@memory_limit(soft_limit="512M", hard_limit="1.5G", poll_interval=0.1)
def memory_increment():
    """
    Функция для тестирования
    
    В течение нескольких секунд достигает использования памяти 1.89G
    Потребление памяти и скорость накопления можно варьировать, изменяя код
    """
    lst = []
    for i in range(50000000):
        if i % 500000 == 0:
            time.sleep(0.1)
        lst.append(i)
    return lst


# In[9]:


memory_increment()


# # Задание 3 (11 баллов)

# Напишите функцию `parallel_map`. Это должна быть **универсальная** функция для распараллеливания, которая эффективно работает в любых условиях.
# 
# Функция должна принимать следующие аргументы:
# 1. `target_func` - целевая функция (обязательный аргумент)
# 2. `args_container` - контейнер с позиционными аргументами для `target_func` (по-умолчанию `None` - позиционные аргументы не передаются)
# 3. `kwargs_container` - контейнер с именованными аргументами для `target_func` (по-умолчанию `None` - именованные аргументы не передаются)
# 4. `n_jobs` - количество workers, которые будут использованы для выполнения (по-умолчанию `None` - количество логических ядер CPU в системе)
# 
# Функция должна работать аналогично `***PoolExecutor.map`, применяя функцию к переданному набору аргументов, но с некоторыми дополнениями и улучшениями
#     
# Поскольку мы пишем **универсальную** функцию, то нам нужно будет выполнить ряд требований, чтобы она могла логично и эффективно работать в большинстве ситуаций
# 
# 1. `target_func` может принимать аргументы любого вида в любом количестве
# 2. Любые типы данных в `args_container`, кроме `tuple`, передаются в `target_func` как единственный позиционный аргумент. `tuple` распаковываются в несколько аргументов
# 3. Количество элементов в `args_container` должно совпадать с количеством элементов в `kwargs_container` и наоборот, также значение одного из них или обоих может быть равно `None`, в иных случаях должна кидаться ошибка (оба аргумента переданы, но размеры не совпадают)
# 
# 4. Функция должна выполнять определённое количество параллельных вызовов `target_func`, это количество зависит от числа переданных аргументов и значения `n_jobs`. Сценарии могут быть следующие
#     + `args_container=None`, `kwargs_container=None`, `n_jobs=None`. В таком случае функция `target_func` выполнится параллельно столько раз, сколько на вашем устройстве логических ядер CPU
#     + `args_container=None`, `kwargs_container=None`, `n_jobs=5`. В таком случае функция `target_func` выполнится параллельно **5** раз
#     + `args_container=[1, 2, 3]`, `kwargs_container=None`, `n_jobs=5`. В таком случае функция `target_func` выполнится параллельно **3** раза, несмотря на то, что `n_jobs=5` (так как есть всего 3 набора аргументов для которых нам нужно получить результат, а лишние worker'ы создавать не имеет смысла)
#     + `args_container=None`, `kwargs_container=[{"s": 1}, {"s": 2}, {"s": 3}]`, `n_jobs=5`. Данный случай аналогичен предыдущему, но здесь мы используем именованные аргументы
#     + `args_container=[1, 2, 3]`, `kwargs_container=[{"s": 1}, {"s": 2}, {"s": 3}]`, `n_jobs=5`. Данный случай аналогичен предыдущему, но здесь мы используем и позиционные, и именованные аргументы
#     + `args_container=[1, 2, 3, 4]`, `kwargs_container=None`, `n_jobs=2`. В таком случае в каждый момент времени параллельно будет выполняться **не более 2** функций `target_func`, так как нам нужно выполнить её 4 раза, но у нас есть только 2 worker'а.
#     + В подобных случаях (из примера выше) должно оптимизироваться время выполнения. Если эти 4 вызова выполняются за 5, 1, 2 и 1 секунды, то параллельное выполнение с `n_jobs=2` должно занять **5 секунд** (не 7 и тем более не 10)
# 
# 5. `parallel_map` возвращает результаты выполнения `target_func` **в том же порядке**, в котором были переданы соответствующие аргументы
# 6. Работает с функциями, созданными внутри других функций
# 
# Для базового решения от вас не ожидается **сверххорошая** оптимизация по времени и памяти для всех возможных случаев. Однако за хорошо оптимизированную логику работы можно получить до **+3 дополнительных баллов**
# 
# Вы можете сделать класс вместо функции, если вам удобнее
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона
# 
# Ниже приведены тестовые примеры по каждому из требований

# In[16]:


import multiprocessing

def parallel_map(target_func, args_container=None, kwargs_container=None, n_jobs=None):
    if not n_jobs:
        n_jobs = multiprocessing.cpu_count()
    if not args_container:
        args_container = ()
    if not kwargs_container:
        kwargs_container = {}
    for i in range(0, n_jobs):
        process = multiprocessing.Process(target=target_func, args=args_container, kwargs=kwargs_container)
        process.start()


# In[17]:


import time


# Это только один пример тестовой функции, ваша parallel_map должна уметь эффективно работать с ЛЮБЫМИ функциями
# Поэтому обязательно протестируйте код на чём-нибудбь ещё
def test_func(x=1, s=2, a=1, b=1, c=1):
    time.sleep(s)
    return a*x**2 + b*x + c


# In[18]:


get_ipython().run_cell_magic('time', '', '\n# Пример 2.1\n# Отдельные значения в args_container передаются в качестве позиционных аргументов\nparallel_map(test_func, args_container=[1, 2.0, 3j-1, 4])   # Здесь происходят параллельные вызовы: test_func(1) test_func(2.0) test_func(3j-1) test_func(4)')


# In[18]:


get_ipython().run_cell_magic('time', '', '\n# Пример 2.2\n# Элементы типа tuple в args_container распаковываются в качестве позиционных аргументов\nparallel_map(test_func, [(1, 1), (2.0, 2), (3j-1, 3), 4])    # Здесь происходят параллельные вызовы: test_func(1, 1) test_func(2.0, 2) test_func(3j-1, 3) test_func(4)')


# In[159]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.1\n# Возможна одновременная передача args_container и kwargs_container, но количества элементов в них должны быть равны\nparallel_map(test_func,\n             args_container=[1, 2, 3, 4],\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}, {"s": 3}])\n\n# Здесь происходят параллельные вызовы: test_func(1, s=3) test_func(2, s=3) test_func(3, s=3) test_func(4, s=3)')


# In[42]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.2\n# args_container может быть None, а kwargs_container задан явно\nparallel_map(test_func,\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}, {"s": 3}])')


# In[43]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.3\n# kwargs_container может быть None, а args_container задан явно\nparallel_map(test_func,\n             args_container=[1, 2, 3, 4])')


# In[44]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.4\n# И kwargs_container, и args_container могут быть не заданы\nparallel_map(test_func)')


# In[44]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.4\n# И kwargs_container, и args_container могут быть не заданы\nparallel_map(test_func)')


# In[32]:


get_ipython().run_cell_magic('time', '', '\n# Пример 3.5\n# При несовпадении количеств позиционных и именованных аргументов кидается ошибка\nparallel_map(test_func,\n             args_container=[1, 2, 3, 4],\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}])')


# In[45]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.1\n# Если функция не имеет обязательных аргументов и аргумент n_jobs не был передан, то она выполняется параллельно столько раз, сколько ваш CPU имеет логических ядер\n# В моём случае это 24, у вас может быть больше или меньше\nparallel_map(test_func)')


# In[47]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.2\n# Если функция не имеет обязательных аргументов и передан только аргумент n_jobs, то она выполняется параллельно n_jobs раз\nparallel_map(test_func, n_jobs=2)')


# In[48]:


get_ipython().run_cell_magic('time', '', "\n# Пример 4.3\n# Если аргументов для target_func указано МЕНЬШЕ, чем n_jobs, то используется такое же количество worker'ов, сколько было передано аргументов\nparallel_map(test_func,\n             args_container=[1, 2, 3],\n             n_jobs=5)   # Здесь используется 3 worker'a")


# In[49]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.4\n# Аналогичный предыдущему случай, но с именованными аргументами\nparallel_map(test_func,\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}],\n             n_jobs=5)   # Здесь используется 3 worker\'a')


# In[50]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.5\n# Комбинация примеров 4.3 и 4.4 (переданы и позиционные и именованные аргументы)\nparallel_map(test_func,\n             args_container=[1, 2, 3],\n             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}],\n             n_jobs=5)   # Здесь используется 3 worker\'a')


# In[50]:


get_ipython().run_cell_magic('time', '', "\n# Пример 4.6\n# Если аргументов для target_func указано БОЛЬШЕ, чем n_jobs, то используется n_jobs worker'ов\nparallel_map(test_func,\n             args_container=[1, 2, 3, 4],\n             kwargs_container=None,\n             n_jobs=2)   # Здесь используется 2 worker'a")


# In[51]:


get_ipython().run_cell_magic('time', '', '\n# Пример 4.7\n# Время выполнения оптимизируется, данный код должен отрабатывать за 5 секунд\nparallel_map(test_func,\n             kwargs_container=[{"s": 5}, {"s": 1}, {"s": 2}, {"s": 1}],\n             n_jobs=2)')


# In[57]:


def test_func2(string, sleep_time=1):
    time.sleep(sleep_time)
    return string

# Пример 5
# Результаты возвращаются в том же порядке, в котором были переданы соответствующие аргументы вне зависимости от того, когда завершился worker
arguments = ["first", "second", "third", "fourth", "fifth"]
parallel_map(test_func2,
             args_container=arguments,
             kwargs_container=[{"sleep_time": 5}, {"sleep_time": 4}, {"sleep_time": 3}, {"sleep_time": 2}, {"sleep_time": 1}])


# In[58]:


get_ipython().run_cell_magic('time', '', '\n\ndef test_func3():\n    def inner_test_func(sleep_time):\n        time.sleep(sleep_time)\n    return parallel_map(inner_test_func, args_container=[1, 2, 3])\n\n# Пример 6\n# Работает с функциями, созданными внутри других функций\ntest_func3()')

