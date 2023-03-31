#!/usr/bin/env python
# coding: utf-8

# # Задание 1 (6 баллов)

# В данном задании мы будем работать со [списком 250 лучших фильмов IMDb](https://www.imdb.com/chart/top/?ref_=nv_mp_mv250)
# 
# 1. Выведите топ-4 *фильма* **по количеству оценок пользователей** и **количество этих оценок** (1 балл)
# 2. Выведите топ-4 лучших *года* (**по среднему рейтингу фильмов в этом году**) и **средний рейтинг** (1 балл)
# 3. Постройте отсортированный **barplot**, где показано **количество фильмов** из списка **для каждого режисёра** (только для режиссёров с более чем 2 фильмами в списке) (1 балл)
# 4. Выведите топ-4 самых популярных *режиссёра* (**по общему числу людей оценивших их фильмы**) (2 балла)
# 5. Сохраните данные по всем 250 фильмам в виде таблицы с колонками (name, rank, year, rating, n_reviews, director) в любом формате (2 балла)
# 
# Использовать можно что-угодно, но полученные данные должны быть +- актуальными на момент сдачи задания

# In[42]:


# Ваше решение здесь
import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import matplotlib.pyplot as plt
from dataclasses import dataclass
from dotenv import load_dotenv
import sys
import time
import datetime
import traceback
import os
import io


# In[79]:


# in case you don't have dotenv install please do pip
# pip install python-dotenv


# In[59]:


# Top 4 movies on IMDB based on rating and number of ratings
response = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mp_mv250")
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("tbody", {"class": "lister-list"})
movies = []
for row in table.find_all("tr"):
    title = row.find("td", {"class": "titleColumn"}).find("a").text.strip()
    rating = float(row.find("td", {"class": "ratingColumn"}).find("strong").text.strip())
    num_ratings = int(row.find("td", {"class": "ratingColumn"}).find("strong")["title"].replace(",", "").split()[3])
    movies.append((title, rating, num_ratings))
movies = sorted(movies, key=lambda x: (x[1], x[2]), reverse=True)
top_movies = movies[:4]
print("Top 4 movies on IMDB (based on rating and number of ratings):")
for i, (title, rating, num_ratings) in enumerate(top_movies):
    print(f"{i+1}. {title} ({rating:.1f} rating, {num_ratings:,d} ratings)")


# In[86]:


# Top 4 best years on IMDB based on mean rating
response = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mp_mv250")
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("tbody", {"class": "lister-list"})

# Create a dictionary to hold the mean ratings for each year
year_ratings = defaultdict(list)
# Extract each movie's title, rating, and year from the table
for row in table.find_all("tr"):
    title = row.find("td", {"class": "titleColumn"}).find("a").text.strip()
    rating = float(row.find("td", {"class": "ratingColumn"}).find("strong").text.strip())
    year = int(row.find("td", {"class": "titleColumn"}).find("span", {"class": "secondaryInfo"}).text.strip("()"))
    year_ratings[year].append(rating)

# Calculate the mean rating for each year, and sort the years by mean rating
mean_ratings = [(year, sum(ratings)/len(ratings)) for year, ratings in year_ratings.items()]
top_years = sorted(mean_ratings, key=lambda x: x[1], reverse=True)[:4]

# Print out the selected years and their mean ratings
print("Top 4 best years on IMDB (based on mean rating):")
for i, (year, mean_rating) in enumerate(top_years):
    print(f"{i+1}. {year} ({mean_rating:.2f})")


# In[78]:


# plotting a barplot with directors' film quantity (only for those with >2 films)

response = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mp_mv250")
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("tbody", {"class": "lister-list"})

director_film_score = {}
for movie in soup.select('td.titleColumn'):
    crew = movie.select('a')[0]['title']
    director = crew.split(',')[0].strip(' (dir.)')
    if director in director_film_score:
        director_film_score[director] += 1
    else:
        director_film_score[director] = 1
director_film_bigscore = {k: v for k, v in director_film_score.items() if v > 2}
director_film_bigscore_sorted = sorted(director_film_bigscore.items(), key=lambda x:x[1])

