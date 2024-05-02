TOKEN = "475191343:AAGXlZNUjXPlFr6zkq3bIVXY3fCHiF6JB-s"
ALLOWED_UPDATES = 'message', 'edited_message'

botName = "BanBot"
textTrigger = ["@banuser", "спам"]

limit: int = 5

candidate = None
messageCandidate = None
userTrigger = None
messageTrigger = None
messageBot = None

usersBan = []
usersBan_id = []
usersFree = []
usersFree_id = []

helpText = f'Чтобы начать голосование за бан, ' \
           f'ответь на сообщение пользователя одним из триггеров: <b>{", ".join(textTrigger)}</b> \n\n/help'

