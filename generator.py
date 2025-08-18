import yaml
from collections import defaultdict

def normalize_link(link):
    if link and link.startswith("docstore:"):
        return "https://jacksj.com/docstore/" + link[len("docstore:"):]
    return link

# Load the YAML files
with open('pubs.yaml', 'r') as file:
    publications = yaml.safe_load(file)

with open('talks.yaml', 'r') as f:
    talks = yaml.safe_load(f)

# ensure every entry has a non-empty short_title and venue_short
for pub in publications:
    if not pub.get('short_title'):
        pub['short_title'] = pub['title']
    if not pub.get('venue_short'):
        pub['venue_short'] = pub.get('venue', '')

for talk in talks:
    if not talk.get('short_title'):
        talk['short_title'] = talk['title']
    if not talk.get('venue_short'):
        talk['venue_short'] = talk.get('venue', '')

# Define the self-author
self_author = "Frederick Stokc"
self_author_modified = "Freddy"

# Personal information for the header
email = "frederick <underscore> stock <at> student.uml.edu "
#subtitle = "Researcher and Software Engineer in Computational Geometry"
subtitle = "Researcher and Software Engineer"
bio = ("I am a researcher and software engineer "
       "and low-level distributed robotics graph-compute systems.")

# Define the order of venue types
venue_order = ["preprint", "conference", "journal", "thesis", "workshop", "software"]
venue_type_title = {
    "preprint": "Preprints",
    "workshop": "Workshop Papers and Others",
    "conference": "Conference Papers",
    "journal": "Journal Papers",
    "thesis": "Theses",
    "software": "Software",
}

# Organize publications by venue type and year
organized_pubs = defaultdict(lambda: defaultdict(list))
for pub in publications:
    venue_type = pub['venue_type'].lower()
    year = pub['publication_year']
    organized_pubs[venue_type][year].append(pub)

# Sort venue types and years
sorted_venue_types = [v for v in venue_order if v in organized_pubs]
for venue_type in organized_pubs:
    organized_pubs[venue_type] = dict(sorted(organized_pubs[venue_type].items(), reverse=True))

# Generate HTML for publications
def generate_pub_html(pub):
    authors = ', '.join([f"<b>{self_author_modified}</b>" if author == self_author else author for author in pub['authors']])
    if "venue" in pub.keys():
        venue = f'<abbr title="{pub["venue"]}">{pub["venue_short"]}</abbr>'
        venue_span = f"<span class=\"pub-venue\">{venue}, {pub['publication_year']}</span>"
    else:
        venue = ""
        #venue_span = ""
        venue_span = f"<span class=\"pub-venue\">{pub['publication_year']}</span>"
    if "comment" in pub.keys():
        comment_span = f"<span class=\"pub-comment\">{pub["comment"]}</span>"
    else:
        comment_span = ""

    links = ""
    pdf_link = normalize_link(pub.get('pdf_link'))
    code_link = normalize_link(pub.get('code_link'))
    if pdf_link:
        links += f'<span class="icon-wrapper"><a href="{pdf_link}" target="_blank"><img src="pdf_icon.png" alt="PDF" width="16"></a></span>'
    if code_link:
        links += f' <span class="icon-wrapper"><a href="{code_link}" target="_blank"><img src="code_icon.png" alt="Code" width="16"></a></span>'

    # Determine the main link for the clickable box
    main_link = pdf_link if pdf_link else code_link

    if main_link:
        return f"""
        <li class="roundbox clickable-pub">
            <a href="{main_link}" target="_blank" class="pub-bg-link"></a>
            <div class="pub-entry">
                <div class="pub-header">
                    <div class="pub-links">{links}</div>
                    <span class="pub-title">{pub['short_title']}</span>
                </div>
                <span class="pub-authors">{authors}</span><br>
                {venue_span}
                {comment_span}
            </div>
        </li>
        """
    else:
        return f"""
        <li class="roundbox">
            <div class="pub-entry">
                <div class="pub-header">
                    <div class="pub-links">{links}</div>
                    <span class="pub-title">{pub['short_title']}</span>
                </div>
                <span class="pub-authors">{authors}</span><br>
                {venue_span}
                {comment_span}
            </div>
        </li>
        """

