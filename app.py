from flask import Flask , request , jsonify

app = Flask(__name__)

# initialize list to hold students records as dictionary in format {"id": 101 , "name": "Jaspreet" } 
students_list = []

# initialize classes list to hold records as dictionary 
# in format {"id": 201 , "name": "CMPE273" , students : [{"id": 101 , "name": "Jaspreet" }] } 
classes_list = []

# starting student id from 100 and class id from 200
sid = 100
cid = 200

# function to retrieve student record with a given student id 
def get_student(student_id):
	students_result = []
	if len(students_list)==0:
		return "No Students in List, Please add Students"
	else:
		for index in students_list:
			if (index["id"]==student_id):
				students_result.append(index) 
	if(len(students_result)==0):
		return "No student found at id : %d" %student_id
	else:
		return students_result

# POST method implementation for creating new student record and storing it in students_list , with Student id auto incremented by 1
@app.route('/students',methods=['POST'])
def create_new_student():
	global sid
	student_name = request.get_json()
	new_student = { "id" : sid + 1 , "name" : student_name.get("name") }
	students_list.append(new_student)
	sid = sid + 1
	return jsonify(new_student) , 201
	
#@app.route('/students/')
#def showall_students():
#	return jsonify(students_list)

# GET method for displaying the student record at given student id
@app.route('/students/<int:student_id>', methods=['GET'])
def show_student(student_id):	
	return jsonify(get_student(student_id))

# POST method for adding new class record and storing it in the classes_list , with class id auto incremented by 1 
@app.route('/classes',methods=['POST'])
def create_new_class():
	global cid
	class_name = request.get_json()
	new_class = { "id" : cid + 1 , "name" : class_name.get("name") , "students" : [] }
	classes_list.append(new_class)
	cid = cid + 1 
	return jsonify(new_class)

#@app.route('/classes/',methods=['GET'])
#def showall_classes():
#	return jsonify(classes_list)

# GET method for displaying the class record at a given class id
# PATCH method to update the record and add the students with student_id in the class at a given class id 
@app.route('/classes/<int:class_id>',methods=['GET','PATCH'])
def get_update_classes(class_id):
	if request.method=='GET':
		search_result = []
		if len(classes_list)==0:
			return "No classes has been setup, Please add classes"
		else:
			for index in classes_list:
				if (index["id"]==class_id):
					search_result.append(index) 
		if len(search_result)==0:
			return "No class found at id : %d" %class_id
		else:
			return jsonify(search_result)
	elif request.method=='PATCH':
		for index in classes_list:
			if index["id"]==class_id:
				data = request.get_json()
				get_sid = data["student_id"]
				add_student = get_student(get_sid)
				index["students"].append(add_student)
				return jsonify(index)
	else:
		return "Nothing Found , Please Try Again"
