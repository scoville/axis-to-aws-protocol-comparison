# Environment
- AXIS Device: 9.25.1.5 on AXIS P7304 Video Encoder
- AWS EC2 SFTP Sever: EC2 Instance: Ubuntu Server 22.04 LTS (HVM), ami-007855ac798b5175e (64-bit (x86)) / ami-0c6c29c5125214c77 (64-bit (Arm)) with EBS gp2 storage, `g4dn` and `m5.xlarge` 
- We based the EC2 instance in another region (us-east-1) to the device (ap-northeast-1) for two reasons:
  - To simulate non-ideal networking conditions (high latency), as a reliable streaming method requires robustness to momentary network issues and high latency connections. We also tried in the same region (see results)
  - us-east-1 is typically the cheapest region for EC2 instances, so is often a desirable choice


# Samba Server Setup

```bash
sudo apt-get update -y
sudo apt install samba -y
```

```bash
#backup config
sudo mv /etc/samba/smb.conf /etc/samba/smb.conf.bak
#create new config file
sudo vi /etc/samba/smb.conf
```

Content of smb.conf file:
```
[global]
workgroup = WORKGROUP
server string = My Samba Server
netbios name = ubuntu
security = user
map to guest = bad user
dns proxy = no

#===START TO SHARE FILE 
[PublicShare]
path = /samba/publicshare
browsable = yes
writable = yes
guest ok = yes
read only = no
```

Check the samba server status:

```
sudo systemctl status smbd
sudo smbstatus # shows the protocol being used, and any files coming in
```

Create a shared folder:

```
#create share folder
sudo mkdir -p /samba/publicshare/

#change permission
sudo chmod -R -0755 /samba/publicshare/

#change group for share folder
sudo chgrp sambashare /samba

#add sambauser in sambashare group 
sudo useradd -M -G sambashare sambauser

#set password for this user
sudo smbpasswd -a sambauser

#change owner for share folder
sudo chown sambauser:sambashare /samba/publicshare/

#change permission
sudo chmod 2770 /samba/publicshare/
```

Restart the server:

```
sudo service smbd stop
sudo service smbd start
```

- Set the EC2 Security Group to allow 445 and 139 TCP incoming connections. 

# Axis Device Recipient Configuration

In System > Events > Recipients:

```
Type: Network Storage
Host: <public ip address of EC2 instance>
Folder: <arbitrary string which is the name of the subfolder that the data will be placed in e.g. data>
Username: sambauser
Password <password_set_above>
```

# Sending via SMB

1. System > Events > Schedules > Add schedule > Pulse > Set X seconds interval
 
2. System > Rules > Add a rule >
Condition:  Pulse (use this condition as a trigger)
Action: Send video clip to network storage
Create Folder: <arbitrary folder name>
Filename: video%y-%m-%d_%H-%M-%S-%f_#s.mkv
prebuffer: <integer>
postbuffer: <integer>

prebuffer and postbuffer can be adjusted as desired.


# Port issues 

Some ISPs block port 445 used by Samba. We found we needed to set our SMB server to non-default port in /etc/samba/smbd.conf by adding `smb ports = 2222` to global section, restartign the server `sudo service smbd stop` `sudo service smbd start`, then opening this port in the EC2 incoming connections. Then from the AXIS device one needs to moutn the storage, when it fails, we need to enable SSH, login to device, and `sed -i 's/Port = 0/Port = 2222/' /etc/dynamic/networkshare.conf` and finally on the AXIS device it should be able to connect.

On the latest firmware 11.3.70 on AXIS P7316 Video Encoder this method no longer seems to work to set a non default port.

# Debugging

You can connect to your SMB server locally on Ubuntu to check it is working: 

`smbclient -p <port> //<server_ip>/publicshare -U WORKGROUP/sambauser `

# Results


- Axis devices allow you to send data to a Samba server in two ways. We found the "Events > Recipients > network storage recipient" was more reliable than the "Storage > Mount Network Storage" approach, which tended to lose entire clips.

15 second pulse with 15 second post buffer 0 second prebuffer resulted in and `m5.xlarge`:

- In same region as the device (ap-northeast-1):
    - 30s clips with around 0.15s gap with some occasional 0.4s gap 
- EC2 server in different region (us-east-1) as the device (ap-northeast-1):
   - Typically around 1 second of video lost between clips but occasionally an entire clip was lost

**We concluded this was not a reliable way to stream video to the cloud.**