x = []
y = []
for item in director_film_bigscore_sorted:
    x.append(item[0])
    y.append(item[1])

plt.bar(x, y)
plt.xticks(rotation=90)

plt.title('Great directors and how many times they are directors in 250 top films on IMDB')
plt.ylabel('Film quantity')
plt.show()


# In[76]:


# export info about all 250 films in a csv file
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.imdb.com/chart/top/?ref_=nv_mp_mv250"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

movies = []
for movie in soup.select(".lister-list tr"):
    rank = float(movie.select_one(".posterColumn span[name='ir']")["data-value"])
    title = movie.select_one(".titleColumn a").text
    year = int(movie.select_one(".titleColumn span.secondaryInfo").text.strip("()"))
    rating = float(movie.select_one(".imdbRating strong").text)
    #n_reviews = float(movie.select_one(".imdbRating").text.replace("\n", ""))
    director = movie.select_one(".titleColumn a")["title"].split(",")[0].strip("(dir.)")
    movies.append((rank, title, year, rating, director))

df = pd.DataFrame(movies, columns=["Rank", "Title", "Year", "Rating", "Director"])
df.to_csv("top250films.csv", index=False)


# # Задание 2 (10 баллов)

# Напишите декоратор `telegram_logger`, который будет логировать запуски декорируемых функций и отправлять сообщения в телеграм.
# 
# 
# Вся информация про API телеграм ботов есть в официальной документации, начать изучение можно с [этой страницы](https://core.telegram.org/bots#how-do-bots-work) (разделы "How Do Bots Work?" и "How Do I Create a Bot?"), далее идите в [API reference](https://core.telegram.org/bots/api)
# 
# **Основной функционал:**
# 1. Декоратор должен принимать **один обязательный аргумент** &mdash; ваш **CHAT_ID** в телеграме. Как узнать свой **CHAT_ID** можно найти в интернете
# 2. В сообщении об успешно завершённой функции должны быть указаны её **имя** и **время выполнения**
# 3. В сообщении о функции, завершившейся с исключением, должно быть указано **имя функции**, **тип** и **текст ошибки**
# 4. Ключевые элементы сообщения должны быть выделены **как код** (см. скриншот), форматирование остальных элементов по вашему желанию
# 5. Время выполнения менее 1 дня отображается как `HH:MM:SS.μμμμμμ`, время выполнения более 1 дня как `DDD days, HH:MM:SS`. Писать форматирование самим не нужно, всё уже где-то сделано за вас
# 
# **Дополнительный функционал:**
# 1. К сообщению также должен быть прикреплён **файл**, содержащий всё, что декорируемая функция записывала в `stdout` и `stderr` во время выполнения. Имя файла это имя декорируемой функции с расширением `.log` (**+3 дополнительных балла**)
# 2. Реализовать предыдущий пункт, не создавая файлов на диске (**+2 дополнительных балла**)
# 3. Если функция ничего не печатает в `stdout` и `stderr` &mdash; отправлять файл не нужно
# 
# **Важные примечания:**
# 1. Ни в коем случае не храните свой API токен в коде и не загружайте его ни в каком виде свой в репозиторий. Сохраните его в **переменной окружения** `TG_API_TOKEN`, тогда его можно будет получить из кода при помощи `os.getenv("TG_API_TOKEN")`. Ручное создание переменных окружения может быть не очень удобным, поэтому можете воспользоваться функцией `load_dotenv` из модуля [dotenv](https://pypi.org/project/python-dotenv/). В доке всё написано, но если коротко, то нужно создать файл `.env` в текущей папке и записать туда `TG_API_TOKEN=<your_token>`, тогда вызов `load_dotenv()` создаст переменные окружения из всех переменных в файле. Это довольно часто используемый способ хранения ключей и прочих приватных данных
# 2. Функцию `long_lasting_function` из примера по понятным причинам запускать не нужно. Достаточно просто убедится, что большие временные интервалы правильно форматируются при отправке сообщения (как в примерах)
# 3. Допустима реализация логирования, когда логгер полностью перехватывает запись в `stdout` и `stderr` (то есть при выполнении функций печать происходит **только** в файл)
# 4. В реальной жизни вам не нужно использовать Telegram API при помощи ручных запросов, вместо этого стоит всегда использовать специальные библиотеки Python, реализующие Telegram API, они более высокоуровневые и удобные. В данном задании мы просто учимся работать с API при помощи написания велосипеда.
# 5. Обязательно прочтите часть конспекта лекции про API перед выполнением задания, так как мы довольно поверхностно затронули это на лекции
# 
# **Рекомендуемые к использованию модули:**
# 1. os
# 2. sys
# 3. io
# 4. datetime
# 5. requests
# 6. dotenv
# 
# **Запрещённые модули**:
# 1. Любые библиотеки, реализующие Telegram API в Python (*python-telegram-bot, Telethon, pyrogram, aiogram, telebot* и так далле...)
# 2. Библиотеки, занимающиеся "перехватыванием" данных из `stdout` и `stderr` (*pytest-capturelog, contextlib, logging*  и так далле...)
# 
# 
# 
# Результат запуска кода ниже должен быть примерно такой:
# 
# ![image.png](attachment:620850d6-6407-4e00-8e43-5f563803d7a5.png)
# 
# ![image.png](attachment:65271777-1100-44a5-bdd2-bcd19a6f50a5.png)
# 
# ![image.png](attachment:e423686d-5666-4d81-8890-41c3e7b53e43.png)

