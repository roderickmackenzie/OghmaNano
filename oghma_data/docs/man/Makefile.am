#latex2html man  -html_version 5,math
# -shell-escape is for minted

all: understanding_oghma_nano.pdf
	echo "Docs built"

understanding_oghma_nano.pdf: *.tex understanding_oghma_nano.bib
	pdflatex -shell-escape understanding_oghma_nano
	makeindex understanding_oghma_nano
	bibtex understanding_oghma_nano
	pdflatex -shell-escape  understanding_oghma_nano
	

clean:
	rm *.pdf *.aux *.rtf *.tmp *.xref *.ind *.docx *.dvi *.idx *.out *.log *.bbl -f
	rm _minted-man -rf


