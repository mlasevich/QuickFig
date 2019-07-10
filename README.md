[![Build Status](https://travis-ci.org/mlasevich/QuickFig.svg?branch=master)](https://travis-ci.org/mlasevich/QuickFig)
[![Coverage Status](https://coveralls.io/repos/github/mlasevich/QuickFig/badge.svg?branch=master)](https://coveralls.io/github/mlasevich/QuickFig?branch=master)
[![PyPI version](https://badge.fury.io/py/QuickFig.svg)](https://badge.fury.io/py/QuickFig)

# QuickFig - Quick and Painless Config Parser for Python

A lightweight schema-supporting config parser for projects.


## QuickFig Release Notes

* 0.3.0
    * Add support setting parameters via environment variables
    * Fix bug causing issues finding definitions in section mode

* 0.2.0
    * Add support for Python 2.7

* 0.1.1
    * Initial version

## Quick Intro to QuickFig

QuickFig is a quick and easy to use library for configuring your application using a Yaml file.
QuickFig allows you to set up a loose schema with default values and data types that reduces error
checking and config processing code in your app.

I have written something like this for almost every project I have done and it always take longer
than it should, so I decided to write it as a library and share it.

### Features

* Set a loose schema for the configuration. While parameters do not require a schema defined, 
  it helps as it will take care of the conversion for it. 
    * ***Example Schema***:

            schema = {
                      'runtime.debug': {
                          'desc': "DEBUG Mode',
                          'type': 'bool', 
                          'default': 'false', 
                          'env': [ 'MYAPP_DEBUG', 'DEBUG']},
                      'myapp.float': {
                          'type': 'float', 
                          'default': 1.2},
                      'myapp.str': {
                          'type': 'str',
                          'default': "string value"}
            }
            
            config = QuickFig(definition=schema)

        The above defines parameter 'runtime.debug' which is a boolan that defaults to False
        if not defined, you can set it by setting env variables `MYAPP_DEBUG` or `DEBUG`, but if 
        both are set, value in `MYAPP_DEBUG` will win. It also defines "myapp.float" and `myapp.str`
        as a float and a string respectively

    * A Schema for a parameter can define:
        * `desc` - Description of the parameter
        * `type` - Parameter Type
            * Pre-Defined Data Types (Additional types may be added dynamically as needed):
                * `str` - Strings (default if not set)
                * `bool` - Boolean
                * `int` - Integer
                * `float` - Floating point
                * `list` - A List of values
                * `dict` - A key-value dictionary
        * `default` - Default value for parameter
        * `env` - Environment variable(s) that can be used if parameter is not set
            * If at least one env variable is set and parameter is not defined in the config file,
              the first environment variable that is defined will be used.
    * When Schema is not defined, QuickFig will take a best guest at parameter type based on
      current value.
* Read a YAML configuration file
    * The file format can be of any depth and may include parameters with or without a schema

    * ***Example:***
       (Using same schema)

        * *Config File: (config.yaml)*
                myapp:
                  str: My String
                  float: 9.2
        * *Code*:

                ## Env variable DEBUG is set to "yes"
                config = QuickFig(definition=schema)

                # No data yet, only schema default
                assert config.myapp.str == "string value"

                #Load config from file
                config.quickfig_load_from_file('config.yaml')

                # Data from config file:
                assert config.myapp.str == "My String"

                # Data From env variable DEBUG
                # Note that it got converted to a boolean from string
                assert config.runtime.debug == True

* Set parameter overrides at runtime that set the value regardless of env variables or values in
  config files. This is handy if you want to allow, for example, user to override a config file
  parameter from command line
    * ***Example:***

            #Note that value can be a string or a boolean
            overrides={'runtime.debug': 'yes'}
            config = QuickFig(definition=schema, overrides=overrides)

            assert config.runtime.debug = True

* Store all of this configuration in an object that allows:
    * Access to read/get any value using dotter notation:
        * ***Example:***

                config = QuickFig(definitions=schema)

                # No data yet, only schema default
                assert config.myapp.str == "string value"

                #set the value
                config.set("myapp.str", "new_value")

                # Get the value using dict-like get(key, default_value)
                assert config.get("myapp.str", "default_value") == "new_value"

    * Access parameters using property notation (setting this way is not supported):
        * ***Example:***

                config = QuickFig(definitions=schema)

                # create a sub-config for section `myapp`
                myapp_config = config.section('myapp')

                #set the value
                myapp_config.set("str", "new_value")

                # Get the value using full config object
                assert config.myapp.str == "new_value"

                # Get the value using full sub-config object
                assert myapp_config.str == "new_value"


    * Creation of a filtered sub-config object that allows access to child nodes without using
      full path:
        * ***Example:***

                config = QuickFig(definitions=schema)

                # No data yet, only schema default
                assert config.myapp.str == "string value"

                #set the value
                config.set("myapp.str", "new_value")

                # Get the value using property notation
                assert config.myapp.str == "new_value"



## Usage

### Concepts

Key concept in QuickFig is that while the config file can be netsted, it can always be flattended using 
the dotted notation - so that something like this:

        myapp:
            section_1:
               parameter: value
            section_2:
               parameter: another value

can also be represented as:

        myapp.section_1.parameter: value
        myapp.section_2.parameter: value

While the main config file can be in either format - the schema and overrides use the dotted notation

The goal is to make the config as seamless as possible to reduce validation and management code in 
your app.

### Examples:

#### Full Example:
(This example exists in examples directory)

* *Config file: (`full_example.conf`)*

       # Config file for full_example
        app:
          component1:
            enabled: true
            host: yahoo.com
          component2:
            enabled: false
            delay: 1.0

* *Code: (`full_example.py`)*

        #!/usr/bin/env python3
        """
        Full Example of using QuickFig
        """
        from argparse import ArgumentParser, Action, ArgumentError
        from argparse import RawDescriptionHelpFormatter
        import os
        import sys
        
        from quickfig import QuickFig
        import yaml
        
        __version__ = 1.0
        __updated__ = ""
        
        SCHEMA_YAML = '''
        debug:
          desc: General Debug Flag
          type: bool
          default: false
          env:
            - APP_DEBUG
            - DEBUG
        
        app.component1.enabled:
          desc: Component 1 Enabled Flag
          type: bool
          default: false
        
        app.component1.host:
          desc: Component 1 Hostname
          type: str
          default: google.com
        
        app.component1.port:
          desc: Component 1 Port Number
          type: int
          default: 443
        
        app.component2.enabled:
          desc: Component 2 Enabled Flag
          type: bool
          default: no
        
        app.component2.delay:
          desc: Delay in seconds for component 2 to startup
          type: float
          default: 0.5
        '''
        
        SCHEMA = yaml.safe_load(SCHEMA_YAML)
        
        
        class StoreNameValuePair(Action):
            ''' Action to store an section.option = value pair into the  '''
        
            def __call__(self, parser, namespace, values, option_string=None):
                for value in values:
                    try:
                        (key, value) = value.split("=", 2)
                    except ValueError:
                        raise ArgumentError(self,
                                            "Could not parse argument %s as section.option=value format" % value)
                    config = getattr(namespace, self.dest) or {}
                    config[key] = value
                    setattr(namespace, self.dest, config)
        
        
        def sep(text=""):
            ''' Print a separator '''
            print('{:^60}'.format("-" * 60))
            print('---- {:^50} ----'.format(text))
            print('{:^60}'.format("-" * 60))
        
        
        def component1(config, debug):
            ''' Run component 1 '''
            print("Starting component 1")
            print("Connecting to: %s:%s" % (config.host, config.port))
            if debug:
                print("Component 1 Config:\n%s" % config)
        
        
        def component2(config, debug):
            ''' Run component 2 '''
            print("Starting component 2")
            print("Delay is: %s" % config.delay)
            if debug:
                print("Component 2 Config:\n%s" % config)
        
        
        def run():
            program_version = "v%s" % __version__
            program_build_date = str(__updated__)
            program_version_message = '%%(prog)s %s (%s)' % (
                program_version, program_build_date)
        
            parser = ArgumentParser()
            parser.add_argument("-D", dest="debug", action="store_true",
                                help="set debug mode [default: %(default)s]")
        
            parser.add_argument("-P", dest="options", metavar="option=value",
                                action=StoreNameValuePair, nargs="+",
                                help="Override config parameters, use option=value syntax")
        
            parser.add_argument('-V', '--version', action='version',
                                version=program_version_message)
        
            # Process arguments
            args = parser.parse_args()
        
            # Determine overrides based on cli args
            overrides = {}
            if args.options:
                overrides.update(args.options)
            if args.debug:
                overrides['debug'] = True
        
            # Create our config
            config = QuickFig(definitions=SCHEMA, overrides=overrides)
        
            # load the config
            config.quickfig_load_from_file("full_example.conf")
            sep("Starting...")
        
            print("Debug Mode is: %s" % ("on" if config.debug else "off"))
        
            if config.debug:
                print("Total Config: \n%s" % config)
        
            # run component1 if enabled
            if config.app.component1.enabled:
                sep("Component 1")
                # Run component 1 and give it only the config it needs
                component1(config.section('app.component1'), config.debug)
        
            # run component2 if enabled
            if config.app.component2.enabled:
                sep("Component 2")
                # Run component 1 and give it only the config it needs
                component2(config.section('app.component2'), config.debug)
            sep("Finished")
        
        
        if __name__ == "__main__":
            run()

* Sample Runs:

    * Basic (no arguments)

            ./full_example.py
            ------------------------------------------------------------
            ----                    Starting...                     ----
            ------------------------------------------------------------
            Debug Mode is: off
            ------------------------------------------------------------
            ----                    Component 1                     ----
            ------------------------------------------------------------
            Starting component 1
            Connecting to: yahoo.com:443
            ------------------------------------------------------------
            ----                      Finished                      ----
            ------------------------------------------------------------

       As per config, debug is off, component 1 is enabled, component 2 is not

    * Override component 2 enable from command line (`-P app.component2.enabled=yes`) 

            ./full_example.py -P app.component2.enabled=yes
            ------------------------------------------------------------
            ----                    Starting...                     ----
            ------------------------------------------------------------
            Debug Mode is: off
            ------------------------------------------------------------
            ----                    Component 1                     ----
            ------------------------------------------------------------
            Starting component 1
            Connecting to: yahoo.com:443
            ------------------------------------------------------------
            ----                    Component 2                     ----
            ------------------------------------------------------------
            Starting component 2
            Delay is: 1.0
            ------------------------------------------------------------
            ----                      Finished                      ----
            ------------------------------------------------------------

     * Enable Debug Mode (`-D`) 

            ./full_example.py -D | sed "s/^/            /"
            ------------------------------------------------------------
            ----                    Starting...                     ----
            ------------------------------------------------------------
            Debug Mode is: on
            Total Config: 
            #QuickFig Config
            
            # Component 1 Enabled Flag (Default: 'False')
            app.component1.enabled = True
            
            # Component 1 Hostname (Default: 'google.com')
            app.component1.host = yahoo.com
            
            # Component 1 Port Number (Default: '443')
            app.component1.port = 443
            
            # Delay in seconds for component 2 to startup (Default: '0.5')
            app.component2.delay = 1.0
            
            # Component 2 Enabled Flag (Default: 'False')
            app.component2.enabled = False
            
            # General Debug Flag (Default: 'False')
            debug = True
            
            #End QuickFig Config
            
            ------------------------------------------------------------
            ----                    Component 1                     ----
            ------------------------------------------------------------
            Starting component 1
            Connecting to: yahoo.com:443
            Component 1 Config:
            #QuickFig Config
            #
            # Path: app.component1
            #
            
            # Component 1 Enabled Flag (Default: 'False')
            enabled = True
            
            # Component 1 Hostname (Default: 'google.com')
            host = yahoo.com
            
            # Component 1 Port Number (Default: '443')
            port = 443
            
            #End QuickFig Config
            
            ------------------------------------------------------------
            ----                      Finished                      ----
            ------------------------------------------------------------

        * Enable debug mode via env variable

                ------------------------------------------------------------
                ----                    Starting...                     ----
                ------------------------------------------------------------
                Debug Mode is: on
                Total Config: 
                #QuickFig Config
                
                # Component 1 Enabled Flag (Default: 'False')
                app.component1.enabled = True
                
                # Component 1 Hostname (Default: 'google.com')
                app.component1.host = yahoo.com
                
                # Component 1 Port Number (Default: '443')
                app.component1.port = 443
                
                # Delay in seconds for component 2 to startup (Default: '0.5')
                app.component2.delay = 1.0
                
                # Component 2 Enabled Flag (Default: 'False')
                app.component2.enabled = False
                
                # General Debug Flag (Default: 'False')
                debug = True
                
                #End QuickFig Config
                
                ------------------------------------------------------------
                ----                    Component 1                     ----
                ------------------------------------------------------------
                Starting component 1
                Connecting to: yahoo.com:443
                Component 1 Config:
                #QuickFig Config
                #
                # Path: app.component1
                #
                
                # Component 1 Enabled Flag (Default: 'False')
                enabled = True
                
                # Component 1 Hostname (Default: 'google.com')
                host = yahoo.com
                
                # Component 1 Port Number (Default: '443')
                port = 443
                
                #End QuickFig Config
                
                ------------------------------------------------------------
                ----                      Finished                      ----
                ------------------------------------------------------------

### API:

#### Main Class: *QuickFig()*

This is the main class when using QuickFig.

##### *QuickFig()* Constructor
- Keyword arguments:
    - **definitions** - schema as a dictionary
        - **definitions** should be flat(dotted notation) dictionary of key to definition dict
    - **config** - config as a python dictionary object
        - Dictionary may be nested or flat using dots
    - **overrides** - overrides as a dictionary object
        - **overrides** should be flat dictionary of key to value
    - **resolver** - an optional instance of class `ConfDataTypeResolver()`. 
        - If not specified, uses default resolver.
        - Main reason to specify is to add custom type resolution 
          without affecting default resolver

  
##### *QuickFig()* Instance Methods

- `quickfig_load(config)` - load configuration provided by parameter `config`

- `quickfig_load_from_file(filename, warn=False)` - load configuration from file whose name is
  provided  by `filename` parameter. If `warn` is true, throw a warning into the log if file not
  present or cannot read. 
- `section(name)` - get a filtered version of the config with `name` as prefix. Returns instance
  of `QuickFigNode()` class
- `set(key, value)` - set parameter specified by `key` to `value`. `key` is a dotted notation
  representation of a parameter name.
- `get(key, default_value=None)` - get parameter specified by `key`(dotted notation). if not set,
   return
  `default_value`, if specified. Note, default value specified by schema will have priority over
  `default_value`
- `get_data_type(key, test_value="")` - get data type for parameter specified by `key`. If parameter is 
  not set and has no schema, use value of `test_value` to guess at the data type. Returns object of 
  class `QuickFigDataType()`
- `get_definition(key, test_value="", default_dtype=None)) - get definition for parameter specified
  by `key`. Use `test_value` to guess at data type if no definition exists and parameter is not set.
  if `default_dtype` is specified, use that data type instead of guessing.


### Class: *QuickFigNode()*

This class appears similar to QuickFig, but is not instanciated directly. Instead it is created via 
`section(name)` method on either `QuickFig()` or `QuickFigNode()` instances)

##### *QuickFigNode()* Instance Methods

- `section(name)` - get a filtered version of the config with `name` as prefix. `name` is combined
  with current prefix, if one is already defined. Returns an instance of  `QuickFigNode()` class
- `set(key, value)` - set parameter specified by `key` to `value`. `key` is a dotted notation
  representation of a parameter name.
- `get(key, default_value=None)` - get parameter specified by `key`(dotted notation). if not set,
   return
  `default_value`, if specified. Note, default value specified by schema will have priority over
  `default_value`
- `get_data_type(key, test_value="")` - get data type for parameter specified by `key`. If parameter is 
  not set and has no schema, use value of `test_value` to guess at the data type. Returns object of 
  class `QuickFigDataType()`
- `get_definition(key, test_value="", default_dtype=None)) - get definition for parameter specified
  by `key`. Use `test_value` to guess at data type if no definition exists and parameter is not set.
  if `default_dtype` is specified, use that data type instead of guessing.


