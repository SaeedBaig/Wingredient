[Mako](https://www.makotemplates.org) templates go in this directory.

Please try to include, near the top of your files, all the Python paramaters that your Mako template relies on (a description of the Python type of said paramaters, and what they're supposed to be, would also be helpful). E.g.

```html
<!DOCTYPE html>

<!--
Python variables that need to be passed in for this template to render correctly:
- title:        str (title of the recipe)
- num_likes:    int (number of likes this recipe has)
- difficulty:   str (either 'Easy', 'Medium' or 'Hard')
- ingredients:  list of str (e.g. ['Milk', 'Eggs', 'Sugar'])
...
-->
```

This is so that people writing the Python files can easily tell at a glance what paramaters they have to pass into the template.render().
