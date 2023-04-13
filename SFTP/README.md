 
# Environment
- AXIS Device: Latest firmware 11.3.70 on AXIS P7316 Video Encoder
- EC2 SFTP Sever: EC2 Instance: Ubuntu Server 22.04 LTS (HVM), ami-007855ac798b5175e (64-bit (x86)) / ami-0c6c29c5125214c77 (64-bit (Arm)) with EBS gp2 storage, t2.micro in Unlimited mode to avoid risk of CPU throttling.

# SFTP Server Setup

- Followed https://qiita.com/alokrawat050/items/709d3c777407ab658aa9 exactly, using port 22 where it asks for a port number.
- extract the SHA fingerprint for the Axis device, so that is done with:

`sudo ssh-keygen -l -E sha256 -f ssh_host_ecdsa_key.pub`

# Axis Device Recipient Configuration

In System > Events > Recipients:

```
Port: 22
Folder: data/
Username: sftp_user
Password <password_set_above>
SSH host public key type: <sha256 obtained above>
Use temporary file name: <ticked>
```

# Video footage 

- Input capture was “ntsc 720x480 @ 30 fps” in the AXIS GUI. The image was largely a static image of a 3D printer (so low bitrate expected), but with the live clock burned into it (using AXIS firmware for this), creating some small variation between frames
- The video arriving at the server was `Stream #0:0(eng): Video: h264 (High), yuvj420p(pc, bt709/smpte170m/bt709, progressive), 704x480 [SAR 10:11 DAR 4:3], SAR 1:1 DAR 22:15, 30 fps, 30 tbr, 1k tbn, 50 tbc (default)` according to ffprobe

# Sending via SFTP

1. System > Events > Schedules > Add schedule > Pulse > Set 30 seconds interval
 
2. System > Rules > Add a rule >
Condition:  Pulse (use this condition as a trigger)
Action: Send video clip through FTPS
Create Folder: <empty>
Filename: video%y-%m-%d_%H-%M-%S-%f_#s.mkv
Stream profile: None
prebuffer: <integer>
postbuffer: <integer>

prebuffer and postbuffer can be adjusted as desired.

# Results

We tried 30 second interval pulse event with:
- 3 second pre buffer and 0 seconds post buffer ([./3pre-0post-30pulse.txt](./3pre-0post-30pulse.txt))
- 3 seconds pre buffer and 30 seconds post buffer ([./3pre-30post-30pulse.txt](./3pre-30post-30pulse.txt))
- 30 seconds pre buffer and 0 seconds post buffer ([./30pre-0post-30pulse.txt](./30pre-0post-30pulse.txt))

And all showed huge gaps (5 to 30 seconds) between each clip making this solution impractical for streaming video to the cloud securely.
