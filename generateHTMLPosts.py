import os
import shutil
import calendar
import markdown

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
    os.remove("index.html")
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
        name = post[11:].strip(".md").title().replace("-", " ").replace(" And ", " and ").replace(" The ", " the ")
        acc += f"\n <a href=Posts/{post.removesuffix(".md")}.html class=\"archiveItem\">{name}</a>"
    acc = acc + "\n</div>"
    os.remove("archiveTemplate.html")
    file = open("archiveTemplate.html", 'w')
    file.write(acc)
    file.close()
    os.remove("archive.html")
    acc = generatePage(acc)
    acc = acc.replace("<title>Eliora Hansonbrook</title>", "<title>The Hansonbrook Blog Archive</title>")
    file = open("archive.html", 'w')
    file.write(acc)
    file.close()

def create404():
    page = generatePage(withStr="<h1>404: Page Not Found</h1>")
    os.remove("404.html")
    file = open("404.html", 'w')
    file.write(page)
    file.close()
            
i = 0
postHTML = ""
shutil.rmtree("Outputs")
os.mkdir("Outputs")
shutil.rmtree("Posts")
os.mkdir("Posts")
for post in os.listdir("Blogposts"):
    date = post[:10]
    name = post[11:].strip(".md").title().replace("-", " ").removesuffix(".md").replace(" And ", " and ").replace(" The ", " the ")
    file = open("Blogposts/" + post, 'r')
    postName = post.removesuffix(".md")
    acc = "<div class=\"postInfo\">\n<h1 class=\"bigLink\"><a href=\"../Posts/" + postName + ".html\">" + name + "</a></h1>\n<h4 class=\"postInfo\">Published " + makeNiceDateName(date) + "</h4>\n</div>"
    for line in file:
        acc = acc + "\n" + refineMarkers(line)
    mded = markdown.markdown(acc)
    file.close()
    file = open("Outputs/" + postName + ".html", 'w')
    file.write(mded)
    file.close()
    file = open("Posts/" + postName + ".html", 'w')
    acc = generatePage(mded)
    acc = acc.replace("<title>Eliora Hansonbrook</title>", "<title>" + name + " – Eliora Hansonbrook</title>")
    file.write(acc)
    file.close()
    if i < len(os.listdir("Blogposts")) - 1:
        postHTML = postHTML + mded + "\n<div class=\"space\"></div>\n"
    else:
        postHTML = postHTML + mded
    i = i + 1
createMain(postHTML)
createArchive()
create404()