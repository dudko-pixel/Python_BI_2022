#!/usr/bin/env python
# coding: utf-8

# # Задание 1 (5 баллов)

# Напишите классы **Chat**, **Message** и **User**. Они должны соответствовать следующим требованиям:
# 
# **Chat**:
# + Должен иметь атрибут `chat_history`, где будут храниться все сообщения (`Message`) в обратном хронологическом порядке (сначала новые, затем старые)
# + Должен иметь метод `show_last_message`, выводящий на экран информацию о последнем сообщении
# + Должен иметь метод `get_history_from_time_period`, который принимает два опциональных аргумента (даты с которой и по какую мы ищем сообщения и выдаём их). Метод также должен возвращать объект типа `Chat`
# + Должен иметь метод `show_chat`, выводящий на экран все сообщения (каждое сообщение в таком же виде как и `show_last_message`, но с разделителем между ними)
# + Должен иметь метод `recieve`, который будет принимать сообщение и добавлять его в чат
# 
# **Message**:
# + Должен иметь три обязательных атрибута
#     + `text` - текст сообщения
#     + `datetime` - дата и время сообщения (встроенный модуль datetime вам в помощь). Важно! Это должна быть не дата создания сообщения, а дата его попадания в чат! 
#     + `user` - информация о пользователе, который оставил сообщение (какой тип данных использовать здесь, разберётесь сами)
# + Должен иметь метод `show`, который печатает или возвращает информацию о сообщении с необходимой информацией (дата, время, юзер, текст)
# + Должен иметь метод `send`, который будет отправлять сообщение в чат
# 
# **User**:
# + Класс с информацией о юзере, наполнение для этого класса придумайте сами
# 
# Напишите несколько примеров использования кода, которое показывает взаимодействие между объектами.
# 
# В тексте задания намерено не указано, какие аргументы должны принимать методы, пускай вам в этом поможет здравый смысл)
# 
# В этом задании не стоит флексить всякими продвинутыми штуками, для этого есть последующие
# 
# В этом задании можно использовать только модуль `datetime`

# In[291]:


from datetime import datetime, date

class Chat:
    def __init__(self):
        self.chat_history = []
        
    def show_last_message(self):
        print(self.chat_history[0])
    
    def get_history_from_time_period(self, from_time, to_time):
        period_start = datetime.strptime(from_time)
        period_end = datetime.strptime(to_time)

        history_period = [m for m in self.chat_history if datetime.strptime(m.datetime) >= period_start and datetime.strptime(m.datetime) <= period_end]

        return Chat(history_period)
    
    def show_chat(self):
        for message in self.chat_history[::-1]:
            message.show()
            print()
            
    def recieve(self, message):
        self.chat_history = [message] + self.chat_history

class Message:
    # Ваш код здесь
    def __init__(self, text, user):
        self.text = text
        self.datetime = datetime
        self.user = user
        
    def show(self):
        print(self.user.show_name(), str(self.datetime), '\n', self.text, '\n________________\n')
    
    def send(self, chat):
        self.datetime = datetime.now()
        chat.recieve(self)

class User:
    # Ваш код здесь
    def __init__(self, nickname, greeting):
        self.nickname = nickname
        self.greeting = greeting
    def show_name(self):
        return self.nickname


# In[292]:


chatik = Chat()


# In[283]:


Poirot = User('Poirot', 'Bonjour')
Hastings = User('Hastings', 'Good day!')


# In[293]:


Poirot_message = Message('There are many things not called poison which can kill a man', Poirot).send(chatik)
Hastings_message = Message('Jesus, Mary and Joseph and the wee donkey!', Hastings).send(chatik)


# In[294]:


chatik.show_chat()


# # Задание 2 (3 балла)

# В питоне как-то слишком типично и неинтересно происходят вызовы функций. Напишите класс `Args`, который будет хранить в себе аргументы, а функции можно будет вызывать при помощи следующего синтаксиса.
# 
# Использовать любые модули **нельзя**, да и вряд-ли это как-то поможет)

# In[88]:


class Args:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    
    def __rlshift__(self, other):
        return other(*self.args, **self.kwargs)


# In[89]:


sum << Args([1, 2])


# In[90]:


(lambda a, b, c: a**2 + b + c) << Args(1, 2, c=50)


# # Задание 3 (5 баллов)

# Сделайте класс наследник `float`. Он должен вести себя как `float`, но также должен обладать некоторыми особенностями:
# + При получении атрибутов формата `<действие>_<число>` мы получаем результат такого действия над нашим числом
# + Создавать данные атрибуты в явном виде, очевидно, не стоит
# 
# Подсказка: если в процессе гуглёжки, вы выйдете на такую тему как **"Дескрипторы", то это НЕ то, что вам сейчас нужно**
# 
# Примеры использования ниже

