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

def isDateLine(string=str):
    return re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]:", string)

def updateList(date, filename, outputFile="ContentManagement/postList.txt"):
    """
    Updates the postList.txt file to add a filename under the specified date.

    Args:
        date (str): The date in "YYYY-MM-DD" format.
        filename (str): The filename to add.
        outputFile (str, optional): The path to the postList.txt file. Defaults to "ContentManagement/postList.txt".
    """

    try:
        with open(outputFile, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    date_line_found = False
    updated_lines = []

    for line in lines:
        if line.startswith(date + ":"):
            date_line_found = True
            updated_lines.append(line)
            # Find the correct insertion point (maintaining alphabetical order)
            insertion_index = len(updated_lines)
            found_copy = False
            for i in range(len(lines) - lines.index(line) - 1):
                temp_line = lines[lines.index(line) + 1 + i].strip()  # Strip whitespace for comparison
                if temp_line.startswith(date) or temp_line == "":
                    break  # no more files under this date
                if temp_line < filename:
                    insertion_index = lines.index(line) + 2 + i
                if temp_line == filename:
                    found_copy = True
            if not found_copy:
                updated_lines.insert(insertion_index, f"\t{filename}\n")

        else:
            updated_lines.append(line)

    if not date_line_found:
        updated_lines.append(f"{date}:\n")
        updated_lines.append(f"\t{filename}\n")
        updated_lines.sort()  # sort the dates

    with open(outputFile, "w") as file:
        file.writelines(updated_lines)


def get_recent_dates(filepath="ContentManagement/postList.txt", n=5):
    """
    Retrieves the n most recent dates from a file formatted as "YYYY-MM-DD:".

    Args:
        filepath (str, optional): Path to the file. Defaults to "ContentManagement/postList.txt".
        n (int, optional): Number of recent dates to retrieve. Defaults to 5.

    Returns:
        list: A list of the n most recent dates in "YYYY-MM-DD" format, or an empty list if an error occurs.
    """
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return []

    dates = []
    for line in lines:
        if line.endswith(":\n") and len(line) == 12: #Checking that it is a date line.
            date_str = line[:10]  # Extract the date string
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d") #verify date format
                dates.append(date_obj)
            except ValueError:
                print(f"Warning: Invalid date format found: {date_str}")

    dates.sort(reverse=True)  # Sort dates in descending order (most recent first)

    return [date.strftime("%Y-%m-%d") for date in dates[:n]]

def get_dates_before(target_date, filepath="ContentManagement/postList.txt"):
    """
    Retrieves all dates from a file that are strictly before the given target date.

    Args:
        target_date (str): The target date in "YYYY-MM-DD" format.
        filepath (str, optional): Path to the file. Defaults to "ContentManagement/postList.txt".

    Returns:
        list: A list of dates (strings) that are before the target date, or an empty list if an error occurs.
    """
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return []

    try:
        target_date_obj = datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid target date format: {target_date}")
        return []

    before_dates = []
    for line in lines:
        if line.endswith(":\n") and len(line) == 12:  # Check for date line format
            date_str = line[:10]
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if date_obj < target_date_obj:
                    before_dates.append(date_str)
            except ValueError:
                print(f"Warning: Invalid date format found: {date_str}")

    return before_dates

def get_filenames_for_date(target_date, filepath="ContentManagement/postList.txt"):
    acc = []
    finding = False
    file = open(filepath, 'r')
    for line in file:
        if finding == False:
            if line == f"{target_date}:\n":
                finding = True
        else:
            if isDateLine(line):
                finding = False
                return acc
            else:
                acc.append(line.strip())
    return acc


def process_post(post_path, output_dir, post_type="Blogposts"):
    """Processes a single blog post or link post."""
    post_name = os.path.basename(post_path).removesuffix(".md")
    date = post_name[:10]
    name = titelize(post_name[11:])

    with open(post_path, 'r') as file:
        acc = "\n".join(refineMarkers(line) for line in file)
    mded = markdown.markdown(acc)

    if mded.splitlines()[0][:2] == "<p":
        acc = f"<div class=\"postInfo\">\n<h1 class=\"bigLink\"><a href=\"../Posts/{post_name}.html\">{name}</a></h1>\n<h4 class=\"postInfo\">Published {makeNiceDateName(date)}</h4>\n</div>\n"
        mded = acc + mded

    output_html_path = os.path.join(output_dir, f"{post_name}.html")
    with open(output_html_path, 'w') as file:
        file.write(mded)

    updateList(date, output_html_path)

    return name, date, mded, post_name

def process_blog_post(post_path, output_dir, posts_dir):
    """Processes regular blog posts and generates individual pages."""

    name, date, mded, post_name = process_post(post_path, output_dir, posts_dir)

    page_html_path = os.path.join("Posts", f"{post_name}.html")
    with open(page_html_path, 'w') as file:
        page_content = generatePage(mded)
        page_content = page_content.replace("<title>Eliora Hansonbrook</title>", f"<title>{name} – Eliora Hansonbrook</title>\n\t\t<meta property=\"og:title\" content=\"{name}\">\n\t\t<meta property=\"og:type\" content=\"article\">\n\t\t<meta property=\"og:url\" content=\"https://hansonbrook.com/Posts/{post_name}\">\n\t\t<meta property=\"og:image\" content=\"https://hansonbrook.com/Media/PreviewImage.png\">\n\t\t<meta property=\"og:sitename\" content=\"Eliora Hansonbrook\">")
        page_content = page_content.replace("<meta name=\"description\" content=\"Eliora Hansonbrook's blog\">", f"<meta name=\"description\" content=\"{str(re.split(r'\n', mded)[-1]).replace('<p>', '').replace('</p>', '')}\">{makeGoogleHappy(name, date)}")
        page_content = page_content.replace("<link rel=\"manifest\" href=\"/site.webmanifest\">", f"<link rel=\"manifest\" href=\"/site.webmanifest\">\n<link rel=\"canonical\" href=\"https://hansonbrook.com/Posts/{post_name}\">")
        file.write(page_content)

    return name, date, mded

def getMainPageStartDate():
    now = datetime.datetime.now()
    year = int(now.strftime("%Y"))
    month = int(now.strftime("%m"))-1
    if month < 0:
        month += 12
        year -= 1
    month = str(month)
    if len(month) == 1:
        month = f"0{month}"
    day = now.strftime("%d")
    startDate = f"{year}-{month}-{day}"
    return startDate

def generate_dates_until_today(start_date_str, date_format="%Y-%m-%d"):
    start_date = datetime.datetime.strptime(start_date_str, date_format).date()
    now = str(datetime.datetime.now())[:10]
    today = datetime.datetime.strptime(now, date_format).date()
    dates = []
    current_date = today
    while current_date > start_date:
        dates.append(current_date.strftime(date_format))
        current_date -= datetime.timedelta(days=1)
    return dates

def get_html_outputs_after_date(target_date):
    acc = []
    for date in generate_dates_until_today(target_date):
        for output in get_html_outputs_for_date(date):
            acc.append(output)
    return acc

def get_html_outputs_for_date(target_date):
    html_outputs = []
    current_date = target_date

    for filename in get_filenames_for_date(current_date):
        file_date_str = filename[:10]  # Extract date from filename
        if file_date_str > target_date:
            html_outputs.append(filename)

    return html_outputs


def main():
    postHTML = ""
    rssArticles = []
    output_dir = "Outputs"

    startDate = getMainPageStartDate()

    # Process Blogposts
    blog_posts_dir = "Blogposts"
    blog_posts = sorted(os.listdir(blog_posts_dir), reverse=True)
    for post in blog_posts:
        name, date, mded = process_blog_post(os.path.join(blog_posts_dir, post), output_dir, blog_posts_dir)
        rssArticles.append(generateRSSarticle(name, date, mded))

    # Process LinkPosts and add them to the main page
    link_posts_dir = "LinkPosts"
    link_posts = sorted(os.listdir(link_posts_dir), reverse=True)
    for post in link_posts:
        name, date, mded, post_name = process_post(os.path.join(link_posts_dir, post), output_dir, link_posts_dir)

    items = get_html_outputs_after_date(startDate)
    for item in items:
        file = open(f"{item}", 'r')
        contents = file.read()
        file.close()
        postHTML += contents + "\n<div class=\"space\"></div>\n"

    postHTML += "\n<div class=\"optionsBox\"><h3><a href=\"../archive.html\">See Older Posts in the Archive</a></h3></div>\n"
    createMain(postHTML)
    makeRSS(rssArticles)
    createArchive()
    create404()

if __name__ == "__main__":
    main()