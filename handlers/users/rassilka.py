import asyncio
import datetime
from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hide_link
from keyboards.default.admin_panel import admin_buttons
from keyboards.inline.r_inline_buttons import r_i_buttons, add_buttons, splited, del_buttons, add_mediafile, \
    del_mediafile, undo, next_step, post
from loader import dp, telegraph, usersdb, bot
from states.rassilka_state import RassilkaState, AddButtonState, AddMediaFileState


@dp.message_handler(text="📢Рассылка")
async def rassilka(message: types.Message):
    text = 'Отправьте боту то, что хотите рассылать. ' \
           'Это может быть всё, что угодно – текст, фото, видео, аудио, документ!))'
    await message.answer(text)
    await RassilkaState.type.set()


@dp.message_handler(state=RassilkaState.type, content_types=types.ContentTypes.TEXT)
async def r_text(message: types.Message, state: FSMContext):
    text = message.text
    murkup = await r_i_buttons(type="text")
    await message.answer(text, reply_markup=murkup)
    await state.update_data({
        "type": "text",
        "text": text,
        "realtext": text,
        "ib": None,
        "am": None
    })
    await state.reset_state(with_data=False)


@dp.message_handler(state=RassilkaState.type, content_types=types.ContentTypes.PHOTO)
async def r_photo(message: types.Message, state: FSMContext):
    text = message.caption
    print(message)
    photo = message.photo[-1].file_id
    murkup = await r_i_buttons(type="other")
    await message.answer_photo(photo=photo, caption=text, reply_markup=murkup)
    await state.update_data({
        "type": "photo",
        "text": text,
        "file_id": photo
    })
    await state.reset_state(with_data=False)


@dp.message_handler(state=RassilkaState.type, content_types=types.ContentTypes.VIDEO)
async def r_video(message: types.Message, state: FSMContext):
    text = message.caption
    video = message.video.file_id
    murkup = await r_i_buttons(type="other")
    await message.answer_video(video=video, caption=text, reply_markup=murkup)
    await state.update_data({
        "type": "video",
        "text": text,
        "file_id": video
    })
    await state.reset_state(with_data=False)


@dp.message_handler(state=RassilkaState.type, content_types=types.ContentTypes.DOCUMENT)
async def r_document(message: types.Message, state: FSMContext):
    text = message.caption
    document = message.document.file_id
    murkup = await r_i_buttons(type="other")
    await message.answer_document(document=document, caption=text, reply_markup=murkup)
    await state.update_data({
        "type": "document",
        "text": text,
        "file_id": document
    })
    await state.reset_state(with_data=False)


@dp.message_handler(state=RassilkaState.type, content_types=types.ContentTypes.AUDIO)
async def r_audio(message: types.Message, state: FSMContext):
    text = message.caption
    audio = message.audio.file_id
    murkup = await r_i_buttons(type="other")
    await message.answer_audio(audio=audio, caption=text, reply_markup=murkup)
    await state.update_data({
        "type": "audio",
        "text": text,
        "file_id": audio
    })
    await state.reset_state(with_data=False)


@dp.message_handler(state=RassilkaState.type, content_types=types.ContentTypes.ANY)
async def r_format_none(message: types.Message, state: FSMContext):
    await message.answer("Формат не известен")
    text = 'Выберите Действие 👇'
    await message.answer(text=text, reply_markup=admin_buttons)
    await state.finish()


@dp.callback_query_handler(add_buttons.filter())
async def add_button(call: types.CallbackQuery):
    await call.answer(cache_time=50)
    text = """Отправьте мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:

Кнопка 1 - http://example1.com
Кнопка 2 - http://example2.com


Используйте разделитель |, чтобы добавить до трех кнопок в один ряд. Пример:

Кнопка 1 - http://example1.com | Кнопка 2 - http://example2.com
Кнопка 3 - http://example3.com | Кнопка 4 - http://example4.com



Нажмите кнопку «Отмена», чтобы вернуться к добавлению сообщений."""
    await call.message.answer(text)
    await AddButtonState.text.set()


