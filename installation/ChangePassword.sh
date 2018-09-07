#!/usr/bin/expect
# -*- coding: utf-8 -*-
#

set timeout 5
set OLDPASSWORD "raspberry"
set NEWPASSWORD "pibs"

# change password to super-secret combination
spawn passwd
expect "(current) UNIX password: " 
send "$OLDPASSWORD\r"
expect "Enter new UNIX password: "
send "$NEWPASSWORD\r"
expect "Retype new UNIX password: "
send "$NEWPASSWORD\r"
interact

