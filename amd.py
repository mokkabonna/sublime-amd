import sublime, sublime_plugin, re

class AddAmdModuleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		selection = self.view.sel()[0]
		selected_word = self.view.word(selection)
		word = self.view.substr(selected_word)

		all_text = self.view.substr(sublime.Region(0, self.view.size()))

		matches = re.search(r'(?:define\((\'.+\')?)(\[(?P<modules>.+)(?P<insert_path>\]),\s)function\((?P<variables>([^)]+))?\)', all_text, re.MULTILINE | re.DOTALL)

		variables = matches.group("variables")
		dependencies = matches.group("modules")

		dep_pos = self.view.find(dependencies, 0, sublime.LITERAL)
		var_pos = self.view.find(variables, dep_pos.b, sublime.LITERAL)
		variables += ', ' + word
		self.view.replace(edit, var_pos, variables)

		self.view.window().show_input_panel('Module prefix', word, self.done, self.change, self.cancel)

	def change(self, edit):
		print('change')

	def cancel(self):
		print('cancel')

	def done(self, module_path):
		self.view.run_command("add_amd_module_path", { "new_dependency": module_path })

class AddAmdModulePathCommand(sublime_plugin.TextCommand):
	def run(self, edit, new_dependency):
		print(new_dependency)
		selection = self.view.sel()[0]
		selected_word = self.view.word(selection)
		word = self.view.substr(selected_word)

		all_text = self.view.substr(sublime.Region(0, self.view.size()))
		matches = re.search(
			r'(?:define\((\'.+\')?)'
			r'\[(?P<modules>'
			r'[^]]+'
			r')\]'
			r',\s+function\('
			r'(?P<variables>([^)]+))?\)'
			, all_text
			, re.MULTILINE | re.DOTALL)


		all_modules_string = matches.group('modules')

		modules = re.split(',', all_modules_string)


		last_module_pos = self.view.find(modules[-1], 0, sublime.LITERAL)

		last_module = self.view.substr(last_module_pos)

		##copy the last_module before we change it
		new_module = last_module

		#remove any newline if it has that
		if (last_module[-1] == '\n'):
			last_module = last_module[0:-1] + ','
		else:
			last_module += ','

		#the new module should have the same structure as the last module, jsut repalce the name
		#this means all whitespace in front and after the last module will be reused
		new_module = re.sub('\'.+\'', '\'' + new_dependency + '\'', new_module)


		self.view.replace(edit, last_module_pos, last_module + new_module)

