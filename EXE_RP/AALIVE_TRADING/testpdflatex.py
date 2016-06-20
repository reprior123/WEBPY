import re # import regular expressions module
project = "./" # specify the project folder
print project, 'is pro'
in_file = "{}example.txt".format(project) # path to the txt-file relative to the project folder
with open(in_file) as f:    # loads the file
    content = f.read()
    keys = re.findall(r"%(.+):", content)   # find the keys using RegEx
    values = re. findall(r":\s*([\w\W]+?)\s*(?:%|$)", content) # find the values using RegEx
options = zip(keys, values) # combining keys and values in one nested list
print options
tex_code = ""
for key, value in options:
    tex_code = tex_code + "\\newcommand{{\\{}}}{{{}}}\n".format(key, value)

template = "test"

newtext = """
\documentclass{article}

\\title{Title of my document}
\\date{2013-09-01}
\\author{John Doe}

\\begin{document}

\maketitle
\pagenumbering{gobble}
\\newpage
\pagenumbering{arabic}

\section{Section}

Hello World!

\subsection{Subsection}

Structuring a document is easy!

\end{document}
"""

print newtext
tex_code = tex_code + """

\\documentclass{{{}}} % din a4, 11 pt, one-sided,

\\begin{{document}}

\\end{{document}}
""".format(template)

tex_code = newtext + """
""".format(template)
import os, shutil

build_d = project +'build/'
print build_d
out_file = "{}sample2".format(build_d)

if not os.path.exists(build_d):  # create the build directory if not existing
    os.makedirs(build_d)

with open(out_file+".tex", "w") as f:  # saves tex_code to output file
    f.write(tex_code)    

os.system("pdflatex -output-directory {} {}".format(os.path.realpath(build_d), os.path.realpath(out_file)))
shutil.copy2(out_file+".pdf", os.path.dirname(os.path.realpath(in_file)))

