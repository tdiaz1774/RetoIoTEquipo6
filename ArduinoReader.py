
import serial
import db_connector as db

def readHRData(number):
	"""Read the data Heart Rate data sent from our arduino, and insert it into our data base.
	readHRData(number: int)
	"""
	try:

		ser = serial.Serial('COM3',9600, timeout = 2)

		while True:

			data = (int(ser.readline().decode("utf-8")))

			if data:
				print(data)
				if db.checkDataBase():
					db.insertHR(number, data)
				else:
					db.createDataBase()
					db.insertHR(number, data)
			else:
				break

	except Exception as e:
		print(f"Occurrio un error! \n{e}")

readHRData("1")	