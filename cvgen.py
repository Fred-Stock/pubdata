#!/usr/bin/env python3
import yaml
from jinja2 import Environment, FileSystemLoader

def normalize_link(link, website):
    if link and link.startswith("docstore:"):
        return website.rstrip('/') + '/docstore/' + link[len("docstore:"):]
    return link

def load_yaml(fn):
    with open(fn, 'r') as f:
        return yaml.safe_load(f)

if __name__ == '__main__':
    personal = {
        'name': 'Jack Spalding-Jamieson',
        'email': 'jacksj@uwaterloo.ca',
        'phone': '+1-250-878-9930',
        'website': 'https://jacksj.com',
        'scholar': 'https://scholar.google.com/citations?user=GKhnWJMAAAAJ'
    }

    data = {
        'personal': personal,
        'accolades': load_yaml('accolades.yaml'),
        'education': load_yaml('education.yaml'),
        'positions': load_yaml('positions.yaml'),
        'pubs': load_yaml('pubs.yaml'),
        'service': load_yaml('service.yaml'),
        'talks': load_yaml('talks.yaml'),
    }

    # normalize docstore links
    for pub in data['pubs']:
        pub['pdf_link']  = normalize_link(pub.get('pdf_link'),  data['personal']['website'])
        pub['code_link'] = normalize_link(pub.get('code_link'), data['personal']['website'])

    for talk in data['talks']:
        talk['slides_link'] = normalize_link(talk.get('slides_link'), data['personal']['website'])

    env = Environment(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='<<',
        variable_end_string='>>',
        loader=FileSystemLoader('template'),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tpl = env.get_template('cv_template.tex')
    out = tpl.render(**data)
    with open('tex/cv.tex', 'w') as f:
        f.write(out)
    print("Wrote tex/cv.tex")
