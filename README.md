
## EC2 Configuration

### Security group settings

Under "Firewall", choose "Create security group" and check
to allow SSH, HTTP and HTTPS. Plus, add a rule to your
security group for solara at:
```
Custom TCP port 8765 source 0.0.0.0/0
```

### User Data

```bash
curl -O https://raw.githubusercontent.com/bmorris3/jdaviz-aws-demo/refs/heads/main/setup
chmod 700 setup
sudo su
bash ./setup
```


## Usage

If the public IP address of your EC2 instance is `10.0.0.0`, visit `http://10.0.0.0:8765` to see
the running app. It may take ~2 minutes to become available.
