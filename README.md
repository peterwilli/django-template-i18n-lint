Django Template i18n lint
=========================
+ Awesomeness from Peter Willemsen
---------------------

Automatically changes text to translatable text.
## Example
	<meta charset="utf-8">
	<title>Hi!!!!</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="">
	<meta name="author" content="">

	Make 'Hi!!!!' translatable? [y/n] y

### Becomes
	<meta charset="utf-8">
	<title>{% trans "Hi!!!!" %}</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="">
	<meta name="author"	 content="">


A simple script to find non-i18n text in a Django template.

For more info see [Lint tool to find non-i18n strings in a django template](http://www.technomancy.org/python/django-template-i18n-lint/)
