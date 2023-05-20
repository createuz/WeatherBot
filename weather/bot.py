import json
from datetime import datetime

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bs4 import BeautifulSoup as BS

time_now = datetime.now()
current_time = time_now.strftime("%H:%M:%S")

BOT_TOKEN = 'Bot Token'
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


# ' Hi 😉'
def read_file(file_name: str):
    with open(file_name, 'r') as regions_file:
        regions = json.load(regions_file)
    return regions


@dp.message_handler(commands='start')
async def start_hendler(message: types.Message):
    print('Usurname:', message.from_user.first_name, '{ Data:', current_time, '} Text:{',
          message.text, '}')
    await message.answer(f"\nAssalomu alaykum {message.from_user.first_name}\n"
                         f"Botimizga Xush Kelibsiz!")

    ikm = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    for i in ['Bugungi ob-havo', "Haftalik ob-havo ma'lumoti"]:
        ikm.insert(InlineKeyboardButton(i, callback_data=i))
    await message.answer("Qanday ob-havo ma'lumotini olishni istaysiz?", reply_markup=ikm)


@dp.callback_query_handler()
async def command_start_handler(call: CallbackQuery) -> None:
    if call.data == "Bugungi ob-havo":
        ikm = InlineKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        for rg in read_file('regions.json'):
            ikm.insert(InlineKeyboardButton(rg['name'], callback_data=f"region_day={rg['id']}"))
        await call.message.edit_text("Iltimos, shahringizni tanlang👇\n", reply_markup=ikm)

    elif call.data == "Haftalik ob-havo ma'lumoti":
        ikm = InlineKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        for rg in read_file('regions.json'):
            ikm.insert(InlineKeyboardButton(rg['name'], callback_data=f"region_week={rg['id']}"))
        await call.message.edit_text("Iltimos, shahringizni tanlang👇\n", reply_markup=ikm)

    if call.data.split('=')[0] == 'region_day':
        id = call.data.split('=')[1]
        for rg in read_file('regionnn.json'):
            for r in read_file('regions.json'):
                if id == rg['id']:
                    if id == r['id']:
                        # await call.message.edit_text(f"{r['name'].capitalize()} shahri tanlandi")

                        link = f"https://obhavo.uz/{rg['name']}"
                        res = requests.get(link).text
                        soup = BS(res, 'html.parser')

                        def today_func():
                            for el in soup.select('.padd-block'):
                                for le in el.select('.current-day'):
                                    return le.text

                        def today_weather():
                            st = ''
                            for el in soup.select('.current-forecast'):
                                st += el.text
                                return st.strip().replace('\n', '  ')

                        def qor():
                            for el in soup.select('.current-forecast-desc'):
                                if el.text == 'Ochiq havo':
                                    return '☀'.strip()
                                elif el.text == 'Bulutli':
                                    return '☁'.strip()
                                elif el.text == 'Qor':
                                    return '🌨'.strip()
                                else:
                                    return '🌧'.strip()

                        def weather_func():
                            for el in soup.select('.current-forecast-desc'):
                                return el.text

                        def wet_func():
                            for el in soup.select('.current-forecast-details'):
                                for le in el.select('.col-1'):
                                    return f"{le.text[:8]} {le.text[8:]}"

                        def moth_funcc():
                            for el in soup.select('.current-forecast-details'):
                                for le in el.select('.col-2'):
                                    if 'Oy: Qisqarayotgan oy' in le.text:
                                        return '🌘'.strip()
                                    elif "Oy: To'lin oy" in le.text:
                                        return '🌕'.strip()
                                    else:
                                        return '🌒'.strip()

                        def month_func():
                            for el in soup.select('.current-forecast-details'):
                                for le in el.select('.col-2'):
                                    return f"{le.text[:4]} {moth_funcc()}{le.text[4:39]} ☀ " \
                                           f"{le.text[40:60]} ☀ {le.text[61:]}"

                        def morning_func():
                            for el in soup.select('.col-1'):
                                for le in el.select('.time-of-day'):
                                    for l in el.select('.forecast'):
                                        if l.text[0][0] == '-':
                                            return f"{le.text}: {l.text}"
                                        elif l.text[0] == '0':
                                            return f"{le.text}: {l.text}"
                                        else:
                                            return f"{le.text}:  +{l.text}"

                        def day_func():
                            for el in soup.select('.col-2'):
                                for le in el.select('.time-of-day'):
                                    for l in el.select('.forecast'):
                                        if l.text[0][0] == '-':
                                            return f"{le.text}: {l.text}"
                                        elif l.text[0] == '0':
                                            return f"{le.text}: {l.text}"
                                        else:
                                            return f"{le.text}:  +{l.text}"

                        def evening_func():
                            for el in soup.select('.col-3'):
                                for le in el.select('.time-of-day'):
                                    for l in el.select('.forecast'):
                                        if l.text[0][0] == '-':
                                            return f"{le.text}: {l.text}"
                                        elif l.text[0] == '0':
                                            return f"{le.text}: {l.text}"
                                        else:
                                            return f"{le.text}:  +{l.text}"

                        ikm1 = InlineKeyboardMarkup().row(InlineKeyboardButton('⬅Back', callback_data='back1'))
                        await call.message.answer(
                            f"{r['name'].capitalize()}\n{today_func()}\n{qor()} {today_weather()},  {weather_func()}\n\n{morning_func()}\n{day_func()}\n{evening_func()}{wet_func()}"
                            f"{month_func()}",
                            reply_markup=ikm1)

    if call.data.split('=')[0] == 'region_week':
        id = call.data.split('=')[1]
        for rg in read_file('regionnn.json'):
            for r in read_file('regions.json'):
                if id == rg['id']:
                    if id == r['id']:
                        # await call.message.edit_text(f"{r['name'].capitalize()} shahri tanlandi")

                        link = f"https://obhavo.uz/{rg['name']}"
                        res = requests.get(link).text
                        soup = BS(res, 'html.parser')

                        def photo1():
                            s = soup.select('.weather-table .weather-row-desc')[1].text.strip()
                            if s == 'ochiq havo':
                                return '☀'.strip()
                            elif s == 'bulutli':
                                return '☁'.strip()
                            elif s == 'qor' or \
                                    s == "qor aralash yomg'ir":
                                return '🌨'.strip()
                            else:
                                return '🌧'.strip()

                        def photo2():
                            s = soup.select('.weather-table .weather-row-desc')[2].text.strip()
                            if s == 'ochiq havo':
                                return '☀'.strip()
                            elif s == 'bulutli':
                                return '☁'.strip()
                            elif s == 'qor' or \
                                    s == "qor aralash yomg'ir":
                                return '🌨'.strip()
                            else:
                                return '🌧'.strip()

                        def photo3():
                            s = soup.select('.weather-table .weather-row-desc')[3].text.strip()
                            if s == 'ochiq havo':
                                return '☀'.strip()
                            elif s == 'bulutli':
                                return '☁'.strip()
                            elif s == 'qor' or \
                                    s == "qor aralash yomg'ir":
                                return '🌨'.strip()
                            else:
                                return '🌧'.strip()

                        def photo4():
                            s = soup.select('.weather-table .weather-row-desc')[4].text.strip()
                            if s == 'ochiq havo':
                                return '☀'.strip()
                            elif s == 'bulutli':
                                return '☁'.strip()
                            elif s == 'qor' or \
                                    s == "qor aralash yomg'ir":
                                return '🌨'.strip()
                            else:
                                return '🌧'.strip()

                        def photo5():
                            s = soup.select('.weather-table .weather-row-desc')[5].text.strip()
                            if s == 'ochiq havo':
                                return '☀'.strip()
                            elif s == 'bulutli':
                                return '☁'.strip()
                            elif s == 'qor' or \
                                    s == "qor aralash yomg'ir":
                                return '🌨'.strip()
                            else:
                                return '🌧'.strip()

                        def photo6():
                            s = soup.select('.weather-table .weather-row-desc')[6].text.strip()
                            if s == 'ochiq havo':
                                return '☀'.strip()
                            elif s == 'bulutli':
                                return '☁'.strip()
                            elif s == 'qor' or \
                                    s == "qor aralash yomg'ir":
                                return '🌨'.strip()
                            else:
                                return '🌧'.strip()

                        def photo7():
                            s = soup.select('.weather-table .weather-row-desc')[7].text.strip()
                            if s == 'ochiq havo':
                                return '☀'.strip()
                            elif s == 'bulutli':
                                return '☁'.strip()
                            elif s == 'qor' or \
                                    s == "qor aralash yomg'ir":
                                return '🌨'.strip()
                            else:
                                return '🌧'.strip()

                        def photo8():
                            s = soup.select('.weather-table .weather-row-desc')[8].text.strip()
                            if s == 'ochiq havo':
                                return '☀'.strip()
                            elif s == 'bulutli':
                                return '☁'.strip()
                            elif s == 'qor' or \
                                    s == "qor aralash yomg'ir":
                                return '🌨'.strip()
                            else:
                                return '🌧'.strip()

                        def wet1():
                            return f"Yog‘ingarchilik ehtimoli: {soup.select('.weather-table .weather-row-pop')[1].text.strip()}"

                        def wet2():
                            return f"Yog‘ingarchilik ehtimoli: {soup.select('.weather-table .weather-row-pop')[2].text.strip()}"

                        def wet3():
                            return f"Yog‘ingarchilik ehtimoli: {soup.select('.weather-table .weather-row-pop')[3].text.strip()}"

                        def wet4():
                            return f"Yog‘ingarchilik ehtimoli: {soup.select('.weather-table .weather-row-pop')[4].text.strip()}"

                        def wet5():
                            return f"Yog‘ingarchilik ehtimoli: {soup.select('.weather-table .weather-row-pop')[5].text.strip()}"

                        def wet6():
                            return f"Yog‘ingarchilik ehtimoli: {soup.select('.weather-table .weather-row-pop')[6].text.strip()}"

                        def wet7():
                            return f"Yog‘ingarchilik ehtimoli: {soup.select('.weather-table .weather-row-pop')[7].text.strip()}"

                        def wet8():
                            return f"Yog‘ingarchilik ehtimoli: {soup.select('.weather-table .weather-row-pop')[8].text.strip()}"

                        def cloud1():
                            return soup.select('.weather-table .weather-row-desc')[1].text.strip()

                        def cloud2():
                            return soup.select('.weather-table .weather-row-desc')[2].text.strip()

                        def cloud3():
                            return soup.select('.weather-table .weather-row-desc')[3].text.strip()

                        def cloud4():
                            return soup.select('.weather-table .weather-row-desc')[4].text.strip()

                        def cloud5():
                            return soup.select('.weather-table .weather-row-desc')[5].text.strip()

                        def cloud6():
                            return soup.select('.weather-table .weather-row-desc')[6].text.strip()

                        def cloud7():
                            return soup.select('.weather-table .weather-row-desc')[7].text.strip()

                        def cloud8():
                            return soup.select('.weather-table .weather-row-desc')[8].text.strip()

                        def week1():
                            day = soup.select('.weather-table .weather-row-day ')[1].text.strip().replace('\n', ' ')
                            t = soup.select('.weather-table .weather-row-forecast')[0].text.replace('\n', ' ')
                            return f"{r['name'].capitalize()}\n{day}\n{photo1()}{t}{cloud1().capitalize()}\n{wet1()}"

                        def week2():
                            day = soup.select('.weather-table .weather-row-day ')[2].text.strip().replace('\n', ' ')
                            s = soup.select('.weather-table .weather-row-forecast')[1].text.replace('\n', ' ')
                            return f"{day}\n{photo2()}{s}{cloud2().capitalize()}\n{wet2()}"

                        def week3():
                            day = soup.select('.weather-table .weather-row-day ')[3].text.strip().replace('\n', ' ')
                            s = soup.select('.weather-table .weather-row-forecast')[2].text.replace('\n', ' ')
                            return f"{day}\n{photo3()}{s}{cloud3().capitalize()}\n{wet3()}"

                        def week4():
                            day = soup.select('.weather-table .weather-row-day ')[4].text.strip().replace('\n', ' ')
                            s = soup.select('.weather-table .weather-row-forecast')[3].text.replace('\n', ' ')
                            return f"{day}\n{photo4()}{s}{cloud4().capitalize()}\n{wet4()}"

                        def week5():
                            day = soup.select('.weather-table .weather-row-day ')[5].text.strip().replace('\n', ' ')
                            s = soup.select('.weather-table .weather-row-forecast')[4].text.replace('\n', ' ')
                            return f"{day}\n{photo5()}{s}{cloud5().capitalize()}\n{wet5()}"

                        def week6():
                            day = soup.select('.weather-table .weather-row-day ')[6].text.strip().replace('\n', ' ')
                            s = soup.select('.weather-table .weather-row-forecast')[5].text.replace('\n', ' ')
                            return f"{day}\n{photo6()}{s}{cloud6().capitalize()}\n{wet6()}"

                        def week7():
                            day = soup.select('.weather-table .weather-row-day ')[7].text.strip().replace('\n', ' ')
                            s = soup.select('.weather-table .weather-row-forecast')[6].text.replace('\n', ' ')
                            return f"{day}\n{photo7()}{s}{cloud7().capitalize()}\n{wet7()}"

                        def week8():
                            day = soup.select('.weather-table .weather-row-day ')[8].text.strip().replace('\n', ' ')
                            s = soup.select('.weather-table .weather-row-forecast')[7].text.replace('\n', ' ')
                            return f"{day}\n{photo8()}{s}{cloud8().capitalize()}\n{wet8()}"

                        ikm1 = InlineKeyboardMarkup().row(InlineKeyboardButton('⬅Back', callback_data='back1'))
                        await call.message.answer(
                            f"{week1()}\n\n{week2()}\n\n{week3()}\n\n{week4()}\n\n{week5()}\n\n{week6()}\n\n{week7()}\n\n{week8()}",
                            reply_markup=ikm1)

    if call.data == 'back1':
        ikm = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        for i in ['Bugungi ob-havo', "Haftalik ob-havo ma'lumoti"]:
            ikm.insert(InlineKeyboardButton(i, callback_data=i))
        await call.message.edit_text("Qanday ob-havo ma'lumotini olishni istaysiz?", reply_markup=ikm)
    else:
        return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
