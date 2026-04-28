import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8642842194:AAGSMdeosWyAmsvWh2Bo143wvYq3AdOLhXk'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

user_selections = {}

# ---------------------- МОДЕЛИ ----------------------
models = {
    'finist': {
        'name': 'ФИНИСТ',
        'base_price': 2_300_000,
        'desc': '⚙️ Технические характеристики\nМощность: 109 л.с.\nКатегория прав: А2\n\n📦 Базовая комплектация\nДвигатель Тойота 1NZ-FE, АКПП Тойота, отопитель салона Газель, передние раздвижные форточки, раздвижная форточка задней двери, автолин на полу, передние сиденья ВАЗ, шины МАРШЛЭНД 1300x600, обшивка композитным материалом, гидрообъёмное рулевое управление, дисковые тормоза, светотехника, рессорная подвеска.'
    },
    'profi': {
        'name': 'ФИНИСТ ПРО',
        'base_price': 2_695_000,
        'desc': '⚙️ Технические характеристики\nМощность: 109 л.с.\nКатегория прав: А2\n\n📦 Базовая комплектация\nДвигатель Тойота 1NZ-FE, АКПП Тойота, отопитель салона Газель, передние раздвижные форточки, раздвижная форточка задней двери, автолин на полу, передние сиденья ВАЗ, шины МАРШЛЭНД 1300x600, обшивка композитным материалом, гидрообъёмное рулевое управление, дисковые тормоза, светотехника, рессорная подвеска, раздатка ГАЗ 66, передняя пружинная подвеска.'
    },
    'pikap': {
        'name': 'ФИНИСТ Пикап',
        'base_price': 2_200_000,
        'desc': '⚙️ Технические характеристики\nМощность: 109 л.с.\nКатегория прав: А2\n\n📦 Базовая комплектация\nДвигатель Тойота 1NZ-FE, АКПП Тойота, отопитель салона Газель, передние раздвижные форточки, раздвижная форточка задней двери, автолин на полу, передние сиденья ВАЗ, шины МАРШЛЭНД 1300x600, обшивка композитным материалом, гидрообъёмное рулевое управление, дисковые тормоза, светотехника, рессорная подвеска.'
    }
}

# ---------------------- ОПЦИИ С КОРОТКИМИ ID ----------------------
options_data = {
    'electro': {
        'title': 'Электрооборудование',
        'items': [
            {'id': 1, 'name': 'Дизельный автономный отопитель', 'price': 35000},
            {'id': 2, 'name': 'Электро лебедка 6000 dbl 4000 кг', 'price': 54000},
            {'id': 3, 'name': 'Быстросъемный механизм для крепления лебедки спереди и сзади', 'price': 15000},
            {'id': 4, 'name': 'Задний диодный свет', 'price': 8000},
            {'id': 5, 'name': 'Светодиодная балка 240 W', 'price': 17000},
            {'id': 6, 'name': 'Внутрисалонное LED освещение', 'price': 10000},
            {'id': 7, 'name': 'Боковой диодный свет', 'price': 10000},
            {'id': 8, 'name': 'Камера заднего вида+монитор+ аудиоподготовка', 'price': 45000},
        ]
    },
    'body': {
        'title': 'Кузов',
        'items': [
            {'id': 9, 'name': 'Фаркоп (квадрат/шар)', 'price': 8000},
            {'id': 10, 'name': 'Расширители колесных арок ПНД', 'price': 15000},
            {'id': 11, 'name': 'Задние лавки со спинкой (2 шт.)', 'price': 20000},
            {'id': 12, 'name': 'Заднее спальное место (включая задние лавки)', 'price': 30000},
            {'id': 13, 'name': 'Отсекатель веток', 'price': 7000},
            {'id': 14, 'name': 'Дополнительная топливная канистра 15 л.', 'price': 10000},
            {'id': 15, 'name': 'Обработка днища антикором', 'price': 23000},
            {'id': 16, 'name': 'Подкачка шин выхлопными газами', 'price': 5000},
            {'id': 17, 'name': 'Усиленный задний бампер', 'price': 10000},
            {'id': 18, 'name': 'Откидные лобовые стекла Триплекс, 2 шт.', 'price': 53000},
            {'id': 19, 'name': 'Обшивка салона с утеплением', 'price': 197000},
            {'id': 20, 'name': 'Раздвижные форточки боковые в задней части кунга (2шт)', 'price': 30000},
            {'id': 21, 'name': 'Люк в крыше (1шт)', 'price': 27000},
            {'id': 22, 'name': 'Багажник экспедиционный', 'price': 30000},
            {'id': 23, 'name': 'Лестница экспедиционная', 'price': 10000},
        ]
    },
    'transmission': {
        'title': 'Трансмиссия',
        'items': [
            {'id': 24, 'name': 'Полуоси усиленные (4 шт.)', 'price': 55000},
            {'id': 25, 'name': 'Принудительная блокировка электрическая передней оси (1шт)', 'price': 50000},
            {'id': 26, 'name': 'Принудительная блокировка электрическая задней оси (1шт)', 'price': 50000},
        ]
    },
    'design': {
        'title': 'Оформление',
        'items': [
            {'id': 27, 'name': 'Электронный ПСМ', 'price': 100000},
        ]
    }
}

# Вспомогательные словари для быстрого доступа: id -> (cat_key, option_data)
option_by_id = {}
for cat_key, cat_data in options_data.items():
    for opt in cat_data['items']:
        option_by_id[opt['id']] = (cat_key, opt)

