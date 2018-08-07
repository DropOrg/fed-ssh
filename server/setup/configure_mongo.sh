og_conf_path="/usr/local/etc/mongod.conf"
fed_ssh_conf_path="fed_ssh_mongo.conf"
cp -f $fed_ssh_conf_path $og_conf_path
mv usr/local/etc/$fed_ssh_conf_path $og_conf_path