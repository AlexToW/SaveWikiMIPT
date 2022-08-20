import requests
from bs4 import BeautifulSoup as bs
import typing
import re

import comment


def get_teacher_name(url: str) -> str:
    r = requests.get(url)
    soup = bs(r.text, "lxml")
    return soup.find(id="content", class_="mw-body").find(id="firstHeading", class_="firstHeading").text.strip()


def get_all_comments_by_page(page_url: str) -> typing.List[comment.TeacherComment]:
    comments: typing.List[comment.TeacherComment] = []
    comment_type = comment.CommentType.TEACHER

    print(f"Parsing subject: {get_teacher_name(page_url)}")

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
        
        comm = comment.TeacherComment(type=comment_type, author=author, date=date, time=time, score=score, text=text, hidden=hidden, reply=reply)
        comm.teacher_name = get_teacher_name(page_url)
    
        comments.append(comm)
    print()
    return comments


def get_teachers_urls(url: str) -> typing.List[str]:
    # список ссылок на странички препов, взятых из teacher_lists_urls
    teachers_urls: typing.List[str] = []

    r = requests.get(url)
    soup = bs(r.text, "lxml")

    urls_data = soup.find(id="mw-pages").find(class_="mw-content-ltr").find(class_="mw-category").find_all(class_="mw-category-group")

    for url_data in urls_data:
        raw_urls = url_data.find("ul").find_all("li")
        for raw_url in raw_urls:
            url = raw_url.find("a").get("href")
            teachers_urls.append(url)
    
    return teachers_urls



def parse_all_teacher_comments() -> typing.List[comment.TeacherComment]:
    teacher_lists_urls: typing.List[str] = list( 
        ["http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pageuntil=%D0%92%D0%B8%D0%BA%D1%82%D0%BE%D1%80+%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B8%D1%87+%D0%9F%D0%B0%D0%BD%D0%BA%D1%80%D0%B0%D1%82%D0%BE%D0%B2#mw-pages",
        "http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%92%D0%B8%D0%BA%D1%82%D0%BE%D1%80+%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B8%D1%87+%D0%9F%D0%B0%D0%BD%D0%BA%D1%80%D0%B0%D1%82%D0%BE%D0%B2#mw-pages",
        "http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%96%D0%B4%D0%B0%D0%BD%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9+%D0%98%D0%BB%D1%8C%D1%8F+%D0%AE%D1%80%D1%8C%D0%B5%D0%B2%D0%B8%D1%87#mw-pages",
        "http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%9A%D0%BE%D0%BF%D1%87%D0%B5%D0%BD%D0%BE%D0%B2+%D0%92%D0%B0%D0%BB%D0%B5%D1%80%D0%B8%D0%B9+%D0%98%D0%B3%D0%BE%D1%80%D0%B5%D0%B2%D0%B8%D1%87#mw-pages",
        "http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%9C%D0%B5%D1%82%D0%BB%D0%BE%D0%B2+%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80+%D0%92%D0%B8%D0%BA%D1%82%D0%BE%D1%80%D0%BE%D0%B2%D0%B8%D1%87#mw-pages",
        "http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%A0%D0%B5%D0%B4%D0%BA%D0%BE%D0%B7%D1%83%D0%B1%D0%BE%D0%B2%D0%B0+%D0%95%D0%BB%D0%B5%D0%BD%D0%B0+%D0%AE%D1%80%D1%8C%D0%B5%D0%B2%D0%BD%D0%B0#mw-pages",
        "http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%A2%D1%83%D0%BC%D0%B0%D0%B9%D0%BA%D0%B8%D0%BD+%D0%98%D0%BB%D1%8C%D1%8F+%D0%9D%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B5%D0%B2%D0%B8%D1%87#mw-pages"]
    )
    comments: typing.List[comment.TeacherComment] = []
    for page_url in teacher_lists_urls:
        for teacher_url in get_teachers_urls(page_url):
            teacher_url = "http://wikimipt.org" + teacher_url
            for comment in get_all_comments_by_page(teacher_url):
                comments.append(comment)
    
    return comments
