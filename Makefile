all: dudeney.gif

dudeney.gif: dudeney.py
	python dudeney.py
	convert -delay 5 `seq -f out%02g.png 1 48` `seq -f out%02g.png 47 1` -coalesce dudeney.gif