# In[22]:


chat_id=284155032
load_dotenv()
token=os.getenv("TG_API_TOKEN")


# In[43]:


def telegram_logger(chat_id):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            filename = f"{func.__name__}.log"
            with io.StringIO() as f:
                sys.stdout = sys.stderr = f
                try: 
                    func(*args, **kwargs)

                    end_time = datetime.datetime.now()
                    emoji = '\U0001F643'
                    message = f"{emoji}Function `{func.__name__}` successfully finished in `{end_time - start_time}`"

                except Exception as e:
                    emoji = '\U0001F92C'
                    message = f"{emoji}Function `{func.__name__}` failed with an exception:\n\n`{str(e.__class__.__name__)}: {str(e)}`\n"
                    
                finally:
                    f1 = io.StringIO(f.getvalue())
                    f1.name = filename
                    if f1.getvalue():
                        files = {'document': f1}
                        values = {'chat_id': chat_id, 'caption': message, 'parse_mode': "Markdown"}
                        requests.post(f"https://api.telegram.org/bot{token}/sendDocument", data=values, files=files)
                    else:
                        values = {'chat_id': chat_id, 'text': message, 'parse_mode': "Markdown"}
                        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=values)
                        # requests.post(f"https://api.telegram.org/bot{token}/sendSticker?chat_id={chat_id}&sticker=CAADAgADOQADfyesDlKEqOOd72VKAg")
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
        return wrapper
    return decorator


@telegram_logger(chat_id)
def good_function():
    print("This goes to stdout")
    print("And this goes to stderr", file=sys.stderr)
    time.sleep(2)
    print("Wake up, Neo")

@telegram_logger(chat_id)
def bad_function():
    print("Some text to stdout")
    time.sleep(2)
    print("Some text to stderr", file=sys.stderr)
    raise RuntimeError("Ooops, exception here!")
    print("This text follows exception and should not appear in logs")
    
@telegram_logger(chat_id)
def long_lasting_function():
    time.sleep(200000000)
    
@telegram_logger(chat_id)
def good_silent_function():
    time.sleep(1)
    
@telegram_logger(chat_id)
def bad_silent_function():
    time.sleep(1)
    raise RuntimeError("Ooops, exception here!")


good_function()

try:
    bad_function()
except Exception:
    pass

# long_lasting_function()

good_silent_function()

try:
    bad_silent_function()
except Exception:
    pass


# # Задание 3
# 
# В данном задании от вас потребуется сделать Python API для какого-либо сервиса
# 
# В задании предложено два варианта: простой и сложный, **выберите только один** из них.
# 
# Можно использовать только **модули стандартной библиотеки** и **requests**. Любые другие модули можно по согласованию с преподавателем.