@dp.message_handler(state=AddButtonState.text)
async def button_text(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if data.get("am") is None:
        murkup = await splited(text=message.text, type=data.get("type"), doc_status=True)
    else:
        murkup = await splited(text=message.text, type=data.get("type"), doc_status=False)

    if murkup is None:
        await message.answer("Неправильный формат, попытайся снова")
    else:
        if data.get("type") == "text":
            if data.get("am") is None:
                await message.answer(text=f'{data.get("text")}', reply_markup=murkup)
            else:
                await message.answer(text=f'{data.get("text")}', reply_markup=murkup)
        elif data.get("type") == "photo":
            await message.answer_photo(photo=data.get("file_id"), caption=f'{data.get("text")}', reply_markup=murkup)
        elif data.get("type") == "video":
            await message.answer_video(video=data.get("file_id"),  caption=f'{data.get("text")}', reply_markup=murkup)
        elif data.get("type") == "document":
            await message.answer_document(document=data.get("file_id"), caption=f'{data.get("text")}',
                                          reply_markup=murkup)
        elif data.get("type") == "audio":
            await message.answer_audio(audio=data.get("file_id"),
                                       caption=f'{data.get("text")}',
                                       reply_markup=murkup)
        await state.update_data({
            "ib": message.text
        })
        await state.reset_state(with_data=False)


@dp.callback_query_handler(del_buttons.filter())
async def del_buttons(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=50)
    data = await state.get_data()
    if data.get("type") == "text":
        if data.get("am") is None:
            murkup = await r_i_buttons(type="text")
        else:
            murkup = await r_i_buttons(type="text", doc_type=False)
    else:
        murkup = await r_i_buttons(type="other", inline_type=True)
    await state.update_data({
        "ib": None
    })
    await call.message.edit_reply_markup(murkup)


@dp.callback_query_handler(add_mediafile.filter())
async def add_doc(call: types.CallbackQuery):
    await call.answer(cache_time=50)
    await call.message.answer("Отправь Медиафайл")
    await AddMediaFileState.media.set()


async def photo_link(photo: types.photo_size.PhotoSize):
    with await photo.download(BytesIO()) as file:
        links = await telegraph.upload(file)
    return links[0]


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AddMediaFileState.media)
async def media_add(message: types.Message, state: FSMContext):
    photo_msg = message.photo[-1]
    photo = await photo_link(photo=photo_msg)
    data = await state.get_data()
    text = hide_link(photo) + f'{data.get("text")}'
    if data.get("ib") is None:
        murkup = await r_i_buttons(type="text", doc_type=False)
        await message.answer(text=text, reply_markup=murkup)
    else:
        murkup = await splited(text=data.get("ib"), type='text', doc_status=False)
        await message.answer(text, reply_markup=murkup)
    await state.update_data({
        "text": text,
        "am": photo_msg
    })
    await state.reset_state(with_data=False)


@dp.callback_query_handler(del_mediafile.filter())
async def del_mediafile(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=50)
    data = await state.get_data()
    if data.get("ib") is None:
        murkup = await r_i_buttons(type=data.get("type"), doc_type=True)
        await call.message.edit_text(text=data.get("realtext"), reply_markup=murkup)
    else:
        murkup = await splited(data.get("ib"), type=data.get("type"), doc_status=True)
        await call.message.edit_text(text=data.get("realtext"), reply_markup=murkup)
    await state.update_data({
        "type": "text",
        "text": data.get("realtext"),
        "am": None
    })


@dp.callback_query_handler(undo.filter())
async def undo_all(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=50)
    text = 'Выберите Действие 👇'
    await call.message.answer(text=text, reply_markup=admin_buttons)
    await state.finish()


@dp.callback_query_handler(next_step.filter())
async def next(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=50)
    data = await state.get_data()
    if data.get("ib") is None:
        murkup = await r_i_buttons(type="other", next=True)
    else:
        murkup = await splited(text=data.get("ib"), type='other', doc_status=True, next=True)


    if data.get("type") == "text":
        if data.get("ib") is None:
            murkup = await r_i_buttons(type="text", next=True)
        else:
            murkup = await splited(text=data.get("ib"), type='text', next=True, doc_status=True)
        if data.get("am") is None:
            await call.message.answer(text=f'{data.get("text")}', reply_markup=murkup)
        else:
            await call.message.answer(text=f'{data.get("text")}', reply_markup=murkup)
    elif data.get("type") == "photo":
        await call.message.answer_photo(photo=data.get("file_id"),
                                   caption=f'{data.get("text")}',
                                   reply_markup=murkup)
    elif data.get("type") == "video":
        await call.message.answer_video(video=data.get("file_id"),
                                   caption=f'{data.get("text")}',
                                   reply_markup=murkup)
    elif data.get("type") == "document":
        await call.message.answer_document(document=data.get("file_id"),
                                      caption=f'{data.get("text")}',
                                      reply_markup=murkup)
    elif data.get("type") == "audio":
        await call.message.answer_audio(audio=data.get("file_id"),
                                   caption=f'{data.get("text")}',
                                   reply_markup=murkup)


