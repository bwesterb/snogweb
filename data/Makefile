%.raw.dot: %.snog
	python ../snog2dot.py < $< > $@

%.pos.dot: %.raw.dot
	neato -Elen=10 < $< > tmp
	neato -s -Elen=1 < tmp > tmp2
	fdp -s -Elen=0.011 -Gsplines=true -Gmaxiter=10000 < tmp2 > $@
	rm tmp tmp2

%.anon.pos.dot: %.pos.dot
	python ../anonymize-dot.py $< $@

view-%: %.pos.dot
	neato -s -n2 -Tgtk < $<
%.png: %.pos.dot
	neato -s -n2 -Tpng < $< > $@
%.thumb.png: %.png
	convert -scale 618 $< $@
%.ps: %.pos.dot
	neato -s -n2 -Tps < $< > $@
%.a3.ps: %.ps
	poster $< -p a3 -m a3 -c5% -o $@
%.a2.ps: %.ps
	poster $< -p a2 -m a3 -c5% -o $@
%.a1.ps: %.ps
	poster $< -p a1 -m a3 -c5% -o $@
%.a0.ps: %.ps
	poster $< -p a0 -m a3 -c5% -o $@

%.pdf: %.ps
	ps2pdf $<

clean:
	rm -f *.png *.{pos,raw}.dot *.ps *.pdf
perm:
	find -user ${USER} -exec chmod g+w {} \;
_install: knp.thumb.png knp.a3.pdf
	cp knp.thumb.png /groups/kn/gossie/protected_html/snog.png
	cp knp.a3.pdf /groups/kn/gossie/protected_html/snog.pdf
install: _install perm

.PHONY:
