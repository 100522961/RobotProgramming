import random


def create_matrix():
    matrix = []
    for _ in range(10):
        good_student = random.choice([True, False])
        low_mark, high_mark = (75, 100) if good_student else (0, 60)
        matrix.append([random.randint(low_mark, high_mark) for _ in range(4)])
    return matrix


def averages(matrix):
    return [[sum(student_marks) / len(student_marks)] for student_marks in matrix]


marks = create_matrix()
student_averages = averages(marks)

print("Marks:")
for student_marks in marks:
    print(student_marks)

print("Averages:")
for student_average in student_averages:
    print(student_average)