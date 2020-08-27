.............Before this you need to create a project and add models and create superuser account and must need to ok everythings ...if yes then step forward with me

There's a library available for creating awsome textbox and manyothers called : tinymce
So i am gonna use that for creating textbox purpose.



1.....To install--- pip install django-tinymce4-lite

2.... add insetings.py -> INSTALLED_APPS and add 'tinymce':
3.... and add this text bellow anywhere in  setings.py  without all dash(---) :
----------------------------------------------------------------------------------------------------------------------
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
    }
----------------------------------------------------------------------------------------------------------------------
4.... then go to mysite (project's main) url then add the url of tinymce like -- > path('tinymce/',include('tinymce.urls'))

then you can use tinymce anywhere in you project


------------------------------------------------------------------------------------------------------------------------

in my project i am using this on admin page so : 

....1 Goto admin.py and import the : from tinymce import TinyMCE   
	....To use tinymce's feature
....2.And import : from django.db import models
	....Because we are replacing models widgets to have a awesome texteditor 
....2.then in NewsAdmin class and add: 
 
	formfield_overrides = {
        models.TextField:{'widget':TinyMCE}

    	}

...3. Now everythings is ok ....go to http://127.0.0.1:8000/admin ......and log in with your admin name and pass 
		.... I have added an account name : Rami
					     pass : ramirami

...4. And now goto http://127.0.0.1:8000/admin/main/news/add/ and see the magic on Textbox