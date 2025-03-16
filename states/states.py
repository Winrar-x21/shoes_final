from aiogram.fsm.state import State, StatesGroup

class SettingsStates(StatesGroup):
    choose_name = State()
    add_address_label = State()
    add_address_text = State()