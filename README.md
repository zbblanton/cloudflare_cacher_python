# Cloudflare Cacher (Written in Python)

## Description
A script that can run as a cron job to keep your website cached in cloudflare. This script will scan the specified folder and cache anything new or older than X amount of days.  

## Requirements
* Cloudflare account
* Python >= 2.7.12

## Example
Will add example soon...

Linux:
```
crontab -e
```

Then add something like this to the crontab:
```
* * * * * python cloudflare_cacher.py
```
