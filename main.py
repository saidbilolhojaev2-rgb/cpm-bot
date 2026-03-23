import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# --- МАЪЛУМОТИ АСОСӢ ---
API_TOKEN = '8594148352:AAHv0t9qBb06cgEJQhGmPP-U_i5bJzY1RVw'
ADMINS = [7357553081, 6452145821] 
CHANNELS = ["@saidbilol65", "@muhamadali65", -1002347963236] 

# ТАРЗИ НАВИШТИ КАРТАИ ТУ
PAYMENT_TEXT = (
    "💳 **БАРОИ ПАРДОХТ:**\n\n"
    "🏦 **Душанбе Сити**\n"
    "🔹 По номеру карты: `9762000169743753`\n"
    "🔹 По номеру телефона: `104143449`\n"
    "👤 Ном: **Фарида Ш.**\n\n"
    "⚠️ Пулро гузаронед ва расми чекро (screenshot) дар инҷо фиристед!"
)

LANG_TEXTS = {
    'tj': {
        'main_menu': "Менюи асосӣ:",
        'order_btn': "🛒 Заказ кардан",
        'wait_admin': "✅ Чек ба админҳо рафт. Интизор шавед.",
        'get_creds': "✅ Чек қабул шуд!\nЛутфан Gmail ва Пароли худро фиристед:",
        'admin_acc_wait': "✅ Чек қабул шуд! Админ ҳозир акаунтро мефиристад.",
        'btn_king': "👑 Кинг", 'btn_hp': "🚀 HP ва Чит", 'btn_cars': "💲 Мошинҳои Premium",
        'btn_danat': "💰 Данат", 'btn_accs': "👤 Аккаунтҳои Full", 'btn_other': "🛠 Хизматрасониҳо",
        'btn_check': "✅ Санҷиши Чек", 'btn_support': "📞 Тамос бо Админ"
    },
    'ru': {
        'main_menu': "Главное меню:",
        'order_btn': "🛒 Заказать",
        'wait_admin': "✅ Чек отправлен админам. Ожидайте.",
        'get_creds': "✅ Чек принят!\nОтправьте ваш Gmail и Пароль:",
        'admin_acc_wait': "✅ Чек принят! Админ сейчас отправит аккаунт.",
        'btn_king': "👑 Кинг", 'btn_hp': "🚀 HP и Чит", 'btn_cars': "💲 Premium Машины",
        'btn_danat': "💰 Донат", 'btn_accs': "👤 Full Аккаунты", 'btn_other': "🛠 Услуги",
        'btn_check': "✅ Проверка Чека", 'btn_support': "📞 Связь с Админом"
    },
    'uz': {
        'main_menu': "Asosiy menyu:",
        'order_btn': "🛒 Buyurtma berish",
        'wait_admin': "✅ Chek adminlarga yuborildi. Kuting.",
        'get_creds': "✅ Chek qabul qilindi!\nGmail va Parolingizni yuboring:",
        'admin_acc_wait': "✅ Chek qabul qilindi! Admin hozir akkauntni yuboradi.",
        'btn_king': "👑 King", 'btn_hp': "🚀 HP va Chit", 'btn_cars': "💲 Premium Mashinalar",
        'btn_danat': "💰 Donat", 'btn_accs': "👤 Full Akkauntlar", 'btn_other': "🛠 Xizmatlar",
        'btn_check': "✅ Chekni tekshirish", 'btn_support': "📞 Admin bilan aloqa"
    }
}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class OrderProcess(StatesGroup):
    lang = State()
    current_order = State()
    waiting_admin_data = State()

def get_main_kb(lang):
    t = LANG_TEXTS[lang]
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=t['btn_king']), KeyboardButton(text=t['btn_hp'])],
        [KeyboardButton(text=t['btn_cars']), KeyboardButton(text=t['btn_danat'])],
        [KeyboardButton(text=t['btn_accs']), KeyboardButton(text=t['btn_other'])],
        [KeyboardButton(text=t['btn_check']), KeyboardButton(text=t['btn_support'])]
    ], resize_keyboard=True)

