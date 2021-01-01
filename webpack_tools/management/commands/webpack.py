import subprocess
import os

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = 'Runs the webpack build...'

    dev_packages = [
        "webpack",
        "webpack-cli",
        "webpack-bundle-analyzer",
        "@stimulus/webpack-helpers",
        "babel-loader",
        "@babel/core",
        "@babel/plugin-proposal-decorators",
        "@babel/plugin-proposal-class-properties",
        "@babel/plugin-transform-runtime",
        "@babel/preset-env"
    ]

    def add_arguments(self, parser):
        parser.add_argument('--init-full', dest='init-full', action='store_true',
                            help='do all operations, equivalent to --init-npm --dependencies')

        parser.add_argument('--init-npm', dest='init-npm', action='store_true',
                            help='Initialize npm')

        parser.add_argument('--dependencies', dest='dependencies', action='store_true',
                            help='Install npm dependencies')

        parser.add_argument('--loop', dest='loop', action='store_true',
                            help='Install npm dependencies in a loop')

        parser.add_argument('--build', dest='build', action='store_true',
                            help='Execute webpack')

    def handle(self, *args, **options):
        if options['init-full'] or options['init-npm']:
            self.npm_init(*args, **options)
        if options['init-full'] or options['dependencies']:
            self.npm_install_dev_dependencies(*args, **options)
        if options['build']:
            self.call_webpack(*args, **options)

    def call_webpack(self, *args, **options):
        if not os.path.exists('webpack.config.js'):
            self.stdout.write(self.style.WARNING('No Webpack Config Found, installing default...'))
            with open('webpack.config.js', 'a') as file:
                file.write(render_to_string('webpack_tools/webpack.config.js', {}))
            self.stdout.write(self.style.SUCCESS('Default Webpack Config created...'))
        self.stdout.write(self.style.SUCCESS('Calling Webpack!'))
        # TODO use response?
        response = subprocess.run(["npx", "webpack"])

    def npm_init(self, *args, **options):
        if os.path.exists('package.json'):
            self.stdout.write(self.style.ERROR('Existing package.json already found, dont initialising npm!'))
            return
        response = subprocess.run(["npm", "init", "-y"])
        if response.returncode == 0:
            self.stdout.write(self.style.SUCCESS('package.json was created sucessfully!'))
        else:
            self.stdout.write(self.style.WARNING('Unnable to init npm, see above for more details!'))

    def npm_install_dev_dependencies(self, *args, **options):
        if not os.path.exists('package.json'):
            self.stdout.write(self.style.ERROR('No package.json found, please initialise npm first...'))
            return

        if options['loop']:
            results = {}
            for package in self.dev_packages:
                self.stdout.write(f'Installing package {package}')
                response = subprocess.run(["npm", "install", "--save-dev", package])
                results.update({package: response})
                if response.returncode == 0:
                    self.stdout.write(self.style.SUCCESS(f'Package {package} was installed successfully!'))
                else:
                    self.stdout.write(self.style.ERROR(f'Package {package} failed to install!'))

            if len(list(filter(lambda k: results[k].returncode != 0, results.keys()))) > 0:
                self.stdout.write(self.style.WARNING(f'There were errors when installing packages...'))
        else:
            self.stdout.write(f'Installing all packages at once {self.dev_packages}')
            response = subprocess.run(["npm", "install", "--save-dev"] +  self.dev_packages)
            if response.returncode != 0:
                self.stdout.write(self.style.WARNING(f'There were errors when installing packages...'))
