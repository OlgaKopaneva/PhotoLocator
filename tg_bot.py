import logging
from aiogram import Bot, Dispatcher, executor, types
from prediction import predict
from async_gpt import get_chatbase_response


API_TOKEN = '6543532275:AAEKp9XiDOVHq1_dawaQF6PuPLYcGeIFe84' # Чтение токена из переменных окружения

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('''Привет! Отправь мне достопримечательность и я расскажу немного о ней. О какой достопримечательности ты бы хотел узнать?''')

# Обработка отправленных изображений
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    try:
        # Загрузка изображения
        await message.photo[-1].download('user_image.jpg')

        # Предсказание класса изображения
        predicted_class = predict('user_image.jpg')  # Убедитесь, что функция predict асинхронная

        # Формирование запроса к GPT
        prompt =f'''Ты гид по колледжам в Оксфорде,
         подробно рассказывающий о их истории и культуре, 
         делая это увлекательно и информативно. 
         Подробно расскажи о месте под названием {predicted_class}.
         Обязательно на русском'''

        # Получение ответа от GPT
        response = await get_chatbase_response(prompt)  # Убедитесь, что функция ask_gpt асинхронная

        # Отправка ответа пользователю
        await message.reply(response)
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        await message.reply("Извините, произошла ошибка.")

if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
