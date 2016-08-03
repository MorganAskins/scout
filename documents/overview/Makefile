file:=overview
dir:=./texfiles

all: direct
	pdflatex -output-directory $(dir) $(file).tex
	ln -sf $(dir)/$(file).pdf $(file).pdf
direct:
	mkdir -p $(dir)

smaller:
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$(file)_comp.pdf $(dir)/$(file).pdf

clean:
	rm -rf $(dir) $(file).pdf