def generate_talk_html(talk):
    slides = normalize_link(talk.get('slides_link'))
    links = ""
    if slides:
        links = f'<a href="{slides}" target="_blank"><img src="pdf_icon.png" alt="Slides" width="16"></a>'

    venue = f'<abbr title="{talk["venue"]}">{talk["venue_short"]}</abbr>'
    venue_span = f'<span class="pub-venue">{venue}, {talk["year"]}</span>'
    comment_span = f'<span class="pub-comment">{talk["comment"]}</span>' if talk.get("comment") else ""

    return f"""
    <li class="roundbox">
        <div class="pub-entry">
            <div class="pub-header">
                <div class="pub-links">{links}</div>
                <span class="pub-title" title="{talk['title']}">{talk['short_title']}</span>
            </div>
            {venue_span}
            {comment_span}
        </div>
    </li>
    """

# Generate Publications Section HTML
pubs_html = ""
for venue_type in sorted_venue_types:
    pubs_html += f"<h4>{venue_type_title[venue_type]}</h4><ul>"
    for year in organized_pubs[venue_type]:
        for pub in organized_pubs[venue_type][year]:
            pubs_html += generate_pub_html(pub)
    pubs_html += "</ul>"

# Generate Talks Section HTML
talks_html = "<ul>"
for talk in sorted(reversed(talks), key=lambda x: x['year'], reverse=True):
    talks_html += generate_talk_html(talk)
talks_html += "</ul>"

# Full HTML Template
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self_author_modified}</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* Global Styles */
        body {{
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }}
        #container {{
            max-width: 900px;
            width: 100%;
        }}
        h1 {{
            font-size: 2.5em;
            margin-bottom: 5px;
        }}
        h2 {{
            font-size: 1.5em;
            color: #666;
            margin-top: 0;
        }}
        p.bio {{
            font-size: 1em;
            color: #555;
        }}
        a.email {{
            font-size: 1em;
            color: #007BFF;
            text-decoration: none;
        }}
        a.email:hover {{
            text-decoration: underline;
        }}

        /* Publications Section */
        h3, h4 {{
            color: #444;
            border-bottom: 2px solid #ccc;
            padding-bottom: 5px;
        }}
        ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        .roundbox {{
            background-color: #fff;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            max-width: 600px; /* Width of work/pub slides */
            width: 100%;
            margin: 10px auto;  /* Center each entry horizontally */
        }}
        .pub-entry {{
            display: flex;
            flex-direction: column;
        }}
        .pub-header {{
            display: flex;
            align-items: center;
        }}
        .pub-links {{
            margin-right: 5px; /* Space between icons and title */
        }}
        .pub-title {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        .pub-title:hover {{
            text-decoration: underline;
            cursor: help;
        }}
        .pub-authors {{
            font-size: 0.9em;
            color: #555;
        }}
        .pub-venue {{
            font-size: 0.85em;
            color: #777;
        }}
        .pub-comment {{
            font-size: 0.85em;
            color: #444;
        }}
        .pub-links a img {{
            margin-right: 0px;
        }}
        .clickable-pub {{
            position: relative;
            transition: box-shadow 0.2s ease;
        }}
        .clickable-pub:hover {{
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}
        .clickable-pub:hover .pub-title {{
            text-decoration: underline;
        }}
        .pub-bg-link {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }}
        .pub-entry {{
            position: relative;
            z-index: 2;
            pointer-events: none;
        }}
        .pub-links {{
            position: relative;
            z-index: 10;
            pointer-events: auto;
        }}
    </style>
</head>
<body>
    <div id="container">
        <!-- Header Section -->
        <header>
            <h1>{self_author_modified}</h1>
            <h2>{subtitle}</h2>
            <a class="email">{email}</a>
            <p class="bio">{bio}</p>
        </header>

        <!-- Works Section -->
        <div id="content">
            <h3><b>Works</b></h3>
            {pubs_html}
        </div>

        <!-- Presentation Section -->
        <div id="content">
            <h3><b>Presentations</b></h3>
            {talks_html}
        </div>
    </div>
</body>
</html>
"""

# Write to an HTML file
with open("index.html", "w") as f:
    f.write(html_template)

print("Updated HTML homepage generated successfully as 'index.html'.")
