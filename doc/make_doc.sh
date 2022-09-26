rm -f source/sdxml.*.rst
mkdir -p source/_static source/_templates
sphinx-apidoc -M -f -n -o source ../xmlcoll
make html
