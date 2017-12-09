from flask_restful import  Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
class Book(Resource):
	TABLE_NAME = 'books'
	parser = reqparse.RequestParser()
	parser.add_argument('author',
		type = str,
		required = True,
		help="This field cannot be left blank."
	)
	parser.add_argument('status',
		type = str,
		required = True,
		help="This field cannot be left blank."
	)
	@jwt_required
	def get(self, name):
		book = self.find_by_name(name)
		if book:
			return book
		return {"Message":"Book not found"},404

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close()
		if row:
			return {'item': {'name': row[0], 'author': row[1], 'status': row[2]}}

	def post(self, name):
		if self.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}
		data = Book.parser.parse_args()
		book = {'name':name, 'author':data['author'], 'status':data['status']}
		try:
			Book.insert(book)
		except:
			return {"message": "An error occurred inserting the book."}
		return book

	@classmethod
	def insert(cls, book):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "INSERT INTO {table} VALUES(?, ?, ?)".format(table=cls.TABLE_NAME)
		cursor.execute(query, (book['name'],book['author'],book['status']))
		connection.commit()
		connection.close()

class BookList(Resource):
	TABLE_NAME = 'books'
	def get(self):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
		result = cursor.execute(query)
		books = []
		for row in result:
			books.append({'name':row[0],'author':row[1],'status':row[2]})
		connection.close()
		return {"Books":books}