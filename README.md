surfshark是一个不错的VPN,但是在中国因为DNS污染无法正确解析和连接。

因此写一个脚本来处理DNS问题。

python3写的,可以将域名*.surfshark.com解析到正确的ip从而解决连接问题。

surfshark is a good VPN, but cannot resolve and connect properly in China due to DNS pollution.

So write a script to deal with DNS issues.

Written in python3, it can resolve the domain name *.surfshark.com to the correct ip to solve the connection question.

in  China,you can use this url:

my.surfshark.com

my.shark-china.com

my.shark-chinaz.com

my.sharkchinaz.com

my.shark-in-china.com

my.shark-in-chinaz.com

my.sharky-china.com

sudo echo -e "[Resolve]\nDNS=1.1.1.1\nDNSOverTLS=yes">/etc/systemd/resolved.conf

或者

sudo sh -c 'echo -e "[Resolve]\nDNS=1.1.1.1 2606:4700:4700::1111\nFallbackDNS=1.0.0.1 2606:4700:4700::1001\nDNSOverTLS=yes" > /etc/systemd/resolved.conf'

sudo systemctl restart systemd-resolved


sudo ufw allow out to 1.1.1.1 port 853 proto tcp

sudo ufw allow out to 1.1.1.1 port 443 proto tcp

on ubuntu ,you can use  tls over dns

Enter the following in the command line window

sudo echo -e "[Resolve]\nDNS=1.1.1.1\nDNSOverTLS=yes">/etc/systemd/resolved.conf

or   

sudo sh -c 'echo -e "[Resolve]\nDNS=1.1.1.1 2606:4700:4700::1111\nFallbackDNS=1.0.0.1 2606:4700:4700::1001\nDNSOverTLS=yes" > /etc/systemd/resolved.conf'


sudo systemctl restart systemd-resolved


dns over tls can solve the problem of dns pollution

In addition, you can buy a domain name and use the cname to point to the surfshark domain name to solve the pollution problem.

你需要找一个kill-switch脚本或者利用防火墙实现kill-switch，最好kill-switch脚本在kill-switch之后自动连接ovpn文件，去让chatgpt给你写吧。

另外surfshark的vpn经常被阻断，可以考虑使用普通的机场，几块钱的即可，然后接入洋葱网络，再开一个v2ray我们称之为代理2吧，(注意使用另外的代理端口)，这个连接socket5到洋葱的端口上，最后系统设置代理2的v2ray代理，加入广告屏蔽规则。洋葱虽然匿名性非常好很好，但是严重牺牲速度。我已经就好多机场记录啦，不要相信没有记录这种鬼话。
