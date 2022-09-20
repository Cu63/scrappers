from urllib.request import urlopen
from random import randint


def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum


def retrieveRandomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word


def buildWordDict(text):
    # удаляем разрывы
    text = text.replace('\n', ' ')
    text = text.replace('"', '')

    # Убедимся, что знаки препинания рассматриваются как отдельные "слова",
    # чтобы они тоже включались в цепь Мароква.
    punctuation = [',', '.', ';', ':']
    for symbol in punctuation:
        text = text.replace(symbol, ' {} '.format(symbol))

    words = text.split(' ')
    # убираем пустышки
    words = [word for word in words if word != '']

    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
            # Созаем новый словарь
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] += 1
    return wordDict


text = str(urlopen('https://pythonscraping.com/files/inaugurationSpeech.txt')
           .read(), 'utf-8')
wordDict = buildWordDict(text)

# Генерируем цепь Маркова
length = 100
chain = ['I']
for i in range(9, length):
    newWord = retrieveRandomWord(wordDict[chain[-1]])
    chain.append(newWord)

print(' '.join(chain))
