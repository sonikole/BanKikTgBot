TOKEN = "475191343:AAGXlZNUjXPlFr6zkq3bIVXY3fCHiF6JB-s"
ALLOWED_UPDATES = 'message', 'edited_message'

botName = "BanBot"
messageBan = "@BanUser"

limit = 5
count_ban: int = 0
count_free: int = 0
candidate = "null"
userTrigger = "null"
messageToEdit_id = -1
messageToBan = "null"
usersBan = []
usersFree = []

helpText = f'Ответь на спам-сообщение "{messageBan}", чтобы начать голосование за бан пользователя.\n/help'

