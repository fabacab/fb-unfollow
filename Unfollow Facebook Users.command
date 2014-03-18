#!/bin/bash -

cd $(dirname "$0")

if [ $(pip; echo $?) -gt 0 ]; then
    curl -LO https://raw.github.com/pypa/pip/master/contrib/get-pip.py \
        && python get-pip.py \
            && rm -f get-pip.py
fi

pip install -r requirements.txt

echo -n 'Enter your Facebook username: '
read FB_USER
echo -n 'Enter your Facebook password: '
read -s FB_PASS
echo
echo "Unfollowing $FB_USER's Facebook friends..."
python ./unfollow_facebook_users.py $FB_USER $FB_PASS
