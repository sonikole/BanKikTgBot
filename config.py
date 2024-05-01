TOKEN = "475191343:AAGXlZNUjXPlFr6zkq3bIVXY3fCHiF6JB-s"
ALLOWED_UPDATES = 'message', 'edited_message'

botName = "BanBot"
textTrigger = ["@banuser", "драка"]

limit: int = 5
count_ban: int = 0
count_free: int = 0

candidate = None
messageCandidate = None
userTrigger = None
messageTrigger = None
messageBot = None

usersBan = []
usersFree = []

helpText = f'Ответь на спам-сообщение {textTrigger}, чтобы начать голосование за бан пользователя.\n/help'

