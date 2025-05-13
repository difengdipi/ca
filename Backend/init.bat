@REM python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

@REM pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

@REM pip install -r requirements.txt

python manage.py makemigrations App
python manage.py migrate

python manage.py runserver

@REM python manage.py createsuperuser --username=admin --email=123456@qq.com
