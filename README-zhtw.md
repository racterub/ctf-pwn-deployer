Pwning CTF Challenge Deployer
===

Deployer 架構(須依照架構使用)
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
請將 Binary 放在 `chal/`內，並建立一個同名的資料夾
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
cd ctf-pwn-deployer
python activator.py <PORT> <IMAGE VERSION> <TIMEOUT> #建立並啟動 container      // port 依據 challenge 數量遞增
                                                                              // TIMEOUT 可選 (0 為取消 timeout)


python deactivator.py #停止並刪除 container
```
