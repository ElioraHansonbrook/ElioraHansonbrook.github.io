import os
import shutil
import calendar
import datetime
import markdown
import time
import re
from email import utils

def titelize(string=str):
    return string.title().replace("-", " ").replace(" And ", " and ").replace(" The ", " the ").replace(" Of ", " of ")

def generateRSSarticle(name, date, content=str):
    dateB = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10]))
    tuple = dateB.timetuple()
    timeStamp = time.mktime(tuple)
    dateB = utils.formatdate(timeStamp+3600*6)
    xml = "\n<item>\n<title>"+ name + "</title>\n"
    xml += "<pubDate>" + str(dateB) + "</pubDate>\n"  # Add publication date
    xml += "<author>Eliora Hansonbrook</author>\n"  # Add byline
    xml += "<description><![CDATA[" + content.replace("../", "https://hansonbrook.com/") + "]]></description>\n"  # Add content/description
    xml += "<link>https://hansonbrook.com/Posts/" + date + "-" + name.replace(" ", "-").lower() + "</link>\n"
    xml += "</item>\n"
    return xml

def makeRSS(articles):
    xml = """<?xml version="1.0"?>
    <rss version="2.0">
    <channel>
    <title>Eliora Hansonbrook</title>
    <link>https://hansonbrook.com</link>
    <description>The latest posts from the blog</description>
    <language>en</language>
    <copyright>©2025 Eliiora Hansonbrook. All Rights Reserved.</copyright>
    <managingEditor>eliora@hansonbrook.com</managingEditor>"""
    for article in articles:
        xml += article
    xml += """
        </channel>
    </rss>
    """
    file = open("rss.xml", 'w')
    file.write(xml)
    file.close()

def makeNiceDateName(date: str):
    year = date[:4]
    month = date[5:7]
    day = date [8:10].removeprefix("0")
    return calendar.month_name[int(month)] + " " + day + ", " + year

def getSidebar():
    sidebar = ""
    file = open("sidebar.html", 'r')
    for line in file:
        sidebar = sidebar + line
    file.close()
    return sidebar

def getTopbar():
    topbar = ""
    file = open("topbar.html", 'r')
    for line in file:
        topbar = topbar + line
    file.close()
    return topbar

def generatePage(withStr: str):
    sidebar = getSidebar()
    topbar = getTopbar()
    acc = ""
    file = open("template.html", 'r')
    for line in file:
        if line.__contains__("No Text Here Right Now."):
            acc = acc + withStr + "\n"
        elif line.__contains__("Sidebar."):
            acc = acc + sidebar + "\n"
        elif line.__contains__("Topbar."):
            acc = acc + topbar + "\n"
        else:
            acc = acc + line
    file.close()
    return acc

def createMain(withStr: str):
    acc = generatePage(withStr)
    file = open("index.html", 'w')
    file.write(acc)
    file.close()

def refineMarkers(text: str):
    acc = ""
    for i in range(len(text)):
        if text[i] == "\"":
            if text[i+1] != " " and text[i+1] != "\n":
                acc = acc + "“"
            else: 
                acc = acc + "”"
        elif text[i] == "\'":
            if text[i-1] == " " or text[i-1] == "\n":
                acc = acc + "‘"
            else: 
                acc = acc + "’"
        else:
            acc = acc + text[i]
    return acc

def createArchive():
    acc = """<h1>Archive</h1>
    <div class=\"archive\">
    <div class=\"miniSpace\"></div>"""
    for post in os.listdir("Blogposts"):
        date = post[:10]
        name = titelize(post[11:].removesuffix(".md"))
        acc += f"\n <a href=Posts/{post.removesuffix(".md")}.html class=\"archiveItem\">{name}</a>"
    acc = acc + "\n</div>"
    file = open("archiveTemplate.html", 'w')
    file.write(acc)
    file.close()
    acc = generatePage(acc)
    acc = acc.replace("<title>Eliora Hansonbrook</title>", "<title>The Hansonbrook Blog Archive</title>")
    file = open("archive.html", 'w')
    file.write(acc)
    file.close()

def create404():
    page = generatePage(withStr="<h1>404: Page Not Found</h1>")
    file = open("404.html", 'w')
    file.write(page)
    file.close()
            
i = 0
postHTML = ""
shutil.rmtree("Outputs")
os.mkdir("Outputs")
shutil.rmtree("Posts")
os.mkdir("Posts")
rssArticles = []
for post in os.listdir("Blogposts"):
    date = post[:10]
    name = titelize(post[11:].removesuffix(".md"))
    file = open("Blogposts/" + post, 'r')
    postName = post.removesuffix(".md")
    acc = ""
    for line in file:
        acc += "\n" + refineMarkers(line)
    mded = markdown.markdown(acc)
    rssArticles.append(generateRSSarticle(name, date, mded))
    acc = "<div class=\"postInfo\">\n<h1 class=\"bigLink\"><a href=\"../Posts/" + postName + ".html\">" + name + "</a></h1>\n<h4 class=\"postInfo\">Published " + makeNiceDateName(date) + "</h4>\n</div>\n"
    mded = acc + mded
    file.close()
    file = open("Outputs/" + postName + ".html", 'w')
    file.write(mded)
    file.close()
    file = open("Posts/" + postName + ".html", 'w')
    acc = generatePage(mded)
    acc = acc.replace("<title>Eliora Hansonbrook</title>", "<title>" + name + " – Eliora Hansonbrook</title>")
    acc = acc.replace("<meta name=\"description\" content=\"Eliora Hansonbrook's blog\">", "<meta name=\"description\" content=\"" + str(re.split("\n", mded)[-1]).replace("<p>", "").replace("</p>", "") + "\">")
    file.write(acc)
    file.close()
    if i < len(os.listdir("Blogposts")) - 1:
        postHTML = postHTML + mded + "\n<div class=\"space\"></div>\n"
    else:
        postHTML = postHTML + mded
    i = i + 1
createMain(postHTML)
makeRSS(rssArticles)
createArchive()
create404()