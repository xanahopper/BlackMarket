# def get_ids_set(courses):
#     return set([course.id for course in courses])


# def get_course_ids_by_name(name):
#     if not name:
#         return set()
#     return get_ids_set(
#         Course.query.filter(Course.name.ilike('%' + name + '%')))
#
#
# def get_course_ids_by_teacher(teacher):
#     if not teacher:
#         return set()
#     return get_ids_set(
#         Course.query.filter(Course.teacher.ilike('%' + teacher + '%')))
#
#
# def get_course_ids_by_credit(credit):
#     if not credit:
#         return set()
#     return get_ids_set(Course.query.filter_by(credit=credit))
#
#
# def get_course_ids_by_days(days):
#     course_ids = set()
#     if not days:
#         return course_ids
#     for day in days:
#         for schedule in CourseSchedule.query.filter_by(day=day):
#             course_ids.add(schedule.course_id)
#     return course_ids
#
#
# def search_course(text):
#     if not text:
#         return
#     ids_by_name = get_course_ids_by_name(text)
#     ids_by_teacher = get_course_ids_by_teacher(text)
#     course_ids = ids_by_name.union(ids_by_teacher)
#     return [get_course_by_id(id) for id in course_ids]