async def protsent_rssilki(protsent, one_protsent, user_id, message_id):
    if protsent % one_protsent == 0:
        rp = protsent // one_protsent
        await bot.edit_message_text(text=f"Процесс Рассылки {rp}%", chat_id=user_id, message_id=message_id)
    else:
        return False


@dp.callback_query_handler(post.filter())
async def post(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=50)
    data = await state.get_data()
    users = usersdb.select_all_users()
    await call.message.answer(f"👥Количество Пользователей сейчас {len(users)}")
    rassilka_time = len(users) * 0.05
    await call.message.answer(f"⌚️Время рассылки продлится около: {datetime.timedelta(seconds=round(rassilka_time))}")
    if data.get("ib") is None:
        murkup = None
    else:
        murkup = await splited(text=data.get("ib"), type='other', doc_status=True, new_post=True)

    message_id = await bot.send_message(chat_id=call.from_user.id, text=f"Процесс Рассылки 0%")
    protsent = 0
    one_protsent = round(len(users) / 100)
    # users_protsent = len(users) // 100
    if data.get("type") == "text":
        if data.get("ib") is None:
            murkup = None
        else:
            murkup = await splited(text=data.get("ib"), type='text', doc_status=True, new_post=True)
        if data.get("am") is None:
            for i in users:
                try:
                    await bot.send_message(i[0], text=f'{data.get("text")}', reply_markup=murkup)
                except:
                    usersdb.delete_user(i[0])

                protsent += 1
                protses = await protsent_rssilki(protsent=protsent,
                                                 one_protsent=one_protsent,
                                                 user_id=call.from_user.id,
                                                 message_id=message_id.message_id)
                await asyncio.sleep(0.05)
        else:
            for i in users:
                try:
                    await bot.send_message(i[0], text=f'{data.get("text")}', reply_markup=murkup)
                except:
                    usersdb.delete_user(i[0])

                protsent += 1
                protses = await protsent_rssilki(protsent=protsent,
                                                 one_protsent=one_protsent,
                                                 user_id=call.from_user.id,
                                                 message_id=message_id.message_id)
                await asyncio.sleep(0.05)
    elif data.get("type") == "photo":
        for i in users:
            try:
                await bot.send_photo(i[0], photo=data.get("file_id"),
                                                caption=f'{data.get("text")}',
                                                reply_markup=murkup)
            except:
                usersdb.delete_user(i[0])

            protsent += 1
            protses = await protsent_rssilki(protsent=protsent,
                                             one_protsent=one_protsent,
                                             user_id=call.from_user.id,
                                             message_id=message_id.message_id)
            await asyncio.sleep(0.05)

    elif data.get("type") == "video":
        for i in users:
            try:
                await bot.send_video(i[0], video=data.get("file_id"),
                                                caption=f'{data.get("text")}',
                                                reply_markup=murkup)
            except:
                usersdb.delete_user(i[0])

            protsent += 1
            protses = await protsent_rssilki(protsent=protsent,
                                             one_protsent=one_protsent,
                                             user_id=call.from_user.id,
                                             message_id=message_id.message_id)
            await asyncio.sleep(0.05)
    elif data.get("type") == "document":
        for i in users:
            try:
                await bot.send_document(i[0], document=data.get("file_id"),
                                                   caption=f'{data.get("text")}',
                                                   reply_markup=murkup)
            except:
                usersdb.delete_user(i[0])

            protsent += 1
            protses = await protsent_rssilki(protsent=protsent,
                                             one_protsent=one_protsent,
                                             user_id=call.from_user.id,
                                             message_id=message_id.message_id)
            await asyncio.sleep(0.05)
    elif data.get("type") == "audio":
        for i in users:
            try:
                await bot.send_audio(i[0], audio=data.get("file_id"),
                                                caption=f'{data.get("text")}',
                                                reply_markup=murkup)
            except:
                usersdb.delete_user(i[0])

            protsent += 1
            protses = await protsent_rssilki(protsent=protsent,
                                             one_protsent=one_protsent,
                                             user_id=call.from_user.id,
                                             message_id=message_id.message_id)
            await asyncio.sleep(0.05)
    count_users = usersdb.select_all_users()
    await call.message.answer(f"👥Количество Пользователей после рассылки {len(count_users)}")
    await call.message.answer(f"Рассылка успешно выполнено")
    text = 'Выберите Действие 👇'
    await call.message.answer(text=text, reply_markup=admin_buttons)
    await state.finish()
