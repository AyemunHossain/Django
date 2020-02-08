................Before this you need to know about adding models, creating superuser, some little knowledge on : html,css,javascript

....1.goto views.py : 
	.... change the return to:
			    return render(
        		        request = request,
        		        template_name="main/home.html",
                                context={"news":News.objects.all},
                           )



....2.then create a folder in main floder called templates then create another on templates called main then create a home.html on main/templates/main/

....3.and add :

	<head>
    {%  load static %}
    <link href="{% static 'tinymce/css/prism.css' %}" rel = "stylesheet">

</head>

<body>

    {% for tut in tutorials %}
    <p> {{ tut.tutorial_title }} </p>
    <p> {{ tut.tutorial_published }} </p>
    <p> {{ tut.tutorial_content|safe}} </p>
    <br><br>
    {% endfor %}

</body>

<script src="{% static 'tinymce/css/prism.js'%}"> </script>

to home.html

...that's it 