from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
							InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from pymongo import MongoClient
import os
import random
import re
import time
import numexpr as ne
import math

bot = Bot(token="token")
dp = Dispatcher(bot, storage=MemoryStorage())

cluster = MongoClient("token")
collusers = cluster.users.users

class Math(StatesGroup):
	otvet = State()


def main():
	@dp.message_handler(commands="start")
	async def menu(message: types.Message):
		if collusers.count_documents({"_id": message.from_user.id}) != 1:
			collusers.insert_one(
					{
						"_id": message.from_user.id,
						"dones": 0,
						"fails": 0,
						"now": "0",
						"start": '0'
					}
				)
		keyboard = ReplyKeyboardMarkup(
			[
				[
					KeyboardButton("➕ Решить пример")
				],
				[
					KeyboardButton("🌀 Статистика"),
					KeyboardButton("🔙 Сбросить статистику")
				]
			],
			resize_keyboard=True
		)
		await message.answer("🍒 Меню", reply_markup=keyboard)

	@dp.message_handler(commands="delete")
	async def delete(message: types.Message):
		if collusers.count_documents({"_id": message.from_user.id}) != 1:
			collusers.insert_one(
					{
						"_id": message.from_user.id,
						"dones": 0,
						"fails": 0,
						"now": "0",
						"start": '0'
					}
				)
		collusers.update_one({"_id": message.from_user.id}, {"$set": {"dones": 0}})
		collusers.update_one({"_id": message.from_user.id}, {"$set": {"fails": 0}})
		await message.answer("Сбросил вам статистику!")
		await stat(message)

	@dp.message_handler(commands="primer")
	async def primer(message: types.Message):
		if collusers.count_documents({"_id": message.from_user.id}) != 1:
			collusers.insert_one(
					{
						"_id": message.from_user.id,
						"dones": 0,
						"fails": 0,
						"now": "0",
						"start": '0'
					}
				)
		if random.randint(1, 2) == 1:
			delenie = ['4 / 2', '6 / 2', '8 / 2', '10 / 2', '12 / 2', '14 / 2', '16 / 2', '18 / 2', '20 / 2', '6 / 3', '9 / 3', '12 / 3', '15 / 3', '18 / 3', '21 / 3', '24 / 3', '27 / 3', '30 / 3', '8 / 4', '12 / 4', '16 / 4', '20 / 4', '24 / 4', '28 / 4', '32 / 4', '36 / 4', '40 / 4', '10 / 5', '15 / 5', '20 / 5', '25 / 5', '30 / 5', '35 / 5', '40 / 5', '45 / 5', '50 / 5', '12 / 6', '18 / 6', '24 / 6', '30 / 6', '36 / 6', '42 / 6', '48 / 6', '54 / 6', '60 / 6', '14 / 7', '21 / 7', '28 / 7', '35 / 7', '42 / 7', '49 / 7', '56 / 7', '63 / 7', '63 / 7', '70 / 7', '16 / 8', '24 / 8', '32 / 8', '40 / 8', '48 / 8', '56 / 8', '64 / 8', '72 / 8', '80 / 8', '18 / 9', '27 / 9', '36 / 9', '45 / 9', '54 / 9', '63 / 9', '72 / 9', '81 / 9', '90 / 9', '20 / 10', '30 / 10', '40 / 10', '50 / 10', '60 / 10', '70 / 10', '80 / 10', '90 / 10', '100 / 10']
			prim = random.choice(delenie)
			collusers.update_one({"_id": message.from_user.id}, {"$set": {"now": prim}})
			keyboard = ReplyKeyboardMarkup([[KeyboardButton("✋ Exit")]], resize_keyboard=True, one_time_keyboard=True)
			await message.answer(f"Реши этот пример:\n{prim}", reply_markup=keyboard)
			start = message.date
			collusers.update_one({"_id": message.from_user.id}, {"$set": {"start": start}})
			await Math.otvet.set()
		else:
			a = random.randint(2, 9)
			b = random.randint(2, 9)
			prim = f'{a} * {b}'
			collusers.update_one({"_id": message.from_user.id}, {"$set": {"now": prim}})
			keyboard = ReplyKeyboardMarkup([[KeyboardButton("✋ Exit")]], resize_keyboard=True, one_time_keyboard=True)
			await message.answer(f"Реши этот пример:\n{prim}", reply_markup=keyboard)
			start = message.date
			collusers.update_one({"_id": message.from_user.id}, {"$set": {"start": start}})
			await Math.otvet.set()


	@dp.message_handler(commands="state")
	async def stat(message: types.Message):
		if collusers.count_documents({"_id": message.from_user.id}) != 1:
			collusers.insert_one(
					{
						"_id": message.from_user.id,
						"dones": 0,
						"fails": 0,
						"now": "0",
						"start": '0'
					}
				)
		dones =	collusers.find_one({"_id": message.from_user.id})['dones']
		fails = collusers.find_one({"_id": message.from_user.id})['fails']
		vse = dones + fails
		markdown = """
		*bold text*
		_italic text_
		[text](URL)
		"""
		await message.answer(f"Имя: *{message.from_user.first_name}* \nВсего: *{vse}*\nПравильных: *{dones}*\nНеправильных: *{fails}*", parse_mode= "Markdown")


	@dp.message_handler(state=Math.otvet)
	async def process_math_otvet(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			if message.text == "✋ Exit":
				collusers.update_one({"_id": message.from_user.id}, {"$inc": {"fails": 1}})
				await message.answer("Ок, я засчитаю этот ответ как неправильный!")
				await menu(message)
				await state.finish()
			else:
				data['otvet'] = message.text
				now = collusers.find_one({"_id": message.from_user.id})['now']
				start = collusers.find_one({"_id": message.from_user.id})['start']
				stop = message.date
				time = (stop - start).total_seconds()
				otvet = ne.evaluate(now)
				markdown = """
				*bold text*
				_italic text_
				[text](URL)
				"""
				try:
					otvet = math.floor(otvet)
					if time >= 10:
						if int(data['otvet']) == otvet:
							collusers.update_one({"_id": message.from_user.id}, {"$inc": {"fails": 1}})
							await message.answer(f"Это правильный ответ, но ты не успел за 10 секунд! Я засчитаю это в статистику, как неправильный ответ.")
							await menu(message)
							await state.finish()
						else:
							collusers.update_one({"_id": message.from_user.id}, {"$inc": {"fails": 1}})
							await message.answer(f"Это неправильный ответ и ты не упел за 10 секунд!\nПравильный ответ: *{otvet}*", parse_mode= "Markdown")
							await menu(message)
							await state.finish()
					elif int(data['otvet']) == otvet:
						collusers.update_one({"_id": message.from_user.id}, {"$inc": {"dones": 1}})
						await message.answer(f"Это правильный ответ!")
						await menu(message)
						await state.finish()
					else:
						collusers.update_one({"_id": message.from_user.id}, {"$inc": {"fails": 1}})
						await message.answer(f"Это неправильный ответ!\nПравильный ответ: *{otvet}*", parse_mode= "Markdown")
						await menu(message)
						await state.finish()
				except ValueError:
					await message.answer(f"Это не число, попробуй сделать новый пример.\nНа этот пример был ответ: *{otvet}*", parse_mode= "Markdown")
					await menu(message)
					await state.finish()

	@dp.message_handler(content_types=["text"])
	async def some_text(message: types.Message):
		if message.text == "🍒 Меню":
			await menu(message)
		elif message.text == "➕ Решить пример":
			await primer(message)
		elif message.text == "🌀 Статистика":
			await stat(message)
		elif message.text == "🔙 Сбросить статистику":
			await delete(message)
		else:
			await message.answer("Я не знаю такую команду")
			await menu(message)


if __name__ == '__main__':
	main()
	executor.start_polling(dp)
