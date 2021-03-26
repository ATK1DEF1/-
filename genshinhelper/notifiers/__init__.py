from . import (
    bark,
    coolpush,
    customnotifier,
    dingtalkbot,
    igot,
    pushplus,
    serverchan,
    serverchanturbo,
    telegrambot,
    wechatworkapp,
    wechatworkbot,
)

_all_notifiers = {
    'bark': bark.Bark,
    'coolpush': coolpush.CoolPush,
    'customnotifier': customnotifier.CustomNotifier,
    'dingtalkbot': dingtalkbot.DingTalkBot,
    'igot': igot.Igot,
    'pushplus': pushplus.PushPlus,
    'serverchan': serverchan.ServerChan,
    'serverchanturbo': serverchanturbo.ServerChanTurbo,
    'telegrambot': telegrambot.TelegramBot,
    'wechatworkapp': wechatworkapp.WechatWorkApp,
    'wechatworkbot': wechatworkbot.WechatWorkBot,
}


def send(text='Genshin Impact Helper', status='status', desp='desp'):
    for notifier in _all_notifiers.values():
        notifier().send(text, status, desp)
