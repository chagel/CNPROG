SITE_SRC_ROOT = '~/dev/workspace/cnprog'

#for logging
import logging
LOG_FILENAME = 'development.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


#Database configuration 
DATABASE_ENGINE = 'mysql'      
DATABASE_HOST = ''            
DATABASE_PORT = ''          
DATABASE_NAME = 'twogeekt_lanai'             # Or path to database file if using sqlite3.
DATABASE_USER = 'twogeekt_lanai'             # Not used with sqlite3.
DATABASE_PASSWORD = 'sysadm'                # Not used with sqlite3.


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '~/dev/workspace/cnprog/templates/upfiles/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8000/upfiles/'
