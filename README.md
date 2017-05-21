# jenreflect

This is a tool for mirroring the jenkins update center.
It downloads the update-center.json file to determine
the latest version of jenkins, then downloads and checks
the sha1 of the jenkins war file and all listed plugin
hpi files.  It avoids downloading files that already
exist and have the correct SHA1 hash.

## Quick Start
```bash
cd sandbox
git clone https://github.com/lowens/jenreflect.git
cd jenreflect
pyvenv venv
. venv/bin/activate
pip install -e .[dev]
jenreflect
```

The default options will produce a jenkins-mirror
subdirectory containing update-center.json,
jenkins-<version>.war, and a subdirectory
structure of <plugin name>/<version>/<plugin.hpi>
for all plugins.
