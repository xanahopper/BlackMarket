from black_market.models.models import (Course, CourseSchedule)


def get_ids_set(courses):
    return set([course.id for course in courses])


def get_all_courses():
    return Course.query.all()


def get_course_by_id(id):
    return Course.query.get(id)


def get_course_ids_by_name(name):
    if not name:
        return set()
    return get_ids_set(
        Course.query.filter(Course.name.ilike('%' + name + '%')))


def get_course_ids_by_credit(credit):
    if not credit:
        return set()
    return get_ids_set(Course.query.filter_by(credit=credit))


def get_course_ids_by_days(days):
    course_ids = set()
    if not days:
        return course_ids
    for day in days:
        for schedule in CourseSchedule.query.filter_by(day=day):
            course_ids.add(schedule.course_id)
    return course_ids


def search_course_by_filters(name=None, days=None, credit=None):
    if not any([name, days, credit]):
        return
    days = days.split(',') if days else None
    ids_by_days = get_course_ids_by_days(days)
    ids_by_name = get_course_ids_by_name(name)
    ids_by_credit = get_course_ids_by_credit(credit)
    course_ids = ids_by_days.union(ids_by_name).union(ids_by_credit)
    if name:
        course_ids = course_ids.intersection(ids_by_name)
    if days:
        course_ids = course_ids.intersection(ids_by_days)
    if credit:
        course_ids = course_ids.intersection(ids_by_credit)
    return [get_course_by_id(id) for id in course_ids]
