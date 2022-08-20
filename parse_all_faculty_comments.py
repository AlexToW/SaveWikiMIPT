import requests
from bs4 import BeautifulSoup as bs
import typing
import re

import comment

def get_faculty_name(url: str) -> str:
    r = requests.get(url)
    soup = bs(r.text, "lxml")
    return soup.find(id="firstHeading", class_="firstHeading").text.strip()


def get_all_faculty_urls() -> typing.List[str]:
    url = "http://wikimipt.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B0%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D0%B5%D1%82%D1%8B"
    r = requests.get(url)
    soup = bs(r.text, "lxml")

    urls = list()
    raw_groups_data = soup.find(id="mw-pages").find(class_="mw-content-ltr").find(class_="mw-category").find_all(class_="mw-category-group")
    for raw_group_data in raw_groups_data:
        raw_urls_data = raw_group_data.find("ul").find_all("li")
        for raw_url_data in raw_urls_data:
            urls.append("http://wikimipt.org" + raw_url_data.find("a").get("href"))
    
    return urls


def get_all_comments_by_page(page_url: str) -> typing.List[comment.FacultyComment]:
    comments: typing.List[comment.FacultyComment] = []
    comment_type = comment.CommentType.FACULTY

    print(f"Parsing faculty: {get_faculty_name(page_url)}")

    r = requests.get(page_url)
    soup = bs(r.text, "lxml")

    raw_comments_data = soup.find(id="allcomments").find_all(id=re.compile("comment*"))
    cnt = 1
    for raw_comment_data in raw_comments_data:
        if cnt > 1:
            print("\r" * ( len(str(cnt)) + len("Comment number: ")), end="")
        print(f"Comment number: {cnt}", end="")
        cnt += 1
        hidden = False
        reply = False
        class_str = " ".join(raw_comment_data.get("class"))
        if class_str == "c-item full":
            hidden = False
            reply = False
        elif class_str == "c-item c-comment-hidden full":
            hidden = True
            reply = False
        elif class_str == "c-item reply":
            hidden = False
            reply = True
        elif class_str == "c-item c-comment-hidden reply":
            hidden = True
            reply = True
        
        raw_user_data = raw_comment_data.find(class_="c-container").find(class_="c-user")
        author = raw_user_data.find("p").text.strip()
        date, time = raw_user_data.find(class_="c-time").text.split(" ")
        score = None
        if not hidden:
            score = raw_user_data.find(class_="c-score").find(class_="c-score-title").find(id=re.compile("Comment*")).text.strip()

        text = ""
        if not reply and not hidden:
            ok = False
            try:
                text = raw_comment_data.find(class_="c-container").find(class_="c-comment f-message").find("p").text.strip()
                ok = True
            except:
                pass
            if not ok:
                try:
                    text = raw_comment_data.find(class_="c-container").find(class_="c-comment f-message").find("ul").find("li").text.strip()
                except:
                    pass
        elif not reply and hidden:
            text = raw_comment_data.find(class_="c-container").find(class_="c-comment f-message").text.strip()
        elif reply and not hidden:
            ok = False
            try:
                text = raw_comment_data.find(class_="c-container").find(class_="c-comment r-message").find("p").text.strip()
                ok = True
            except:
                pass
            if not ok:
                try:
                    text = raw_comment_data.find(class_="c-container").find(class_="c-comment r-message").find("ul").find("li").text.strip()
                except:
                    pass
        elif reply and hidden:
            text = raw_comment_data.find(class_="c-container").find(class_="c-comment r-message").text.strip()
        
        link = ""
        if not reply and not hidden:
            try:
                link = raw_comment_data.find(class_="c-container").find(class_="c-comment f-message").find("p").find("a").get("href")
            except:
                pass
        elif reply and not hidden:
            try:
                link = raw_comment_data.find(class_="c-container").find(class_="c-comment r-message").find("p").find("a").get("href")
            except:
                pass
        elif not reply and hidden:
            link = ""
        elif reply and hidden:
            link = ""
        
        if len(link) > 0:
            text += "(" + link + ")"
        
        comm = comment.FacultyComment(type=comment_type, author=author, date=date, time=time, score=score, text=text, hidden=hidden, reply=reply)
        comm.faculty_name = get_faculty_name(page_url)
    
        comments.append(comm)
    print()
    return comments





def parse_all_faculty_comments() -> typing.List[comment.FacultyComment]:
    print(f"Parsing faculty comments...")
    comments: typing.List[comment.FacultyComment] = []

    for faculty_url in get_all_faculty_urls():
        for comm in get_all_comments_by_page(faculty_url):
            comments.append(comm)
    
    #print(len(comments))
    return comments


