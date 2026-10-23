python -m compileall .
python -c "from sidgeo.view.aplicativo_tela import AplicativoVisual; print('OK')"



python testebuild.py > resultado-build.txt 2>&1


pylint sidgeo -enable=F,E --disable=R,C,I,W  --output-format=text  >> resultado-build.txt 2>&1

rem pyright . --level error  >> resultado-build.txt 2>&1