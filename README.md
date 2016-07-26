**About**
A python lambda implementation of the Janitor Monkey.

In order to check tag rules and that there are no unused resources laying around.

**Deploy**
Made with [Apex](apex.run) in mind for the deploy tool - not entirely sure how I was supposed to structure this but if
you create a new apex project should just be able to drop this into that directory.

**Tests**
Tests through pytest

**Adding new resources**
The plan is should just be able to drop a new .py file with a class of the resource name into the Janitor/resources directory.
Just make sure the class implements use_janitor and tag_janitor methods and returns an array of the correct type of violations and should be good to go.