# ❗❗❗ В **данном задании** требуется оформить код в виде отдельного модуля (как будто вы пишете свою библиотеку). Код в ноутбуке проверяться не будет ❗❗❗

# ## Вариант 1 (простой, 10 баллов)
# 
# В данном задании вам потребуется сделать Python API для сервиса http://hollywood.mit.edu/GENSCAN.html
# 
# Он способен находить и вырезать интроны в переданной нуклеотидной последовательности. Делает он это не очень хорошо, но это лучше, чем ничего. К тому же у него действительно нет публичного API.
# 
# Реализуйте следующую функцию:
# `run_genscan(sequence=None, sequence_file=None, organism="Vertebrate", exon_cutoff=1.00, sequence_name="")` &mdash; выполняет запрос аналогичный заполнению формы на сайте. Принимает на вход все параметры, которые можно указать на сайте (кроме Print options). `sequence` &mdash; последовательность в виде строки или любого удобного вам типа данных, `sequence_file` &mdash; путь к файлу с последовательностью, который может быть загружен и использован вместо `sequence`. Функция должна будет возвращать объект типа `GenscanOutput`. Про него дальше.
# 
# Реализуйте **датакласс** `GenscanOutput`, у него должны быть следующие поля:
# + `status` &mdash; статус запроса
# + `cds_list` &mdash; список предсказанных белковых последовательностей с учётом сплайсинга (в самом конце результатов с сайта)
# + `intron_list` &mdash; список найденных интронов. Один интрон можно представить любым типом данных, но он должен хранить информацию о его порядковом номере, его начале и конце. Информацию о интронах можно получить из первой таблицы в результатах на сайте.
# + `exon_list` &mdash; всё аналогично интронам, но только с экзонами.
# 
# По желанию можно добавить любые данные, которые вы найдёте в результатах

# In[ ]:


# Не пиши код здесь, сделай отдельный модуль
# я честно пыталась, но особо не получилос...


# In[77]:


# убрать в модуль
import genscan_api


# ## Вариант 2 (очень сложный, 20 дополнительных баллов)

# В этом варианте от вас потребуется сделать Python API для BLAST, а именно для конкретной вариации **tblastn** https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=tblastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome
# 
# Хоть у BLAST и есть десктопное приложение, всё-таки есть одна область, где API может быть полезен. Если мы хотим искать последовательность в полногеномных сборках (WGS), а не в базах данных отдельных генов, у нас могут возникнуть проблемы. Так как если мы хотим пробластить нашу последовательность против большого количества геномов нам пришлось бы или вручную отправлять запросы на сайте, или скачивать все геномы и делать поиск локально. И тот и другой способы не очень удобны, поэтому круто было бы иметь способ сделать автоматический запрос, не заходя в браузер.
# 
# Необходимо написать функцию для запроса, которая будет принимать 3 обязательных аргумента: **белковая последовательность**, которую мы бластим, **базу данных** (в этом задании нас интересует только WGS, но по желанию можете добавить какую-нибудь ещё), **таксон**, у которого мы ищем последовательность, чаще всего &mdash; конкретный вид. По=желанию можете добавить также любые другие аргументы, соответствующие различным настройкам поиска на сайте. 
# 
# Функция дожна возвращать список объектов типа `Alignment`, у него должны быть следующие атрибуты (всё согласно результатам в браузере, удобно посмотреть на рисунке ниже), можно добавить что-нибудь своё:
# 
# ![Alignment.png](attachment:e45d0969-ff95-4d4b-8bbc-7f5e481dcda3.png)
# 
# 
# Самое сложное в задании - правильно сделать запрос. Для этого нужно очень глубоко погрузиться в то, что происходит при отправке запроса при помощи инструмента для разработчиков. Ещё одна проблема заключается в том, что BLAST не отдаёт результаты сразу, какое-то время ваш запрос обрабатывается, при этом изначальный запрос не перекидывает вас на страницу с результатами. Задание не такое простое как кажется из описания!

# In[ ]:


# Не пиши код здесь, сделай отдельный модуль

