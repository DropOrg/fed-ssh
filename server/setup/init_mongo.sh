# start mongo
# mongod --shutdown (only for linux)
brew services stop mongodb
echo "Starting MongoDB. Please enter the administrator's password."
fedssh_port=41738
sudo mongod --port $fedssh_port

# set username/password
read -p "Enter your desired fed-ssh server username: " username
read -s -p "Enter your desired password: " password

# todo: for linux use sha256sum instead of shasum -a 256
hashed_pass=$(echo -n foobar | shasum -a 256)

#set USERNAME & PASSWORD ENVs, gen temp create_user file to inject into mongo shell
export FED_SSH_USERNAME=$username
export FED_SSH_PASSWORD=$hashed_pass
./get_user_env.sh > temp_create_user.js

#inject create user code -> mongo shell 
mongo localhost:$fedssh_port/fedssh temp_create_user.js
echo "Created USER: $FED_SSH_USERNAME"

# cleanup
unset FED_SSH_USERNAME
unset FED_SSH_PASSWORD
rm temp_create_user.js
