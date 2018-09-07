#!/bin/bash
# Tells local git repository that a remote repository exists

# name of repository
REPO=pibs_client

if [ "$#" == 1 ]
then
	REPO=$1
fi

echo "-> Setting up remotes at fmnc and bitbucket"
cd /home/pi/$REPO; git remote add fmnc git@fmnc.cse.nd.edu:/home/git/$REPO.git
cd /home/pi/$REPO; git remote add cloud https://bitbucket.org/ndwireless/$REPO.git

echo "-> Created Remotes: fmnc, cloud ... Complete ..."
exit 0;
