file:=overview
dir:=./texfiles

all: direct
	pdflatex -output-directory $(dir) $(file).tex
	ln -sf $(dir)/$(file).pdf $(file).pdf
direct:
	mkdir -p $(dir)

clean:
	rm -rf $(dir) $(file).pdf
