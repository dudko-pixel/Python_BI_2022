import re
import matplotlib.pylab as plt
## Let's assume we have a references.txt and 2430AD.txt in our directory
# 1. Parsing the references.txt file to extract only ftp links to the ftps.txt file
with open("references.txt", "r") as ref:
    ftps = []
    while True:
        line = ref.readline()
        ftps += re.findall('(?:(?:ftp):\/\/)?[\w/\-?=%.#]+\.[\w/\-&?=%.]+', line)
        if not line:
            break
    with open("ftps.txt", "w+") as out:
        for ss in ftps:
            out.write(ss)
            out.write("\n")

# 2. Parsing the 2430AD.txt file to extract only ftp links to the numbers_ad.txt file
with open("2430AD.txt", "r") as ad:
    numbers = []
    while True:
    # считываем строку
        line = ad.readline()
        numbers += re.findall(r"([0-9][-.\w]*)", line)
    # прерываем цикл, если строка пустая
        if not line:
            break
    # выводим строку
    with open("numbers_ad.txt", "w+") as out:
        for number in numbers:
            out.write(number)
            out.write("\n")
            
# 3. Parsing the 2430AD.txt file to extract only words with letter 'a' to the awords.txt file, case-insensitively
with open("2430AD.txt", "r") as ad:
    awords = []
    while True:
    # считываем строку
        line = ad.readline()
        awords += re.findall(r"\w*[aA]\w*", line)
    # прерываем цикл, если строка пустая
        if not line:
            break
    # выводим строку
    with open("awords.txt", "w+") as out:
        for aword in awords:
            out.write(aword)
            out.write("\n")
            
# 4. Parsing the 2430AD.txt file to extract only sentences with exclamation to the excl.txt file          
with open("2430AD.txt", "r") as ad:
    excls = []
    while True:
    # считываем строку
        line = ad.readline()
        excls += re.findall(r"[\w\s]*\!+", line)
    # прерываем цикл, если строка пустая
        if not line:
            break
    # выводим строку
    with open("excl.txt", "w+") as out:
        for excl in excls:
            out.write(excl)
            out.write("\n")
            
# 5. Plotting histogram of unique words lengths distribution (based on 2430AD.txt file). Case-insensitively
with open("2430AD.txt", "r") as ad:
    words = []
    wordslen = {}
    while True:
        line = ad.readline()
        line_new = re.sub(r"[.\!\?\:,()\"-]+", "", line)
        for word in line_new.lower().split(" "):
            if word not in words:
                words += [word]
                if len(word) not in wordslen:
                    wordslen[len(word)] = 1
                else:
                    wordslen[len(word)] += 1
        if not line:
            break
plt.bar(list(wordslen.keys()), wordslen.values(), color='m')
plt.title("Unique words lengths distribution", weight='bold', style = 'italic', size = 17)
plt.xlabel("word length", weight='bold', style = 'italic')
plt.ylabel("Word quantity", style = 'italic', weight='bold')
plt.show()

# 6. Let's assume that the 'kirpichniy' language origins are somewhere in Russia. Then, to check our translator-function we'll use a Russian phrase. 
def brick_translator(stroka):
    replacements = {"э": "экэ", "е": "еке", "ы": "ыкы", 
                "а": "ака", "у": "уку", "я": "якя", 
                "и": "ики", "ю": "юкю", "о": "око"}
    def func(matchobj): return replacements.get(matchobj.group(), "")
    return re.sub("[уеыаоэяию]", func, stroka.lower(), flags=re.IGNORECASE)
## Below lies a check phrase for our function. 
## As this language is used primarily by children, I guess they are irrespective enough to talk and write only in lowercase.
stri = 'Слушай, а ловко ты это придумал, я даже сначала не понял'
brick_translator(stri)

# 7. Extracting sentences from input phrase, counting words in each sentence and reporting only sentences which length is equal to the input 'n'
def find_n_words_sentences(stroka, n):
    sentences = re.split('[?!.][\s]*',stroka)
    splitted = []
    for sntnce in sentences:
        if len(sntnce.split(" ")) == n:
            splitted += [tuple(sntnce.split(" "))]
    return splitted
## Checking our function using a part of 2430AD.txt file    
find_n_words_sentences("Their footsteps were muted against the plastic-knit crushed rock underfoot. They passed crosscorridors and saw the endless crowds on the Moving Strips in the middle distance. There was a fugitive whiff of plankton in its varieties. Once, almost by instinct, they could tell that up above, far above, was one of the giant conduits leading in from the sea. And by symmetry they knew there would be another conduit, just as large, far below, leading out to sea.", 10)
