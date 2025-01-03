sudo su
systemctl start nginx.service
cd /home/ec2-user/
source venv/bin/activate
SOLARA_APP=app.py uvicorn --workers 2 --host 0.0.0.0 --port 8765 solara.server.starlette:app