# In[163]:


class StrangeFloat(float):
    def __getattribute__(self, item):
        if '__' not in item:
            operation, value = item.split('_')
            if operation == 'add':
                    return type(self)(self + float(value))
            elif operation == 'subtract':
                    return type(self)(self - float(value))
            elif operation == 'multiply':
                    return type(self)(self * float(value))
            elif operation == 'divide':
                    return type(self)(self / float(value))
            else:
                raise AttributeError


# In[164]:


number = StrangeFloat(3.5)


# In[165]:


number.add_1


# In[166]:


number.subtract_20


# In[167]:


number.multiply_5


# In[168]:


number.divide_25


# In[169]:


number.add_1.add_2.multiply_6.divide_8.subtract_9


# In[170]:


getattr(number, "add_-2.5")   # Используем getattr, так как не можем написать number.add_-2.5 - это SyntaxError


# In[171]:


number + 8   # Стандартные для float операции работают также


# In[172]:


number.as_integer_ratio()   # Стандартные для float операции работают также  (это встроенный метод float, писать его НЕ НАДО)


# # Задание 4 (3 балла)

# В данном задании мы немного отдохнём и повеселимся. От вас требуется заменить в данном коде максимально возможное количество синтаксических конструкций на вызовы dunder методов, dunder атрибутов и dunder переменных.
# 
# Маленькая заметка: полностью всё заменить невозможно. Например, `function()` можно записать как `function.__call__()`, но при этом мы всё ещё не избавляемся от скобочек, так что можно делать так до бесконечности `function.__call__.__call__.__call__.__call__.....__call__()` и при всём при этом мы ещё не избавляемся от `.` для доступа к атрибутам. В общем, замените всё, что получится, не закапываясь в повторы, как в приведённом примере. Чем больше разных методов вы найдёте и используете, тем лучше и тем выше будет балл
# 
# Код по итогу дожен работать и печатать число **4420.0**, как в примере. Структуру кода менять нельзя, просто изменяем конструкции на синонимичные
# 
# И ещё маленькая подсказка. Заменить здесь можно всё кроме:
# + Конструкции `for ... in ...`:
# + Синтаксиса создания лямбда функции
# + Оператора присваивания `=`
# + Конструкции `if-else`

# In[78]:


import numpy as np


matrix = []
for idx in range(0, 100, 10):
    matrix += [list(range(idx, idx + 10))]
    
selected_columns_indices = list(filter(lambda x: x in range(1, 5, 2), range(len(matrix))))
selected_columns = map(lambda x: [x[col] for col in selected_columns_indices], matrix)

arr = np.array(list(selected_columns))

mask = arr[:, 1] % 3 == 0
new_arr = arr[mask]

product = new_arr @ new_arr.T

if (product[0] < 1000).all() and (product[2] > 1000).any():
    print(product.mean())


# In[208]:


import numpy as np


matrix = list.__call__()
for idx in range(0, 100, 10):
    matrix.__iadd__([list(range(idx, idx + 10))])
    
selected_columns_indices = list(filter(lambda x: x in range(1, 5, 2), range(matrix.__len__())))
selected_columns = map(lambda x: [x.__getitem__(col) for col in selected_columns_indices], matrix)

arr = np.array(list.__call__(selected_columns))

mask = arr[:, 1].__mod__(3).__eq__(0)
new_arr = arr.__getitem__(mask)


product = new_arr.__matmul__(new_arr.transpose())

if (product[0].__lt__(1000)).all().__and__((product.__getitem__(2).__gt__(1000)).any()):
    print(product.mean().__str__())


# # Задание 5 (10 баллов)

