CTF PwningChallenge Deployer
===

## [Chinese(Traditional) version](README-zhtw.md)

### Project Structure (Place your file with this structure :))
```
.
├── README.md
├── activator.py
├── chal
│   └── return
│       ├── flag
│       └── return
└── deactivator.py
```

### Setup
Place your challenge in `chal/`, and create a folder with the same challenge name.

e.g.:
```
|-chal
│   └── return
│       ├── flag
│       └── return
```

### Usage:
```
git clone https://github.com/racterub/ctf-pwn-deployer
cd ctf-pwn-deployer/
python activator.py <PORT> <IMAGE VERSION> <TIMEOUT> # Create and Running container      // port will increase its value depends on the amount of your challenge 
                                                                                        // TIMEOUT is optional (set 0 to cancel timeout)


python deactivator.py # Stop and Delete container
```
