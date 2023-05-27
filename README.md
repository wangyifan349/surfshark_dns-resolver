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




最近发现了一种新的方法可以解决surfshark的dns污染问题,由于surfshark的更换ip地址非常频繁(最佳观察每个地区1天2次以上),所以几乎不存在被墙的可能性。

sudo echo -e "[Resolve]\nDNS=1.1.1.1\nDNSOverTLS=yes">/etc/systemd/resolved.conf

sudo systemctl restart systemd-resolved

sudo systemctl restart NetworkManager


Recently, a new method was found to solve the DNS pollution problem of Surfshark. Since Surfshark changes its IP address very frequently (it is best to observe each region more than twice a day), there is almost no possibility of being blocked.


on ubuntu ,you can use  tls over dns

Enter the following in the command line window

sudo echo -e "[Resolve]\nDNS=1.1.1.1\nDNSOverTLS=yes">/etc/systemd/resolved.conf

sudo systemctl restart systemd-resolved

sudo systemctl restart NetworkManager

dns over tls can solve the problem of dns pollution

In addition, you can buy a domain name and use the cname to point to the surfshark domain name to solve the pollution problem.

你需要找一个kill-switch脚本或者利用防火墙实现kill-switch。

注意，这种方法只能保证在debian等开源安全的系统保持隐私，在Windows下保持不了哦，Windows的遥感太多了。


