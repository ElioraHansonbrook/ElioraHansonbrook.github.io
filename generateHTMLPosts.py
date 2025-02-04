import os
import shutil
import markdown

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
    <div>"""
    for post in os.listdir("Blogposts"):
        date = post[:10]
        name = post[11:].strip(".md").title().replace("-", " ")
        acc += f"\n <a href=Posts/{post.removesuffix(".md")}.html>{name}</a>"
    acc = acc + "\n</div>"
    os.remove("archiveTemplate.html")
    file = open("archiveTemplate.html", 'w')
    file.write(acc)
    file.close()
    os.remove("archive.html")
    acc = generatePage(acc)
    file = open("archive.html", 'w')
    file.write(acc)
    file.close()
            
i = 0
postHTML = ""
for post in os.listdir("Blogposts"):
    file = open("Blogposts/" + post, 'r')
    acc = ""
    for line in file:
        acc = acc + "\n" + line
    acc = refineMarkers(acc)
    mded = markdown.markdown(acc)
    file.close()
    shutil.rmtree("Outputs")
    os.mkdir("Outputs")
    postName = post.removesuffix(".md")
    file = open("Outputs/" + postName + ".html", 'w')
    file.write(mded)
    file.close()
    shutil.rmtree("Posts")
    os.mkdir("Posts")
    file = open("Posts/" + postName + ".html", 'w')
    acc = generatePage(mded)
    file.write(acc)
    file.close()
    postHTML = postHTML + mded
    i = i + 1
createMain(postHTML)
createArchive()