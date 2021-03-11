from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

add_buttons = CallbackData("btn", "status")
del_buttons = CallbackData("del_btn", "status")
add_mediafile = CallbackData("add_doc", "status")
del_mediafile = CallbackData("del_media", "status")
undo = CallbackData("undo", "status")
next_step = CallbackData("next_step", "status")
post = CallbackData("post", "status")


async def r_i_buttons(type: str, doc_type=True, inline_type=True, next=False):
    murkup = InlineKeyboardMarkup(row_width=1)
    if not next:
        if type == "text":
            if doc_type:
                murkup.insert(
                    InlineKeyboardButton(text="Прикрепить медиафайл", callback_data=add_mediafile.new(status=True))
                )
            else:
                murkup.insert(
                    InlineKeyboardButton(text="Открепить медиафайл", callback_data=del_mediafile.new(status=True))
                )
            if inline_type:
                murkup.insert(
                    InlineKeyboardButton(text="Добавить Кнопки", callback_data=add_buttons.new(status=True)),
                )
            else:
                murkup.insert(
                    InlineKeyboardButton(text="Удалить Кнопки", callback_data=del_buttons.new(status=False))
                )
            murkup.row(
                InlineKeyboardButton(text="Отменить", callback_data=undo.new(status="true")),
                InlineKeyboardButton(text="Далее", callback_data=next_step.new(status="true"))
            )
        else:
            murkup.insert(
                InlineKeyboardButton(text="Добавить Кнопки", callback_data=add_buttons.new(status=False))
            )
            murkup.row(
                InlineKeyboardButton(text="Отменить", callback_data=undo.new(status="true")),
                InlineKeyboardButton(text="Далее", callback_data=next_step.new(status="true"))
            )
    else:
        murkup.row(
            InlineKeyboardButton(text="Отменить", callback_data=undo.new(status="true")),
            InlineKeyboardButton(text="Опубликовать", callback_data=post.new(status="true"))
        )
    return murkup


async def splited(text: str, type: str, doc_status, next = False, new_post = False):
    murkup = InlineKeyboardMarkup(row_width=1)
    if len(text.splitlines()) == 1:
        sp = text.splitlines()
        if len(sp[0].split('|')) == 1:
            sp = sp[0].split('|')
            if len(sp[0].split('-')) == 1:
                return None
            else:
                sp = sp[0].split('-')
                for i in sp:
                    if i == '':
                        return None
                murkup.insert(
                    InlineKeyboardButton(text=sp[0], url=sp[1].split()[0])
                )
        else:
            sp = sp[0].split('|')
            list = []
            for i in sp:
                if i == '':
                    return None
                sp = i.split('-')
                for i in sp:
                    if i == '':
                        return None
                list.append(sp)
            if len(list) == 2:
                murkup.row(
                    InlineKeyboardButton(text=list[0][0], url=list[0][1].split()[0]),
                    InlineKeyboardButton(text=list[1][0], url=list[1][1].split()[0])
                )
            elif len(list) == 3:
                murkup.row(
                    InlineKeyboardButton(text=list[0][0], url=list[0][1].split()[0]),
                    InlineKeyboardButton(text=list[1][0], url=list[1][1].split()[0]),
                    InlineKeyboardButton(text=list[2][0], url=list[2][1].split()[0])
                )
            else:
                return []
    else:
        sp = text.splitlines()
        for i in sp:
            sp = i.split('|')
            line_list = []
            if len(sp) == 1:
                if len(sp[0].split('-')) == 1:
                    return None
                else:
                    sp = sp[0].split('-')
                    for i in sp:
                        if i == '':
                            return None
                    murkup.insert(
                        InlineKeyboardButton(text=sp[0], url=sp[1].split()[0])
                    )
            else:
                for i in sp:
                    if i == '':
                        return []
                    sp = i.split('-')
                    for i in sp:
                        if i == '':
                            return None
                    line_list.append(sp)
                if len(line_list) == 2:
                    murkup.row(
                        InlineKeyboardButton(text=line_list[0][0], url=line_list[0][1].split()[0]),
                        InlineKeyboardButton(text=line_list[1][0], url=line_list[1][1].split()[0])
                    )
                elif len(line_list) == 3:
                    murkup.row(
                        InlineKeyboardButton(text=line_list[0][0], url=line_list[0][1].split()[0]),
                        InlineKeyboardButton(text=line_list[1][0], url=line_list[1][1].split()[0]),
                        InlineKeyboardButton(text=line_list[2][0], url=line_list[2][1].split()[0])
                    )
                else:
                    return None
    if new_post:
        return murkup
    else:
        if not next:
            if type == "text":
                if doc_status:
                    murkup.insert(
                        InlineKeyboardButton(text="Прикрепить медиафайл", callback_data=add_mediafile.new(status='True'))
                    )
                else:
                    murkup.insert(
                        InlineKeyboardButton(text="Открепить медиафайл", callback_data=del_mediafile.new(status='False'))
                    )
                murkup.insert(
                    InlineKeyboardButton(text="Удалить Кнопки", callback_data=del_buttons.new(status=False)),

                )
                murkup.row(
                    InlineKeyboardButton(text="Отменить", callback_data=undo.new(status="true")),
                    InlineKeyboardButton(text="Далее", callback_data=next_step.new(status="true"))
                )
            else:
                murkup.insert(
                    InlineKeyboardButton(text="Удалить Кнопки", callback_data=del_buttons.new(status="False")),

                )
                murkup.row(
                    InlineKeyboardButton(text="Отменить", callback_data=undo.new(status="true")),
                    InlineKeyboardButton(text="Далее", callback_data=next_step.new(status="true"))
                )
        else:
            murkup.row(
                InlineKeyboardButton(text="Отменить", callback_data=undo.new(status="true")),
                InlineKeyboardButton(text="Опубликовать", callback_data=post.new(status="true"))
            )
    return murkup
