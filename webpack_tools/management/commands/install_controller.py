import subprocess
import os
from importlib import import_module
from os.path import dirname

from django.core.management.base import BaseCommand, CommandError
from django.core.management.templates import TemplateCommand
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = 'Helps to install a stimulus controller into an Entrypoint file'

    def add_arguments(self, parser):
        parser.add_argument('to', help='Name of the application to install to.')
        parser.add_argument('from', help='Name of the application to install from.')
        parser.add_argument('controller', help='Name of the stimulus controller to install')

    def handle(self, *args, **options):
        to_app = options.pop('to')
        from_app = options.pop('from')
        controller = options.pop('controller')

        self.stdout.write(self.style.SUCCESS(f'Installing Controller {controller} from app {from_app} in app {to_app}'))

        to_app_root = self.validate_name(to_app)
        from_app_root = self.validate_name(from_app)

        # print(f'Root To: {to_app_root}')
        # print(f'Root From: {from_app_root}')

        # Count how many paths you have to go upward

        js_path_to = os.path.join(to_app_root, 'javascript')
        js_path_from = os.path.join(from_app_root, 'javascript', 'controllers')

        controller_path = os.path.join(js_path_from, f'{controller}_controller.js')
        entrypoint_path = os.path.join(js_path_to, 'application.js')

        # print(f'Entrypoint: {entrypoint_path}')

        # Check if both exist
        if not os.path.exists(js_path_to):
            raise CommandError(f"No controllers folder found for target app (expected '{js_path_to}')")

        if not os.path.exists(js_path_from):
            raise CommandError(f"No controllers folder found for source app (expected '{js_path_from}')")

        if not os.path.exists(controller_path):
            raise CommandError(f"Controller {controller} was not found for in source app (expected '{controller_path}')")

        # print(f'Controller root To: {js_path_to}')
        # print(f'Controller root From: {controller_path}')

        common_prefix = os.path.commonpath([js_path_to, controller_path])

        # print(f'Common: {common_prefix}')

        # Check how many we have to go down, to go to common path
        mydir = js_path_to
        level = 0
        while not common_prefix == mydir:
            mydir = dirname(mydir)
            level += 1

        # print(f'We need to go {level} dirs up!')

        relative_path = os.path.relpath(controller_path, start=common_prefix)

        # print(f'Relative Segment is: {relative_path}')

        subpaths = ['..' for i in range(0, level)]
        subpath = os.path.join('./', *subpaths)

        # print(f'Subpath: {subpath}')

        import_path = os.path.join(subpath, relative_path)

        # print(f'Import Path: {import_path}')

        controller_identifier = f'{controller.title()}Controller'

        import_statement = f'import {controller_identifier} from "{import_path.replace(".js", "")}"'
        register_statement = f'application.register("{controller}", {controller_identifier})'

        # print(import_statement)

        self.stdout.write(f" + Adding Import Statement '{import_statement}' to {entrypoint_path}")
        self.stdout.write(f" + Adding Register Statement '{register_statement}' to {entrypoint_path}")

        # Insert them in the existing file
        with open(entrypoint_path, "r") as file:
            contents = file.readlines()

        index = 0
        import_line = None
        register_line = None
        for line in contents.copy():
            index += 1
            if line.startswith('// Custom Controller Imports'):
                import_line = index
            if line.startswith('// Custom Controllers'):
                register_line = index

        # Insert the line
        if import_line is None:
            # At the end
            contents.append(f'{import_statement}\n')
            contents.append(f'{register_statement}\n')
        else:
            contents.insert(import_line, f'{import_statement}\n')
            if register_line is not None:
                contents.insert(register_line + 1, f'{register_statement}\n')  # Why + 1 here?
            else:
                contents.append(f'{register_statement}\n')

        # Write back
        with open(entrypoint_path, "w") as file:
            file.write("".join(contents))

        self.stdout.write(self.style.SUCCESS(f'Controller from {controller_path} was successfully imported in entrypoint {entrypoint_path}!'))


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
