pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r ./requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/ --target=./venv/Lib/site-packages