# Напишите абстрактный класс `BiologicalSequence`, который задаёт следующий интерфейс:
# + Работа с функцией `len`
# + Возможность получать элементы по индексу и делать срезы последовательности (аналогично строкам)
# + Вывод на печать в удобном виде и возможность конвертации в строку
# + Возможность проверить алфавит последовательности на корректность
# 
# Напишите класс `NucleicAcidSequence`:
# + Данный класс реализует интерфейс `BiologicalSequence`
# + Данный класс имеет новый метод `complement`, возвращающий комплементарную последовательность
# + Данный класс имеет новый метод `gc_content`, возвращающий GC-состав (без разницы, в процентах или в долях)
# 
# Напишите классы наследники `NucleicAcidSequence`: `DNASequence` и `RNASequence`
# + `DNASequence` должен иметь метод `transcribe`, возвращающий транскрибированную РНК-последовательность
# + Данные классы не должны иметь <ins>публичных методов</ins> `complement` и метода для проверки алфавита, так как они уже должны быть реализованы в `NucleicAcidSequence`.
# 
# Напишите класс `AminoAcidSequence`:
# + Данный класс реализует интерфейс `BiologicalSequence`
# + Добавьте этому классу один любой метод, подходящий по смыслу к аминокислотной последовательности. Например, метод для нахождения изоэлектрической точки, молекулярного веса и т.д.
# 
# Комментарий по поводу метода `NucleicAcidSequence.complement`, так как я хочу, чтобы вы сделали его опредедённым образом:
# 
# При вызове `dna.complement()` или условного `dna.check_alphabet()` должны будут вызываться соответствующие методы из `NucleicAcidSequence`. При этом, данный метод должен обладать свойством полиморфизма, иначе говоря, внутри `complement` не надо делать условия а-ля `if seuqence_type == "DNA": return self.complement_dna()`, это крайне не гибко. Данный метод должен опираться на какой-то общий интерфейс между ДНК и РНК. Создание экземпляров `NucleicAcidSequence` не подразумевается, поэтому код `NucleicAcidSequence("ATGC").complement()` не обязан работать, а в идеале должен кидать исключение `NotImplementedError` при вызове от экземпляра `NucleicAcidSequence`
# 
# Вся сложность задания в том, чтобы правильно организовать код. Если у вас есть повторяющийся код в сестринских классах или родительском и дочернем, значит вы что-то делаете не так.
# 
# 
# Маленькое замечание: По-хорошему, между классом `BiologicalSequence` и классами `NucleicAcidSequence` и `AminoAcidSequence`, ещё должен быть класс-прослойка, частично реализующий интерфейс `BiologicalSequence`, но его писать не обязательно, так как задание и так довольно большое (правда из-за этого у вас неминуемо возникнет повторяющийся код в классах `NucleicAcidSequence` и `AminoAcidSequence`)

# In[73]:


from abc import ABC, abstractmethod
class BiologicalSequence(ABC):
    def __init__(self, bioseq):
        self.bioseq = bioseq
        
    def __len__(self):
        return len(bioseq)

    def __getitem__(self, idxs):
        return self.bioseq[idxs]

    def check_alphabet(self):
        nuclds = ['A', 'T', 'G', 'C', 'U']
        for letter in self.bioseq:
            if letter not in nuclds:
                return "Oops, that's not a biological sequence! Try again, please (use only ATGCU)"
            
class NucleicAcidSequence(BiologicalSequence):
    def __init__(self, bioseq):
        super().__init__(bioseq)
        
    def complement(self):
        if type(self) == NucleicAcidSequence:
            raise NotImplementedError('A wrong class or a wrong method?')
        compl_pairs = {'A': 'T', 
                       'G': 'C', 
                       'T': 'A', 
                       'C': 'G', 
                       'U': 'A'}
        compl_res = ''
        for nucl in self.bioseq:
            compl_res += compl_pairs[nucl]
        return compl_res
    
    def gc_content(self):
        return (bioseq.count("G") + bioseq.count("C")) / len(bioseq)

class DNASequence(NucleicAcidSequence):
    def __init__(self, bioseq):
        
        super().__init__(bioseq)
    def transcribe(self):
        return self.bioseq.replace("T", "U")

class RNASequence(NucleicAcidSequence):
    pass

class AminoAcidSequence(BiologicalSequence):
    def __init__(self, bioseq):
        
        super().__init__(bioseq)
    def check_aaalphabet(self):
        aacids = 'ARNDBCEQZGHILKMFPSTWYV'
        for letter in self.bioseq:
            if letter not in aacids:
                return "Oops, that's not an aminoacid! Try again, please (use only ARNDBCEQZGHILKMFPSTWYV)"
            
    def prot_weight_calculation(self):
        aacid_weight = {'A': 89, 'C': 121, 'D': 133, 'E': 147, 'F': 165, 
                        'G': 75, 'H': 155, 'I': 131, 'K': 146, 'L': 131, 
                        'M': 149, 'N': 132, 'P': 115, 'Q': 146, 'R': 174, 
                        'S': 105, 'T': 119, 'V': 117, 'W': 204, 'Y': 181}
        prot_weight = 0
        for aa in self.bioseq:
            prot_weight += aacid_weight[aa]
        return prot_weight


# In[77]:


DNASequence('ATAGACjAGT').check_alphabet()


# In[30]:


DNASequence('ATAGACAGT').check_alphabet()


# In[53]:


DNASequence("ATCGCGATCG")[2:5]


# In[69]:


DNA = DNASequence("ATCGCGATCG")


# In[70]:


DNA.check_alphabet()


# In[72]:


NucleicAcidSequence("ATGC").complement()


# In[74]:


prot = AminoAcidSequence('ACDKWQ')


# In[75]:


prot.check_aaalphabet()


# In[76]:


prot.prot_weight_calculation()

