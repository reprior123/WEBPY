from tex import latex2pdf
document = ur"""
... \documentclass{article}
... \begin{document}
... Hello, World!
... \end{document}
... """

print 'got here'
pdf = latex2pdf(document)
type(pdf)
<type 'str'>
print "PDF size: %.1f KB" % (len(pdf) / 1024.0)
PDF size: 5.6 KB
pdf[:5]
'%PDF-'
pdf[-6:]
'%%EOF\n'