TOKEN = "475191343:AAGXlZNUjXPlFr6zkq3bIVXY3fCHiF6JB-s"
ALLOWED_UPDATES = 'message', 'edited_message'

botName = "BanBot"
textTrigger = ["@banuser", "/ban", "спам"]

limit: int = 2

chat = None

candidate = None
messageCandidate = None
userTrigger = None
messageTrigger = None
messageBot = None

usersBan_username = []
usersBan = []
usersFree_username = []
usersFree = []


def getStartText():
    return f'Чтобы начать голосование за бан, ' \
           f'ответь на сообщение пользователя одним из триггеров: <b>{", ".join(textTrigger)}</b> \n\n' \
           f'/help'


def getHelpText():
    return "/help — Показывает это сообщение\n" \
           "/limit — Изменить количество голосов для кика пользователя\n" \
           "/addWord — Добавить слово-триггер для начала голосования. Попробуйте например " \
           "<b>\"/addWord кик\"</b>\n " \
           "/removeWord — Удалить слово-триггер для начала голосования. \n\n " \
           f"Текущие слова-триггеры: \n{', '.join(textTrigger)}"


def getAddWordText():
    return f'Теперь затриггерить @{botName} можно с помощью слов: \n<b>{", ".join(textTrigger)}</b>.'


def getRemoveWordText():
    return f'Теперь затриггерить @{botName} можно с помощью слов: \n<b>{", ".join(textTrigger)}</b>.'


def getLimitText():
    return f'Теперь лимит голосующих = {limit}.'
