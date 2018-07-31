mkdir /usr/local/pemstore/certs/$1
cd /usr/local/pemstore/certs/$1

GEN_KEY="ssh-keygen -f $1 -t rsa -b 4096";
EMPTY_PASS="";
(echo $EMPTY_PASS; echo $EMPTY_PASS;) | eval $GEN_KEY;
