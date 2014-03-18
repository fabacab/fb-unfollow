#!/bin/bash -

cd $(dirname "$0")

if [ $(pip; echo $?) -gt 0 ]; then
    curl -LO https://raw.github.com/pypa/pip/master/contrib/get-pip.py \
        && python get-pip.py --user \
            && rm -f get-pip.py
fi

# Add the appropriate PEP370 bin directory to $PATH.
PYTHON_VERSION=$(python --version 2>&1 | cut -d ' ' -f 2)
pipbin="$HOME/Library/Python/$PYTHON_VERSION/bin"
if [[ $PYTHON_VERSION =~ 2.6 ]]; then
    pipbin="$HOME/.local/bin"
fi
export PATH="$PATH:$pipbin"

pip install --user -r requirements.txt

echo -n 'Enter your Facebook username: '
read FB_USER
echo -n 'Enter your Facebook password: '
read -s FB_PASS
echo
echo "Unfollowing $FB_USER's Facebook friends..."
python ./unfollow_facebook_users.py $FB_USER $FB_PASS
