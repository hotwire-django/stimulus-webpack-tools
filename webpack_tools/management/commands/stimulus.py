import subprocess
import os
from importlib import import_module

from django.core.management.base import BaseCommand, CommandError
from django.core.management.templates import TemplateCommand
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = 'Helps with setting up stimulus applications in django'

    ignore_js_folder_exists = True

    def add_arguments(self, parser):
        parser.add_argument('name', help='Name of the application or project.')
        parser.add_argument('controllers', nargs="*", help='Name of the stimulus controllers to create')
        parser.add_argument('--templates', nargs="*", help='Name of the example templates to create')

    def handle(self, *args, **options):
        app_name = options.pop('name')
        controllers = options.pop('controllers')
        templates = options.pop('templates')

        app_root = self.validate_name(app_name)

        # check if a javascript folder already exists
        js_folder = os.path.join(app_root, 'javascript')
        if os.path.exists(js_folder):
            if self.ignore_js_folder_exists:
                self.stdout.write(
                    self.style.WARNING(f'Path {js_folder} already exists, ignoring and possibly overwriting...'))
            else:
                raise CommandError('Javascript directory exists already, skipping...')
        else:
            os.mkdir(js_folder)
            self.stdout.write(self.style.WARNING(f"Folder '{js_folder}' created"))

        # Now start to create an application.js
        app_js_path = os.path.join(js_folder, 'application.js')
        if os.path.exists(app_js_path):
            self.stdout.write(self.style.WARNING(f'File {app_js_path} already exists, skipping creation'))
        else:
            with open(app_js_path, 'a') as file:
                file.write(render_to_string('webpack_tools/application.js', {}))
            self.stdout.write(self.style.SUCCESS(f'Entrypoint application.js successfully created at {app_js_path}'))

        self.stdout.write(self.style.SUCCESS(f'Creating Controllers'))

        controller_folder = os.path.join(js_folder, 'controllers')

        if os.path.exists(controller_folder):
            self.stdout.write(
                self.style.WARNING(f'Folder for Controllers {controller_folder} already exists, not creating it...'))
        else:
            os.mkdir(controller_folder)
            self.stdout.write(self.style.WARNING(f"Folder '{controller_folder}' created"))

        for controller in controllers:
            file_path = os.path.join(controller_folder, f'{controller}_controller.js')
            if os.path.exists(file_path):
                self.stdout.write(
                    self.style.WARNING(f'Controller {controller} already exists, in {file_path}, skipping...'))
                continue
            # Create file from template
            with open(file_path, 'a') as file:
                file.write(render_to_string('webpack_tools/controller.js', {"name": controller}))
            self.stdout.write(self.style.SUCCESS(f'Controller {controller} successfully created at {file_path}'))


        template_folder = os.path.join(app_root, 'templates')

        if os.path.exists(template_folder):
            self.stdout.write(
                self.style.WARNING(f'Folder for Templates {template_folder} already exists, not creating it...'))
        else:
            os.mkdir(template_folder)
            self.stdout.write(self.style.WARNING(f"Folder '{template_folder}' created"))

        if templates is not None:
            for template in templates:

                if not template.endswith('.html'):
                    template = f'{template}.html'

                file_path = os.path.join(template_folder, f'{template}')

                if os.path.exists(file_path):
                    self.stdout.write(
                        self.style.WARNING(f'Template {template} already exists, in {file_path}, skipping...'))
                    continue

                # Create file from template
                with open(file_path, 'a') as file:
                    file.write(render_to_string('webpack_tools/template.html', {"name": template, "controllers": controllers}))
                self.stdout.write(self.style.SUCCESS(f'Template {template} successfully created at {file_path}'))

        self.stdout.write(self.style.SUCCESS('Stimulus setup complete. After building webpack you should be able to '
                                             'use stimulus!'))

    # Copied from TemplateCommand
    def validate_name(self, name):
        if name is None:
            raise CommandError('you must provide an app name')
        # Check it's a valid directory name.
        # if not name.isidentifier():
        #     raise CommandError(
        #         f"'{name}' is not a valid app name. Please make sure the "
        #         "name is a valid identifier.")
        # Check it CAN be imported.
        app_module = None
        try:
            app_module = import_module(name)
        except ImportError:
            raise CommandError(f"Unable to import '{name}' cannot be imported. Is it installed?")

        # Check if we find the proper folder
        app_root = os.path.dirname(app_module.__file__)

        if not os.path.exists(app_root):
            raise CommandError(f"Unable to access root folder '{app_root}' for app '{name}'")

        return app_root
