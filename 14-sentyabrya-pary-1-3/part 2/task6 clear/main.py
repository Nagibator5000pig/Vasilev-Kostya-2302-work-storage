class Message:
    def __init__(self, text, fl_like = False):
        self.text = text
        self.fl_like = fl_like

class Viber:
    msgs = {}

    @classmethod
    def add_message(cls, msg):
        cls.msgs[id(msg)] = msg

    @classmethod
    def remove_message(cls, msg):
        del cls.msgs[id(msg)]

    @classmethod
    def set_like(cls, msg):
        msg.fl_like = not msg.fl_like

    @classmethod
    def total_messages(cls):
        return len(cls.msgs)

msg = Message("Всем привет!")
Viber.add_message(msg)
Viber.add_message(Message("Это курс по Python ООП."))
Viber.add_message(Message("Что вы о нем думаете?"))
Viber.set_like(msg)
print(msg.fl_like)
print(Viber.total_messages())
Viber.remove_message(msg)
print(Viber.total_messages())



