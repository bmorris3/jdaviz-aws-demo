
### EC2 Security group settings

Under "Firewall", choose "Create security group" and check
to allow SSH, HTTP and HTTPS. Plus, add a rule to your
security group for solara at:
```
Custom TCP port 8765 source 0.0.0.0/0
```

### EC2 User Data

```bash
curl -O https://raw.githubusercontent.com/bmorris3/jdaviz-aws-demo/refs/heads/main/setup
chmod 700 setup
sudo su
bash ./setup
```
