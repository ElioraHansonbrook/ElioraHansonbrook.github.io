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

def generatePage(withStr: str):
    sidebar = getSidebar()
    acc = ""
    file = open("template.html", 'r')
    for line in file:
        if line.__contains__("No Text Here Right Now."):
            acc = acc + withStr
        elif line.__contains__("Sidebar."):
            acc = acc + sidebar
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
        acc += f"\n <a href=Posts/{post}.html>{name}</a>"
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
    file = open("Outputs/" + post + ".html", 'w')
    file.write(mded)
    file.close()
    shutil.rmtree("Posts")
    os.mkdir("Posts")
    file = open("Posts/" + post + ".html", 'w')
    acc = generatePage(mded)
    file.write(acc)
    file.close()
    postHTML = postHTML + mded
    i = i + 1
createMain(postHTML)
createArchive()