file:=feb_update
dir:=./texfiles
feyndir:=feyn

all: $(file).tex
	pdflatex -output-directory $(dir) $(file).tex
	ln -sf $(dir)/$(file).pdf $(file.pdf)
	ln -sf $(dir)/$(feyndir) feyn

smaller:
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$(file)_comp.pdf $(dir)/$(file).pdf

clean:
	rm -f $(dir)/*.log $(dir)/*.nav $(dir)/*.aux $(dir)/*.out $(dir)/*.pdf $(dir)/*.snm $(dir)/*.toc $(dir)/*.vrb $(dir)/$(feyndir)/* $(file).pdf feyn $(file)_comp.pdf
