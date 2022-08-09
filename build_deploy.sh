rm -r dist ;
python setup.py sdist bdist_wheel ;
if twine check dist/* ; then
  if [ "$1" = "--test" ] ; then
    python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
  else
    python3 -m twine upload dist/* ;
  fi
fi