import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request



@app.route('/add', methods=['POST'])
def add_user():
        try:
                _json = request.json
                _name = _json['name']
                _height = _json['height']
                _mass = _json['mass']
                _gender = _json['gender']
                _birth = _json['birth']
                
                
                if _name and _height and request.method == 'POST':

                        sql = "INSERT INTO characters (character_name, character_height, character_mass, character_gender, character_birth_year) VALUES (%s, %s, %s, %s, %s)"
                        data = (_name, _height, _mass, _gender, _birth)
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sql, data)
                        conn.commit()
                        resp = jsonify('character add successfully!')
                        resp.status_code = 200
                        return resp
                else:
                        return not_found()
        except Exception as e:
                print(e)
        finally:
                cursor.close()
                conn.close()

@app.route('/favorites')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM characters")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		



		
@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM characters WHERE character_id=%s", (id,))
		conn.commit()
		resp = jsonify('character deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
		
if __name__ == "__main__":
    app.run()