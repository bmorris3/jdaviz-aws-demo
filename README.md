
### EC2 Security group settings

Under "Firewall", choose "Create security group" and check
"Allow HTTP traffic from the internet". Otherwise, add rules to your
security group for:

```
HTTP port 80 source 0.0.0.0/0
HTTPS port 443 0.0.0.0/0
SSH port 22 source 0.0.0.0/0
Custom TCP port 8765 source 0.0.0.0/0
```

### EC2 User Data

```bash
curl -O https://raw.githubusercontent.com/bmorris3/jdaviz-aws-demo/refs/heads/main/setup
chmod 700 setup
sudo su
bash ./setup
```
