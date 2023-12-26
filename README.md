> [!WARNING]  
> This library is unmaintained. Integrating Hotwire and Django is so easy
> that you are probably better served by writing a little bit of Python in your code
> than using a full-blown library that adds another level of abstraction.
> It also seems that the Django community is leaning more towards HTMX than Hotwire
> so you might want to look over there if you want more "support"
> (but we still think that Hotwire is very well suited to be used with Django)

# Stimulus and Webpack Tools for Django

Make the usage of stimulus and webpack in Django fun (again)! 

## Introduction

This module comes with two django management commands to help
with the setup as well as the execution of stimulus / webpack in django
by using the well-known _convention over configuration_ approach.

## Getting started

### Setup

First, you need a Django project. If you dont already have an app, create a new one.
E.g. using

```
python manage.py startapp demo apps/demo
```

and add it as `apps.demo` in your settings.

### Installation

Next, install the `webpack-tools` module in your python runtime, e.g. using 

```
pip install webpack-tools 
```

or via your `requirements.txt`.

Add `'webpack_tools'` to your `INSTALLED_APPS` in your `settings``

### Install Webpack

To prepare your project (not just your app!) for the usage of webpack (and npm if not already done) just type

```
python manage.py webpack --init-full
```

This will

* initialise npm (if no `package.json` is found)
* create a default `webpack.config.js` (if none exists)
* install all necessary npm packages for the execution of the webpack config

After that, you can always execute webpack simply by typing

```
python manage.py webpack --build
```

Note: Both commands can also be combined.

## Create Stimulus Controllers (and View Templates)

Sadly, we have nothing to pack yet.
So its time to create a Stimulus controller and integrate it in a view template.

Therefore, we have the `python manage.py stimulus` command.

To install one (or more) Controllers in your app, just execute

```
python manage.py stimulus {app.name} {controller1} .. {controllerN}
```

where {app.name} refers to the name of your app, as installed in your `settings`.
You can give zero or more controllers to be created. Those should be named all lower with no special characters!

The plugin will then

* Create a folder `/javascript` in your app root folder (if it doesnt already exist).
* Create an `application.js` with sensible defaults (auto detection of controllers during webpack execution) if it doesnt exist.
* Create a subfolder `/controllers` (if it doestn exist)
* Create a stub for each controller named `{controller}_controller.js` (the default convention, in stimulus).

Optionally, you can also create one (or more) view template which has the proper setup to get started even quicker.
For that, just append `--templates {template1} .. {templateN}` to the command above, i.e.

```
python manage.py stimulus {app.name} {controller1} .. {controllerN} --templates {template1} .. {templateN}
```

This will then create the respective templates in your apps `/template` folder and create ready to use templates.

## Bundling with webpack

Now its the right time to come back to `webpack`s `--bundle` command.
So just execute

```
python manage.py webpack --bundle
```

to get your Entrypoint (the `application.js` created above) with all controllers available.
Those will be bundled in a single `application.js` file which will be copied to `static/js/application.js` where it can be imported in your templates (see the auto generated templates for the exact syntax).

## Final words

Now, just take the stub template, integrate it in a view, wire up an url and... boom, your stimulus controllers are up and running, and ready to use.

Note: After changes in your controllers, dont forget to call `python manage.py webpack --bundle` to recreate the bundled asset.

# Installing Controllers from other Apps

When you have a modular structure in your modules (or even install third-party modules) you may come accross the case where you want to
include controllers from other modules into your entrypoint (`application.js`).
There are two approaches. One is that the other modules provide npm packages and the other is to use relative imports to specify the path of the controllers js-file relative to your entrypoint.

The `install_controller` helps you in the second case and does all necessary changes in your `application.js` file.
If one app defines a Controller (from the structure defines above) and it should be added to an entrypoint in another app, one can use the `install_controller` command.
The Syntax is

```
python manage.py install_controller <target-app> <source-app> <controller-name>
```

If you have two apps `apps/demo` and `apps/demo2` and want to install athe controller `Mycontroller` from `apps/demo/javascript/controllers/mycontroller_controller.js` into `apps/demo2`s entrypoint (which is `apps/demo2/javascript/application.js`) then you have to use the command

```
python manage.py install_controller apps.demo2 apps.demo mycontroller
```

# Release Notes

## Release 0.2.0

* Added the `install_controller` command

## Release 0.1.1

* Fixed a bug where `stimulus` only works with `--templates` option.

## Release 0.1.0

* Initial Release

# Community and Discussion

Please feel free to join the project on github: https://github.com/hotwire-django/stimulus-webpack-tools
or join our Slack: https://join.slack.com/t/hotwire-django/shared_invite/zt-kl0e0plt-uXGQ1PUt5yRohLNYcVvhhQ
(if its not working just ping j.feinauer@pragmaticminds.de for an invite or open an issue on github).
