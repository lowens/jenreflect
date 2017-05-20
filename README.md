# jenreflect

This is a tool for mirroring the jenkins update center.
It downloads the update-center.json file to determine
the latest version of jenkins, then downloads and checks
the sha1 of the jenkins war file and all listed plugin
hpi files.  It avoids downloading files that already
exist and have the correct SHA1 hash.

Install for development from the root directory of the
project:

```bash
pip install -e .[dev]
```


