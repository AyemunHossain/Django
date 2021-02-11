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
							.....2. from main.models import News
							.....3.	see all objects of Tutorial class ..... News.objects.all()
							.....4.  creating new objects:

								 from django.utils import timezone 
								 news1 = News(news_title="Bangladesh Won by 3 Wickets",news_author="Ashik",news_published=timezone.now(),
											news_content="So this is a news for today that Bangaldesh is won by 3 wickets and Shakib All Hassan Got 5 wickets and 48 runs in 34 balls")
								 news1 .save()
								 
	.........3. We can iterate over that new_obj1 object
							.....1. for obj in News.objects.all():
   								print( obj.news_title )
								
									