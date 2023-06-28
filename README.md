Dislaimer: This repository is not affiliated with, endorsed by, or otherwise connected to AWS or AXIS.

# Comparing supported protocols on AXIS devices to send video streams over the network to AWS 

As discussed in our [blog](https://benjamin-lowe.medium.com/how-best-to-stream-video-to-the-cloud-using-axis-devices-463a7f2e00c6), we compared FTP, SFTP, SMB (2.0/3.0), HTTPS, RTSP and the Kvstreamer ACAP to assess ability to provide an uninterupted cloud stream.

The summary of results can be found here:

- **HTTPS** - occasionally dropped clips 
- **SFTP** - occasionally dropped clips regardless of region
- **SMB** - occasionally dropped clips when the server was in a different region, when in same region did not drop clips but had small gaps between clips

[Kvstreamer](https://kvstreamer.scoville.jp/) - no dropped video footage, resilience to brief network outages 

- Not presented here is **FTP** and **HTTP** as these protocols are insecure.

**Kvstreamer was the only option to provide a reliable, secure and uninterrupted stream.** 

## Axis Documentation on Recording on the device 

Axis document their natively supported protocols here: https://help.axis.com/en-us/axis-os#network-protocols

Axis provide some best practices for recording here: https://help.axis.com/en-us/axis-os#edge-storage-support

> When configuring your recordings, add at least 30 seconds of post-buffer recording to each event triggered recording in order to avoid many small recording segments

> Configure the Axis device properly with the correct date & time prior to starting a recording. Date & time can either be configured manually or automatically via the NTP server.
