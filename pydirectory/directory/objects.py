import directory.attributes

class Object(object):
	attributes = directory.attributes
	def __init__(self,engine,data):
		self._store = dict()
		self._engine = engine
		self._update(data)

	def _update(self,data):
		for attr,value in data.items():
			self[attr] = value

	def __setattr__(self,key,value):
		if key.find('_') == 0:
			super(Object,self).__setattr__(key,value)
		else:
			self.__setitem__(key,value)

	def __getattr__(self,key):
		if key.find('_') == 0:
			return super(Object,self).__getattribute__(key)
		return self._store[key]

	def __setitem__(self,key,value):
		self._store[key] = self.attributes.attribute(self._engine,value)

	def __dir__(self):
		return self._store.keys()

	def __getitem__(self,key):
		return self._store[key]

	def __delitem__(self,key):
		del self._store[key]

	def __len__(self):
		return len(self._store)

	def __iter__(self):
		return iter(self._store)

	def save(self):
		pass




class ObjectsList(list):
	def __init__(self,obj,engine,*args,**kwargs):
		self._object = obj
		self._engine = engine
		super(ObjectsList,self).__init__(*args,**kwargs)

	def append(self,data):
		obj = self._object(self._engine,data)
		super(ObjectsList,self).append(obj)



class Objects(object):

	class SEARCH(object):
		def __init__(self,engine):
			self._engine = engine

		def __call__(self,query):
			return self._get(query)

	class NEW(object):
		def __init__(self,engine):
			self._engine = engine

		def __call__(self,query):
			return self._get(query)

	def __init__(self,engine):
		self._engine = engine

	@property
	def search(self):
		return self._search(self._engine)

	@property
	def get(self):
		return self._get(self._engine)

	def new(self):
		return self._new(self._engine)
