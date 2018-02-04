<VirtualHost *:80>

  ServerName localhost

  LogLevel alert rewrite:trace3

  DocumentRoot %TRAVIS_BUILD_DIR%/docroot
  DirectoryIndex index.php

  <Directory "%TRAVIS_BUILD_DIR%/docroot">
        Options -Indexes +FollowSymLinks +MultiViews
        AllowOverride All
        Require all granted
  </Directory>

  <FilesMatch \.php$>
        # Else we can just use a tcp socket:
        SetHandler "proxy:fcgi://127.0.0.1:9000"
  </FilesMatch>

</VirtualHost>
