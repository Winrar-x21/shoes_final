from aiogram.fsm.state import State, StatesGroup

class SettingStates(StatesGroup):
    chose_name = State()
    add_adress = State()
    