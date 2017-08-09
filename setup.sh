#!/usr/bin/env bash
current_dir=$(cd $(dirname $0);pwd)
cd ${current_dir}
python setup.py sdist
sudo python setup.py install
# python setup.py register
# python setup.py sdist upload