async def check_sub(user_id):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status not in ['left', 'kicked']: return True
        except: continue 
    return False

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🇹🇯 Тоҷикӣ", callback_data="set_tj"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_ru"),
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_uz"))
    await message.answer("Забонро интихоб кунед / Выберите язык / Tilni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("set_"))
async def set_language(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    await state.update_data(lang=lang)
    if await check_sub(call.from_user.id):
        await call.message.answer(LANG_TEXTS[lang]['main_menu'], reply_markup=get_main_kb(lang))
    else:
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Channel", url="https://t.me/saidbilol65"),
                    InlineKeyboardButton(text="Group", url="https://t.me/+D9gjSMNakCA4OTgy"))
        builder.row(InlineKeyboardButton(text="✅ Обуна шудам", callback_data="recheck"))
        await call.message.answer("Subscribe first!", reply_markup=builder.as_markup())
    await call.answer()

# --- ТУГМАҲОИ ХИЗМАТРАСОНИҲОИ НАВ 🛠 ---
@dp.message(F.text.in_([LANG_TEXTS[l]['btn_other'] for l in LANG_TEXTS]))
async def other_services(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'tj')
    builder = InlineKeyboardBuilder()
    services = [
        ("Матор W16", "10с"),
        ("Пароли акаунтро алиш кардан", "20с"),
        ("Политсейский (1 мошин)", "15с"),
        ("Сигнал (1 мошин)", "10с"),
        ("Бампер пеш", "10с"),
        ("Бампер қафо", "7с"),
        ("Ранги дуд (1 мошин)", "10с")
    ]
    for n, p in services:
        builder.row(InlineKeyboardButton(text=f"{n} - {p}", callback_data=f"buy_{n.replace(' ','_')}_{p}"))
    await message.answer("🛠 Хизматрасониҳои иловагӣ:", reply_markup=builder.as_markup())

# --- ТУГМАҲОИ ДИГАР (ҲАМА ДАР ҶОЯШ) ---
@dp.message(F.text.in_([LANG_TEXTS[l]['btn_king'] for l in LANG_TEXTS]))
async def menu_king(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'tj')
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f"{LANG_TEXTS[lang]['order_btn']} (15с)", callback_data="buy_King_15c"))
    await message.answer("👑 King Status - 15c", reply_markup=builder.as_markup())

@dp.message(F.text.in_([LANG_TEXTS[l]['btn_hp'] for l in LANG_TEXTS]))
async def menu_hp(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'tj')
    builder = InlineKeyboardBuilder()
    for n, p in [("300hp", "10с"), ("414hp", "10с"), ("650hp", "7с"), ("800hp", "5с"), ("1150чит", "10с")]:
        builder.row(InlineKeyboardButton(text=f"{n} - {p}", callback_data=f"buy_{n}_{p}"))
    await message.answer(LANG_TEXTS[lang]['btn_hp'], reply_markup=builder.as_markup())

@dp.message(F.text.in_([LANG_TEXTS[l]['btn_danat'] for l in LANG_TEXTS]))
async def menu_danat(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'tj')
    builder = InlineKeyboardBuilder()
    items = [("10M Cash", "10с"), ("30M Cash", "13с"), ("50M FULL", "15с"), ("100k Coins", "10с"), ("500k Coins", "25с")]
    for n, p in items:
        builder.row(InlineKeyboardButton(text=f"{n} - {p}", callback_data=f"buy_{n.replace(' ','_')}_{p}"))
    await message.answer(LANG_TEXTS[lang]['btn_danat'], reply_markup=builder.as_markup())

@dp.message(F.text.in_([LANG_TEXTS[l]['btn_cars'] for l in LANG_TEXTS]))
async def menu_cars(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'tj')
    builder = InlineKeyboardBuilder()
    cars = [("BMW M5 F90", "10с"), ("BMW M8", "10с"), ("Formula 1", "15с"), ("Mers Banan", "20с"), ("Mers Maybach", "10с")]
    for n, p in cars:
        builder.row(InlineKeyboardButton(text=f"{n} - {p}", callback_data=f"buy_{n.replace(' ','_')}_{p}"))
    await message.answer(LANG_TEXTS[lang]['btn_cars'], reply_markup=builder.as_markup())

@dp.message(F.text.in_([LANG_TEXTS[l]['btn_accs'] for l in LANG_TEXTS]))
async def menu_accs(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'tj')
    builder = InlineKeyboardBuilder()
    for p in ["25с", "35с", "50с", "80с"]:
        builder.row(InlineKeyboardButton(text=f"Acc {p}", callback_data=f"buy_Acc_{p}"))
    await message.answer(LANG_TEXTS[lang]['btn_accs'], reply_markup=builder.as_markup())

