[![bugsplat-github-banner-basic-outline](https://user-images.githubusercontent.com/20464226/149019306-3186103c-5315-4dad-a499-4fd1df408475.png)](https://bugsplat.com)
<br/>
# <div align="center">BugSplat</div> 
### **<div align="center">Crash and error reporting built for busy developers.</div>**
<div align="center">
    <a href="https://twitter.com/BugSplatCo">
        <img alt="Follow @bugsplatco on Twitter" src="https://img.shields.io/twitter/follow/bugsplatco?label=Follow%20BugSplat&style=social">
    </a>
    <a href="https://discord.gg/K4KjjRV5ve">
        <img alt="Join BugSplat on Discord" src="https://img.shields.io/discord/664965194799251487?label=Join%20Discord&logo=Discord&style=social">
    </a>
</div>

## Python Crash Upload

If you'd like to bulk upload minidump files, clone this repo:

```bash
git clone https://github.com/BugSplat-Git/python-crash-upload
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Invoke `upload.py` as follows, being sure to replace database, application, version, and file.dmp with values specific to your [BugSplat](https://bugsplat.com) configuration:

```bash
python upload.py database application version ./file.dmp
```

Thanks for using BugSplat ❤️