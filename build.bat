pandoc -s -w rst README.md -o README.txt
python setup.py sdist bdist_wininst register upload