@dp.message(F.text.in_([LANG_TEXTS[l]['btn_support'] for l in LANG_TEXTS]))
async def support_msg(message: types.Message):
    await message.answer("🤝 Барои тамос: @Khojaev_l ё @Halimov_l")

# --- ЛОГИКАИ ЧЕК ВА АДМИН ---
@dp.callback_query(F.data.startswith("buy_"))
async def handle_buy(call: types.CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'tj')
    order = call.data.replace("buy_", "").replace("_", " ")
    await state.update_data(current_order=order)
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=LANG_TEXTS[lang]['order_btn'], callback_data="pay_now"))
    await call.message.answer(f"🛒 **Заказ:** {order}", reply_markup=builder.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data == "pay_now")
async def pay_now(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(PAYMENT_TEXT, parse_mode="Markdown")

@dp.message(F.photo)
async def handle_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang, order = data.get('lang', 'tj'), data.get("current_order", "Service")
    is_acc = "Acc" in order
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Туғри", callback_data=f"adm_ok_{message.from_user.id}_{lang}_{'ACC' if is_acc else 'SRV'}"))
    builder.row(InlineKeyboardButton(text="❌ Хато", callback_data=f"adm_no_{message.from_user.id}_{lang}"))
    for admin_id in ADMINS:
        try:
            await bot.send_photo(admin_id, message.photo[-1].file_id, 
                                 caption=f"💰 ЧЕК ОМАД!\n🛒: {order}\nID: {message.from_user.id}\nLang: {lang}", 
                                 reply_markup=builder.as_markup())
        except: continue
    await message.answer(LANG_TEXTS[lang]['wait_admin'])

@dp.callback_query(F.data.startswith("adm_ok_"))
async def admin_ok(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMINS: return
    _, _, uid, u_lang, o_type = call.data.split("_")
    uid = int(uid)
    if o_type == "ACC":
        await state.update_data(target_user=uid, target_lang=u_lang)
        await state.set_state(OrderProcess.waiting_admin_data)
        await bot.send_message(call.from_user.id, "Акаунтро фиристед:")
        await bot.send_message(uid, LANG_TEXTS[u_lang]['admin_acc_wait'])
    else:
        await bot.send_message(uid, LANG_TEXTS[u_lang]['get_creds'], parse_mode="Markdown")
        await bot.send_message(call.from_user.id, f"✅ OK фиристода шуд ({u_lang})")
    await call.answer()

@dp.message(OrderProcess.waiting_admin_data)
async def admin_send_final(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMINS: return
    data = await state.get_data()
    uid = data.get('target_user')
    await bot.send_message(uid, f"🎁 **Аккаунти шумо:**\n\n{message.text}")
    await message.answer("✅ Ба мизоҷ фиристода шуд!")
    await state.clear()

@dp.message(lambda m: "@" in m.text and "gmail" in m.text.lower())
async def gmail_client(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'tj')
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⏳ 10 мин", callback_data=f"st_10_{message.from_user.id}_{lang}"),
                InlineKeyboardButton(text="✅ Буд шуд", callback_data=f"st_dn_{message.from_user.id}_{lang}"))
    for admin_id in ADMINS:
        try:
            await bot.send_message(admin_id, f"📩 Gmail: `{message.text}`\n👤: {message.from_user.full_name}", 
                                   reply_markup=builder.as_markup(), parse_mode="Markdown")
        except: continue
    await message.answer("Маълумот ба админҳо рафт.")

@dp.callback_query(F.data.startswith("st_"))
async def final_status(call: types.CallbackQuery):
    if call.from_user.id not in ADMINS: return
    _, s, uid, lang = call.data.split("_")
    msg = "⏳ 10 дақиқа пас тайёр мешавад!" if s == "10" else "✅ Табрик! Кор буд шуд. Дароед бинед! 👑"
    if lang == 'ru': msg = "⏳ Будет готово через 10 минут!" if s == "10" else "✅ Поздравляем! Работа выполнена! 👑"
    if lang == 'uz': msg = "⏳ 10 daqiqadan so'ng tayyor bo'ladi!" if s == "10" else "✅ Tabriklaymiz! Ish bajarildi! 👑"
    await bot.send_message(int(uid), msg)
    await call.answer()

async def main(): await dp.start_polling(bot)
if __name__ == '__main__': asyncio.run(main())
