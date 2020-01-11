

class Task:
	def __init__(self,name,payload):
		self._name =  name
		self._payload = payload

	def get_name(self):
		return self._name

	def get_payload(self):
		return self._payload
		