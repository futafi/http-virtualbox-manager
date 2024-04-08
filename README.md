# http-virtualbox-manager


VirtualboxのVMを[UpSnap](https://github.com/seriousm4x/UpSnap)で実際のPCのように管理したかった。


## how to use
### on host
```
$ pip install flask
$ python server.py
```
### on upsnap
- IP
    - hostのIP
- MAC
    - Virtualboxに適当に割り当てたMAC
- Netmask
    - 適当に
- Ping
    - curl -f $HOSTIP:5000/status/$MACADDR
- Wake
    - curl -f $HOSTIP:5000/start/$MACADDR
- Shutdown
    - curl -f $HOSTIP:5000/pause/$MACADDR


## 今後の予定
- manage\_vm.pyのreturnの値を適当に書きすぎたので修正する
- Sleep On Lanへとの互換機能
- socketを読んでWOLパケットでの起動をする機能の追加
- dockerとかにする？(多分しない)
