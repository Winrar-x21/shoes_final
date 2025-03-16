import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import dotenv_values
from users.users import read_user_config, write_user_config, update_user_config, user_exists
from keyboards.keyboards import start_keyboard, settings_keyboard, addresses_keyboard, back_to_menu_keyboard, catalogue_keyboard
from states.states import SettingsStates
from users.address import Address
from wares.wares import wares, Ware


config = dotenv_values()
bot = Bot(token=config["BOT_TOKEN"])
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(message: Message):
    user = message.from_user
    user_id = user.id

    if user_exists(user_id=user_id):
        user_config = read_user_config(user_id=user_id)
    else:
        user_config = {
            "first_name": user.first_name,
            "addresses": [],
            "cashback_points": 0,
        }

        write_user_config(user_id=user_id, config=user_config)


    await message.answer(text=f'Добро пожаловать в магазин обуви "Кефтеме", {user_config["first_name"]}!',
                        reply_markup=start_keyboard())


@dp.callback_query(F.data == 'settings')
async def settings_menu(callback: CallbackQuery):
    await callback.message.edit_text('Настройки аккаунта',
                                     reply_markup=settings_keyboard())


@dp.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    user_id = callback.message.chat.id
    user = read_user_config(user_id=user_id)

    await callback.message.edit_text(text=f'Добро пожаловать в магазин обуви "Кефтеме", {user["first_name"]}!',
                        reply_markup=start_keyboard())


@dp.callback_query(F.data == 'name_change')
async def name_change(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введите своё новое имя:")

    await state.set_state(SettingsStates.choose_name)


@dp.message(F.text, SettingsStates.choose_name)
async def new_name(message: Message, state: FSMContext):
    new_name = message.text
    user_id = message.from_user.id

    changes = {
        'first_name': new_name
    }

    update_user_config(user_id=user_id, keys_to_update=changes)

    await message.answer(text=f'{new_name}, Ваше имя успешно изменено', 
                         reply_markup=back_to_menu_keyboard())
    await state.set_state(None)


@dp.callback_query(F.data=="addresses_settings")
async def addresses_settings(callback: CallbackQuery, state: FSMContext):
    user_id = callback.message.chat.id
    config = read_user_config(user_id=user_id)
    
    if len(config['addresses']) == 0:
        await callback.message.edit_text('У Вас не указан ни один адрес доставки.\nДобавьте адреса ниже.',
                                         reply_markup=addresses_keyboard())


@dp.callback_query(F.data=='add_address')
async def add_addresses(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите название нового адреса')

    await state.set_state(SettingsStates.add_address_label)


@dp.message(F.text, SettingsStates.add_address_label)
async def add_address_label(message: Message, state: FSMContext):
    address_label = message.text

    await message.answer(f'Укажите адрес для {address_label}')
    await state.set_state(SettingsStates.add_address_text)
    await state.set_data({"label": address_label})


@dp.message(F.text, SettingsStates.add_address_text)
async def add_address_text(message: Message, state: FSMContext):
    address = message.text
    
    data = await state.get_data()
    address_label = data['label']

    user_id = message.from_user.id
    config = read_user_config(user_id=user_id)

    new_address = Address.from_dict(
        {
            "label": address_label,
            "address": address
        }
    )

    config['addresses'].append(new_address.to_dict())
    keys_to_update = {
        'addresses': config['addresses']
    }
    update_user_config(user_id=user_id, keys_to_update=keys_to_update)


@dp.callback_query(F.data=='catalogue')
async def catalogue(callback: CallbackQuery, state: FSMContext):
    user_id = callback.message.chat.id
    user = read_user_config(user_id=user_id)
    name = user['first_name']
    await callback.message.edit_text(f'{name}, выберите заинтересовавший Вас товар из каталога ниже:',
                                    reply_markup=catalogue_keyboard(wares))
    

@dp.callback_query(F.data=='back_to_catalogue')
async def back_to_catalogue(callback: CallbackQuery, state: FSMContext):
    user_id = callback.message.chat.id
    user = read_user_config(user_id=user_id)
    name = user['first_name']
    await callback.message.edit_text(f'{name}, выберите заинтересовавший Вас товар из каталога ниже:',
                                    reply_markup=catalogue_keyboard(wares))


@dp.callback_query(F.data.startswith('ware_'))
async def ware_info(callback: CallbackQuery):
    ware_id = int(callback.data.split('_')[-1])
    ware = Ware.get_ware_by_id(wares, ware_id)

    
    
    
    await callback.message.edit_text(ware.get_ware_details(),
                                     reply_markup=item_keyboard())
    
    await callback.message.edit_text(media=ware.inputImage)


async def main():
    print('Я запущен!')
    await dp.start_polling(bot)
    


asyncio.run(main())