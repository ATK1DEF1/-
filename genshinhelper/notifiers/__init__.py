#from .bark import Bark
from . import (
    bark,
    telegrambot
)


_all_notifiers = {
    'bark': bark.Bark,
    'telegrambot': telegrambot.TelegramBot,
}

def send(text, status, desp):
    for notifier in _all_notifiers.values():
        notifier().send(text, status, desp)

