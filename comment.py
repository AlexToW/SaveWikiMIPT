from enum import Enum

class CommentType(Enum):
    FACULTY = 1,
    DEPARTMENT = 2,
    SUBJECT = 3,
    TEACHER = 4,
    BOOK = 5,
    FOLKLORE = 6,
    ORGANIZATION = 7,
    MEMO = 8,
    GUIDE = 9

class Comment:
    type: CommentType
    author: str
    date: str
    time: str
    score: str
    text: str
    hidden: bool
    reply: bool

    def __init__(self, type: CommentType, author: str, date: str, time: str, score: str, text: str, hidden: bool, reply: bool) -> None:
        self.type = type
        self.author = author
        self.date = date
        self.time = time
        self.score = score
        self.text = text
        self.hidden = hidden
        self.reply = reply


class FacultyComment(Comment):
    faculty_name: str


class DepartmentComment(Comment):
    department_name: str


class SubjectComment(Comment):
    subject_name: str


class TeacherComment(Comment):
    teacher_name: str


class BookComment(Comment):
    book_name: str


class FolkloreComment(Comment):
    folklore_name: str


class OrganizationComment(Comment):
    organization_name: str


class MemoComment(Comment):
    memo_name: str


class GuideComment(Comment):
    guide_name: str

