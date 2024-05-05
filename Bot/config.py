TOKEN = "475191343:AAGXlZNUjXPlFr6zkq3bIVXY3fCHiF6JB-s"
ALLOWED_UPDATES = 'message', 'edited_message'

botName = "BanBot"
words_for_ban = ["@banuser", "/ban", "спам"]

limit: int = 2

chat = None

candidate = None
messageCandidate = None
userTrigger = None
messageTrigger = None
messageBot = None

usersBan = []
usersFree = []


def get_start_text():
    return f'Чтобы начать голосование за бан, ' \
           f'ответь на сообщение пользователя одним из триггеров: <b>{", ".join(words_for_ban)}</b> \n\n' \
           f'/help'


def get_help_text():
    return "/help — Показывает это сообщение\n" \
           "/limit — Изменить количество голосов для кика пользователя\n" \
           "/addWord — Добавить слово-триггер для начала голосования. Попробуйте например " \
           "<b>\"/addWord кик\"</b>\n " \
           "/removeWord — Удалить слово-триггер для начала голосования. \n\n " \
           f"Текущие слова-триггеры: \n{', '.join(words_for_ban)}"


def get_add_word_text():
    return f'Теперь затриггерить @{botName} можно с помощью слов: \n<b>{", ".join(words_for_ban)}</b>.'


def get_remove_word_text():
    return f'Теперь затриггерить @{botName} можно с помощью слов: \n<b>{", ".join(words_for_ban)}</b>.'


def get_limit_text():
    return f'Теперь лимит голосующих = {limit}.'
