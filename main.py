import typing
import comment
import json


from parse_all_faculty_comments import parse_all_faculty_comments               #[DONE]
from parse_all_department_comments import parse_all_department_comments         #[DONE]
from parse_all_subject_comments import parse_all_subject_comments               #[DONE]
from parse_all_teacher_comments import parse_all_teacher_comments               #[DONE]
from parse_all_book_comments import parse_all_book_comments                     #[DONE]
from parse_all_folklore_comments import parse_all_folklore_comments             #[DONE]
from parse_all_organization_comments import parse_all_organization_comments     #[DONE]
from parse_all_memo_comments import parse_all_memo_comments                     #[DONE]     (unusual)
from parse_all_guide_comments import parse_all_guide_comments                   #[DONE]


def comment_to_dict(comm):
    comm_dict = dict()
    comm_dict["author"] = comm.author
    comm_dict["date"] = comm.date
    comm_dict["time"] = comm.time
    comm_dict["score"] = comm.score
    comm_dict["text"] = comm.text
    comm_dict["hidden"] = comm.hidden
    comm_dict["reply"] = comm.reply

    if comm.type == comment.CommentType.FACULTY:
        comm_dict["type"] = "FACULTY"
    elif comm.type == comment.CommentType.DEPARTMENT:
        comm_dict["type"] = "DEPARTMENT"
    elif comm.type == comment.CommentType.SUBJECT:
        comm_dict["type"] = "SUBJECT"
    elif comm.type == comment.CommentType.TEACHER:
        comm_dict["type"] = "TEACHER"
    elif comm.type == comment.CommentType.BOOK:
        comm_dict["type"] = "BOOK"
    elif comm.type == comment.CommentType.FOLKLORE:
        comm_dict["type"] = "FOLKLORE"
    elif comm.type == comment.CommentType.ORGANIZATION:
        comm_dict["type"] = "ORGANIZATION"
    elif comm.type == comment.CommentType.MEMO:
        comm_dict["type"] = "MEMO"
    elif comm.type == comment.CommentType.GUIDE:
        comm_dict["type"] = "GUIDE"
    else:
        comm_dict["type"] = "UNKNOWN"
    
    return comm_dict


def collect_all_comments():
    all_comments = []
    for comm in parse_all_faculty_comments():
        all_comments.append(comm)
    for comm in parse_all_department_comments():
        all_comments.append(comm)
    for comm in parse_all_subject_comments():
        all_comments.append(comm)
    for comm in parse_all_teacher_comments():
        all_comments.append(comm)
    for comm in parse_all_book_comments():
        all_comments.append(comm)
    for comm in parse_all_folklore_comments():
        all_comments.append(comm)
    for comm in parse_all_organization_comments():
        all_comments.append(comm)
    for comm in parse_all_memo_comments():
        all_comments.append(comm)
    for comm in parse_all_guide_comments():
        all_comments.append(comm)
    
    return all_comments


def write_to_json(all_comments):
    data = dict()
    for comm in all_comments:
        if comm.type == comment.CommentType.FACULTY:
            data[comm.faculty_name] = comment_to_dict(comm)
        if comm.type == comment.CommentType.DEPARTMENT:
            data[comm.department_name] = comment_to_dict(comm)
        if comm.type == comment.CommentType.SUBJECT:
            data[comm.subject_name] = comment_to_dict(comm)
        if comm.type == comment.CommentType.TEACHER:
            data[comm.teacher_name] = comment_to_dict(comm)
        if comm.type == comment.CommentType.BOOK:
            data[comm.book_name] = comment_to_dict(comm)
        if comm.type == comment.CommentType.FOLKLORE:
            data[comm.folklore_name] = comment_to_dict(comm)
        if comm.type == comment.CommentType.ORGANIZATION:
            data[comm.organization_name] = comment_to_dict(comm)
        if comm.type == comment.CommentType.MEMO:
            data[comm.memo_name] = comment_to_dict(comm)
        if comm.type == comment.CommentType.GUIDE:
            data[comm.guide_name] = comment_to_dict(comm)
        
    with open("wikimipt_comments.json", "w") as json_out:
        json_dumps_str = json.dumps(data, indent=4)
        print(json_dumps_str, file=json_out)


def _main():
    write_to_json(collect_all_comments())



if __name__ == "__main__":
    _main()