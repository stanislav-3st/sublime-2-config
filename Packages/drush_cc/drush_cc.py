import sublime
import sublime_plugin
from subprocess import call

class DrushccCommand(sublime_plugin.WindowCommand):
    def run(self):      
        call(["/Users/st/bin/drush -r /Users/st/Sites/www/versatel_de cc css+js"], shell=True)
