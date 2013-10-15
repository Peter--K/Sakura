# -*- coding: utf-8 -*-

import os
import ast
import cfgparse


class Config(object):
    def __init__(self):
        self.parser = cfgparse.ConfigParser()
        cfgfile = self.get_configpath()
        self.cfgfile = cfgfile
        try:
            open(cfgfile)
        except:
            # config file not found - create it
            path = os.path.dirname(cfgfile)
            try: 
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise
            with open(cfgfile, 'w') as f:
                print >>f, '[paths]'
                print >>f, 'default_dir = ' + os.path.expanduser('~')   # Default to home
        self.f = self.parser.add_file(cfgfile)

    def get_configpath(self):
        if 'APPDATA' in os.environ:
            confighome = os.environ['APPDATA']
        elif 'XDG_CONFIG_HOME' in os.environ:
            confighome = os.environ['XDG_CONFIG_HOME']
        else:
            confighome = os.environ['HOME']
        configpath = os.path.join(confighome, '.sakura', 'config.ini')
        return configpath

    def read_item(self, group, item):
        """Read the item.

        Keyword arguments:
        group - e.g. 'paths' refers to [paths]
        item - e.g. 'save_path'
    
        Returns:
        Item value parsed using the Python ast evaluator

        """
        option = self.parser.add_option(item, keys=group, type='string')
        val = option.get()
        try:
            val = ast.literal_eval(val)
        except (ValueError, SyntaxError):
            pass
        return val

    def write_item(self, group, item, value, item_type='string'):
        """Write the self.config dict to the self.filename ini file
        
        Arguments:
        group - e.g. 'paths' refers to [paths]
        item - e.g. 'save_path'
        value - e.g. r'C:\foo\bar\baz.ini'
        item_type - e.g. 'string' (default), 'int'
               for types see http://cfgparse.sourceforge.net/cfgparse-option-type.html

        """
        option = self.parser.add_option(item, keys=group, type=item_type)
        option.set(value)
        self.f.write(self.cfgfile)
