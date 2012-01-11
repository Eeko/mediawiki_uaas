# download and do the standard update to mediawiki 1.5
# may need to be run as superuser, depending on your access-rights
source configs.replica

cd ~/mw15_update/
svn co https://svn.wikimedia.org/svnroot/mediawiki/tags/REL1_5_0/phase3 $PWD/mwiki15
sudo mkdir /var/www/wiki15
sudo cp -r $PWD/mwiki15/* /var/www/wiki15/

#reconfigure apache
sudo service httpd stop
sudo sh -c 'echo "Alias /wiki15/ \"/var/www/wiki15/\"" >> /etc/httpd/conf/httpd.conf'
sudo sh -c 'echo "<Directory \"/var/www/wiki15\">" >> /etc/httpd/conf/httpd.conf'
sudo sh -c 'echo "    Order allow,deny" >> /etc/httpd/conf/httpd.conf'
sudo sh -c 'echo "    Allow from all" >> /etc/httpd/conf/httpd.conf'
sudo sh -c 'echo "    Options Indexes FollowSymLinks MultiViews" >> /etc/httpd/conf/httpd.conf'
sudo sh -c 'echo "</Directory>" >> /etc/httpd/conf/httpd.conf'

#copy the mwiki configuration file from 1.4
sudo cp /var/www/wiki14/LocalSettings.php /var/www/wiki15/LocalSettings.php
sudo sed -i 's/\/wiki14/\/wiki15/g' /var/www/wiki15/LocalSettings.php

#sudo cp /var/www/wiki15/AdminSettings.sample /var/www/wiki15/AdminSettings.php
#sudo sed -i "s/wikiadmin/$wikidb_adminusername/g" /var/www/wiki15/AdminSettings.php
#sudo sed -i "s/adminpass/$wikidb_adminpassword/g" /var/www/wiki15/AdminSettings.php

cd /var/www/wiki15/maintenance
sudo /usr/local/bin/php upgrade1_5.php	# on the test-computer, the sudoers default php is the newer 5.3, whilst the mediawiki 1.4 & 1.5 require php 5.2
sudo /usr/local/bin/php update.php	# run the schema updater

sudo service httpd start	# restart apache
echo "the mediawiki 1.5 should now be available at http://localhost/wiki15/index.php"
echo "Now you should start the cloning python script with \"python ~/mw15_update/update_mediawiki.py $local_log_cache\" "
