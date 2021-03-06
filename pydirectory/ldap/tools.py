class setQuery(object):
	specialFields = {}
	operators = {
		'default' : '({field}={value})',
		'conditions': {
			'gt' : '({field}>{value})',
			'ge' : '({field}>={value})',
			'lt' : '({field}<{value})',
			'le' : '({field}<={value})',
			'eq' : '({field}={value})',
		},
		'wrapper' : {
			'not' : '(!{query})'
		}
	}

	def __init__(self,*args,**kwargs):
		pass

	def __call__(self,oper='and',**fields):
		result = ''
		for field,value in list(fields.items()):
			if field in list(self.specialFields.keys()):
				if type(self.specialFields[field]) == dict:
					result += self.specialFields[field][value]
				else:
					if type(value) == list:
						for pos in value:
							result += self.specialFields[field].format(DN=pos)
					else:
						result += self.specialFields[field].format(DN=value)
				continue

			wrapper = False
			for wrap in list(self.operators['wrapper'].keys()):
				if field.find('__'+wrap) > -1:
					field = field.replace('__'+wrap,'')
					wrapper = self.operators['wrapper'][wrap]

			try:
				name,operator = field.split('__')
			except ValueError:
				name = field
				operator = None

			if type(value) == list:
				query = ''
				for val in value:
					aux = self.operators['conditions'].get(operator,self.operators['default']).format(field=name,value=val)
					if wrapper:
						aux = wrapper.format(query=aux)
					query += aux
			else:
				query = self.operators['conditions'].get(operator,self.operators['default']).format(field=name,value=value)
				if wrapper:
					query = wrapper.format(query=query)

			result += query

		if oper == 'and':
			return '(&{query})'.format(query=result)
		if oper == 'or'	:
			return '(|{query})'.format(query=result)
