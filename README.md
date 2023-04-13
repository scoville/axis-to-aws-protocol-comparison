Axis provide some best practices for recording here: https://help.axis.com/en-us/axis-os#edge-storage-support

> When configuring your recordings, add at least 30 seconds of post-buffer recording to each event triggered recording in order to avoid many small recording segments

> Configure the Axis device properly with the correct date & time prior to starting a recording. Date & time can either be configured manually or automatically via the NTP server.


Axis document their natively supported protocols here: https://help.axis.com/en-us/axis-os#edge-storage-support

As discussed in our blog, we compared FTP, SFTP, SMB (2.0/3.0), HTTPS, RTSP and the Kvstreamer ACAP to assess ability to provide an uninterupted cloud stream.

Kvstreamer ACAP was the only option to provide an uninterupted stream. 