def format_price(price):
    return f"{price:,}".replace(",", " ")

def get_user_data(user_id):
    if user_id not in user_selections:
        user_selections[user_id] = {'model': None, 'selected_options': set()}  # set из id
    return user_selections[user_id]

def calculate_total(user_data):
    if not user_data['model']:
        return 0
    total = models[user_data['model']]['base_price']
    for opt_id in user_data['selected_options']:
        if opt_id in option_by_id:
            total += option_by_id[opt_id][1]['price']
    return total

def get_options_keyboard(user_id):
    user_data = get_user_data(user_id)
    keyboard = []
    for cat_key, cat_data in options_data.items():
        # считаем количество выбранных опций в этой категории
        selected_count = sum(1 for opt_id in user_data['selected_options'] if option_by_id[opt_id][0] == cat_key)
        button_text = f"{cat_data['title']} ({selected_count}/{len(cat_data['items'])})"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"cat_{cat_key}")])
    keyboard.append([InlineKeyboardButton("📋 Показать итоговую цену", callback_data="show_total")])
    keyboard.append([InlineKeyboardButton("🔄 Выбрать другую модель", callback_data="change_model")])
    return InlineKeyboardMarkup(keyboard)

def get_category_keyboard(cat_key, user_id):
    user_data = get_user_data(user_id)
    keyboard = []
    for opt in options_data[cat_key]['items']:
        is_selected = opt['id'] in user_data['selected_options']
        mark = "✅ " if is_selected else "❌ "
        button_text = f"{mark}{opt['name']} — {format_price(opt['price'])} ₽"
        callback = f"opt_{opt['id']}"   # короткий callback: opt_<id>
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback)])
    keyboard.append([InlineKeyboardButton("🔙 Назад к категориям", callback_data="back_to_categories")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_selections:
        del user_selections[user_id]
    keyboard = [
        [InlineKeyboardButton("🚙 Финист", callback_data="model_finist")],
        [InlineKeyboardButton("🏎️ Финист ПРО", callback_data="model_profi")],
        [InlineKeyboardButton("🛻 Финист Пикап", callback_data="model_pikap")]
    ]
    await update.message.reply_text(
        "Привет! Я конфигуратор вездеходов.\n\nВыберите модель:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    data = query.data

    # Выбор модели
    if data.startswith("model_"):
        model_key = data.split("_")[1]
        user_data = get_user_data(user_id)
        user_data['model'] = model_key
        user_data['selected_options'].clear()
        model = models[model_key]
        text = (
            f"🚗 {model['name']}\n\n"
            f"{model['desc']}\n\n"
            f"💰 Базовая цена: {format_price(model['base_price'])} руб.\n\n"
            "Теперь выберите дополнительные опции:"
        )
        await query.edit_message_text(
            text=text,
            reply_markup=get_options_keyboard(user_id)
        )
        return

    # Назад к категориям
    if data == "back_to_categories":
        await query.edit_message_reply_markup(reply_markup=get_options_keyboard(user_id))
        return

    # Показать итоговую цену
    if data == "show_total":
        user_data = get_user_data(user_id)
        if not user_data['model']:
            await query.edit_message_text("Сначала выберите модель через /start")
            return
        total = calculate_total(user_data)
        model = models[user_data['model']]
        base_price = model['base_price']
        selected_list = []
        for opt_id in user_data['selected_options']:
            if opt_id in option_by_id:
                opt = option_by_id[opt_id][1]
                selected_list.append(f"• {opt['name']} — {format_price(opt['price'])} ₽")
        addons_text = "\n".join(selected_list) if selected_list else "Нет доп. опций"
        text = (
            f"📊 Итоговая комплектация для {model['name']}:\n\n"
            f"🔹 Базовая цена: {format_price(base_price)} ₽\n"
            f"🔹 Доп. опции:\n{addons_text}\n\n"
            f"💰 Итого: {format_price(total)} ₽"
        )
        await query.message.reply_text(text)
        return

    # Смена модели
    if data == "change_model":
        if user_id in user_selections:
            del user_selections[user_id]
        keyboard = [
            [InlineKeyboardButton("🚙 Финист", callback_data="model_finist")],
            [InlineKeyboardButton("🏎️ Финист ПРО", callback_data="model_profi")],
            [InlineKeyboardButton("🛻 Финист Пикап", callback_data="model_pikap")]
        ]
        await query.edit_message_text(
            "Выберите новую модель:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Выбрана категория (cat_...)
    if data.startswith("cat_"):
        cat_key = data[4:]
        if cat_key in options_data:
            await query.edit_message_reply_markup(reply_markup=get_category_keyboard(cat_key, user_id))
        else:
            await query.edit_message_text("Ошибка: категория не найдена")
        return

    # Включение/выключение опции (opt_<id>)
    if data.startswith("opt_"):
        try:
            opt_id = int(data.split("_")[1])
            if opt_id in option_by_id:
                user_data = get_user_data(user_id)
                if opt_id in user_data['selected_options']:
                    user_data['selected_options'].remove(opt_id)
                else:
                    user_data['selected_options'].add(opt_id)
                # Определяем категорию, чтобы обновить именно её клавиатуру
                cat_key = option_by_id[opt_id][0]
                await query.edit_message_reply_markup(reply_markup=get_category_keyboard(cat_key, user_id))
            else:
                await query.edit_message_text("Ошибка: опция не найдена")
        except ValueError:
            await query.edit_message_text("Ошибка: неверный формат")
        return

    await query.edit_message_text("Неизвестная команда. Попробуйте /start")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
