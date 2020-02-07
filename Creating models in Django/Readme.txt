...................................Please seach google to know what django model is >>

Step 1 — Create Django Application

Step 2 — Add the Posts Model

Step 3 — Add the main apps to settings.py > INSTALLED_APPS list

Step 4 — Make Migrations...........
				...1.python manage.py makemigrateions
				...2.python migrate
............................................................................Thats enough for if you just want too add model 


---Exploring more 
	.........1.We can see what sql are doing backend
							....1.python manage.py sqlmigrate main 0001 (do this for now)
	
	.........2.We can exploring our model class and it's objects
							.....1. python manage.py shell
							.....2. from main.models import Tutorial
							.....3.	see all objects of Tutorial class ..... Tutorial.objects.all()
							.....4.  creating new objects:

								 from django.utils import timezone 
								 new_obj1 = Tutorial(tutorial_tittle="To do",tutorial_content="Bla bla bla",tutorial_published=timezone.now())
								 new_obj1.save()
								 
	.........3. We can iterate over that new_obj1 object
							.....1. for obj in Tutorial.objects.all():
   								print( obj.tutorial_content )
								
									