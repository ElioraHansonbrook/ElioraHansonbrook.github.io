import os
import shutil
import calendar
import datetime
import markdown
import time
import re
from email import utils

def makeGoogleHappy(title = str, date = str):
    return """
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": \"""" + title + """\",
        "image": [
            "https://hansonbrook.com/Media/PreviewImage.png"
        ],
        "datePublished": \"""" + date + """\",
        "dateModified": \"""" + date + """\",
        "author": [{
          "@type": "Person",
          "name": "Eliora Hansonbrook",
          "url": "https://hansonbrook.com"
        }]
    }
    </script>
    """

def titelize(string=str):
    return string.title().replace("-", " ").replace(" And ", " and ").replace(" The ", " the ").replace(" Of ", " of ").replace("Trumpscript", "TrumpScript")

def generateRSSarticle(name, date, content=str):
    dateB = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10]))
    tuple = dateB.timetuple()
    timeStamp = time.mktime(tuple)
    dateB = utils.formatdate(timeStamp+3600*6)
    xml = "\n<item>\n<title>"+ name + "</title>\n"
    xml += "<pubDate>" + str(dateB) + "</pubDate>\n"  # Add publication date
    xml += "<author>eliora@hansonbrook.com (Eliora Hansonbrook)</author>\n"  # Add email
    xml += "<description><![CDATA[" + content.replace("../", "https://hansonbrook.com/") + "]]></description>\n"  # Add content/description
    xml += "<guid>https://hansonbrook.com/Posts/" + date + "-" + name.replace(" ", "-").lower() + "</guid>\n"
    xml += "<link>https://hansonbrook.com/Posts/" + date + "-" + name.replace(" ", "-").lower() + "</link>\n"
    xml += "</item>\n"
    return xml

def makeRSS(articles):
    xml = f"""<?xml version="1.0"?>
    <rss version="2.0">
    <channel>
    <title>Eliora Hansonbrook</title>
    <link>https://hansonbrook.com</link>
    <description>The latest posts from the blog</description>
    <language>en</language>
    <lastBuildDate>{datetime.datetime.now()}</lastBuildDate>
    <category>Politics</category>
    <copyright>©2025 Eliiora Hansonbrook. All Rights Reserved.</copyright>
    <managingEditor>eliora@hansonbrook.com (Eliora Hansonbrook)</managingEditor>"""
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
    file = open("Templates/sidebar.html", 'r')
    for line in file:
        sidebar = sidebar + line
    file.close()
    return sidebar

def getTopbar():
    topbar = ""
    file = open("Templates/topbar.html", 'r')
    for line in file:
        topbar = topbar + line
    file.close()
    return topbar

def generatePage(withStr: str):
    sidebar = getSidebar()
    topbar = getTopbar()
    acc = ""
    file = open("Templates/template.html", 'r')
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
    currMonth = ""
    dir = os.listdir("Blogposts")
    dir.sort()
    dir.reverse()
    for post in dir:
        date = post[:10]
        month = date[5:7]
        postMonth = calendar.month_name[int(month)] + " " + date[:4]
        if postMonth != currMonth:
            acc = acc + f"\n<h3>{postMonth}</h3>\n"
            currMonth = postMonth
        name = titelize(post[11:].removesuffix(".md"))
        acc += f"\n <a href=Posts/{post.removesuffix(".md")}.html class=\"archiveItem\">{name}</a>"
    acc = acc + "\n</div>"
    file = open("Templates/archiveTemplate.html", 'w')
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

def getSpecialAnnouncementHTML(title = str, subtitle = str, top = str, bottom = str):
    return f"""
    <div class = "specialAnnouncement" aria-hidden="true">
        <h1 aria-hidden="true">{title}</h1>
        <h4 aria-hidden="true">{subtitle}</h4>
        <div class = "floatingElementTop">
            <h6 aria-hidden="true">{top}</h6>
        </div>
        <div class = "floatingElementBottom">
            <h6 aria-hidden="true">{bottom}</h6>
        </div>
    </div>"""

def main():
    i = 0
    postHTML = ""
    rssArticles = []
    dir = os.listdir("Blogposts")
    dir.sort()
    dir.reverse()
    for post in dir:
        date = post[:10]
        name = titelize(post[11:].removesuffix(".md"))
        file = open("Blogposts/" + post, 'r')
        postName = post.removesuffix(".md")
        acc = ""
        for line in file:
            acc += "\n" + refineMarkers(line)
        mded = markdown.markdown(acc)
        rssArticles.append(generateRSSarticle(name, date, mded))
        acc = "<div class=\"postInfo\">\n<h1 class=\"bigLink\"><a href=\"../Posts/" + postName +".html\">" + name + "</a></h1>\n<h4 class=\"postInfo\">Published " + makeNiceDateName(date) + "</h4>\n</div>\n"
        mded = acc + mded
        file.close()
        file = open("Outputs/" + postName + ".html", 'w')
        file.write(mded)
        file.close()
        file = open("Posts/" + postName + ".html", 'w')
        acc = generatePage(mded)
        acc = acc.replace("<title>Eliora Hansonbrook</title>", "<title>" + name + " – Eliora Hansonbrook</title>\n\t\t<meta property=\"og:title\" content=\"" + name + "\">\n\t\t<meta property=\"og:type\" content=\"article\">\n\t\t<meta property=\"og:url\" content=\"https://hansonbrook.com/Posts/" + postName + "\">\n\t\t<meta property=\"og:image\" content=\"https://hansonbrook.com/Media/PreviewImage.png\">\n\t\t<meta property=\"og:sitename\" content=\"Eliora Hansonbrook\">")
        acc = acc.replace("<meta name=\"description\" content=\"Eliora Hansonbrook's blog\">", "<meta name=\"description\" content=\"" + str(re.split("\n", mded)[-1]).replace("<p>", "").replace("</p>", "") + "\">" + makeGoogleHappy(name, date))
        acc = acc.replace("<link rel=\"manifest\" href=\"/site.webmanifest\">", f"<link rel=\"manifest\" href=\"/site.webmanifest\">\n<link rel=\"canonical\" href=\"https://hansonbrook.com/Posts/{postName}\">")
        file.write(acc)
        file.close()
        if i < 5:
            postHTML = postHTML + mded + "\n<div class=\"space\"></div>\n"
        elif i == 5:
            postHTML = postHTML + mded
        i = i + 1
    #postHTML = getSpecialAnnouncementHTML("Introducing TrumpScript", "A Satirical Programming Language", "Macalester College • Olin-Rice Science Hall • Room 254", "Friday, February 28, 2025 • 10:10 A.M.") + postHTML
    postHTML = postHTML + "\n<div class=\"optionsBox\"><h3><a href=\"../archive.html\">See Older Posts in the Archive</a></h3></div>\n"
    createMain(postHTML)
    makeRSS(rssArticles)
    createArchive()
    create404()

if __name__ == "__main__":
    main()