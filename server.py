from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

import sqlite3
conn = sqlite3.connect("database2.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS students(
    student_id INT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    average_grade INT);
""")
conn.commit()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_message("Incoming GET request...")
        id_retrieve = parse_qs(self.path[2:])['id_retrieve'][0]
        char_remove = ["'", "[", "]"]
        for char in char_remove:
            id_retrieve = id_retrieve.replace(char,"")
        id_retrieve = int(id_retrieve)
        try:
            cursor.execute(f"SELECT * FROM students WHERE student_id = {id_retrieve};")
            all_results = cursor.fetchall()
            student = all_results[0]
            (student_id, first_name, last_name, grade) = student
            response_get = f"First Name: {first_name}<br> Last Name:{last_name}<br> Student ID: {student_id}<br> Average Grade: {grade}"
        except:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
            return
 
        if id_retrieve in student:
            self.send_response_to_client(200, response_get)
            
        else:
            self.send_response_to_client(400, 'Student not found')
            self.log_message("Student not found")
     
    def do_POST(self):
        self.log_message('Incoming POST request...')
        data = parse_qs(self.path[2:])
        first_name = str(data["first_name"])
        last_name = str(data["last_name"])
        student_id = str(data["student_id"])
        grade = str(data["grade"])
        char_remove = ["'", "[", "]"]
        
        for char in char_remove:
            first_name = first_name.replace(char,"")
            last_name = last_name.replace(char,"")
            student_id = student_id.replace(char,"")
            grade = grade.replace(char, "")
            
        grade = int(grade)
        student_id = int(student_id)
        students = (student_id, first_name, last_name, grade)
        
        try:
            cursor.execute("INSERT INTO students VALUES (?,?,?,?)", students)
            conn.commit()
            self.send_response_to_client(200, data)
            
        except KeyError:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
             
    def send_response_to_client(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(str(data).encode())
 
server_address = ('127.0.0.1', 8080)
http_server = HTTPServer(server_address, RequestHandler)
http_server.serve_forever()