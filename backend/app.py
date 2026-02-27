from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    try:
        students = db.get_all_students()
        return jsonify(students)
    except Exception:
        return jsonify({"error": "Failed to fetch students"}), 404



@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    try:
        student_data = request.json

        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark")

        if not name or not course or mark is None: # should be handled by frontend validation, but just in case :P
            return jsonify({"error": "Missing required fields"}), 404

        db.insert_student(name, course, mark)
        return jsonify(student_data), 200
    except Exception:
        return jsonify({"error": "Invalid request body"}), 404



@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    try:
        existing = db.get_student_by_id(student_id)
        if not existing:
            return jsonify({"error": "Student not found"}), 404
        student_data = request.json

        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark")

        if not name or not course or mark is None: # should be handled by frontend validation, but just in case :P
            return jsonify({"error": "Missing required fields"}), 404

        db.update_student(student_id, name, course, mark)
        return jsonify(student_data), 200
    except Exception:
        return jsonify({"error": "Invalid request body"}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    """
    try:
        existing = db.get_student_by_id(student_id)
        if not existing:
            return jsonify({"error": "Student not found"}), 404

        db.delete_student(student_id)
        return jsonify({"status": "deleted"}), 200
    except Exception:
        return jsonify({"error": "Failed to delete student"}), 404

@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        marks = [s["mark"] for s in students if s.get("mark") is not None]

        if len(marks) == 0:
            return jsonify({
                "count": 0,
                "average": None,
                "min": None,
                "max": None
            }), 200

        count = len(marks)
        average = sum(marks) / count
        minimum = min(marks)
        maximum = max(marks)

        return jsonify({
            "count": count,
            "average": average,
            "min": minimum,
            "max": maximum
        }), 200
    except Exception:
        return jsonify({"error": "Failed to compute stats"}), 404


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
