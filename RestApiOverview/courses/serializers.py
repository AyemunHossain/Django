from rest_framework import serializers
from courses.models import Courses, Review


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		extra_kwargs ={
		'email':{'write_only':True}
		}
		exclude = ['course']
		model = Review

	def validate_rating(self, value):
		if value in range(1, 6):
			return value
		raise serializers.ValidationError("Rating must be a number between 1 to 5")
		
class CoursesSerializer(serializers.ModelSerializer):
	reviews = serializers.HyperlinkedRelatedField(
		view_name='review-detail',
		read_only=True,
		many=True,
		)

	class Meta:
		fields = ('id','title','url','reviews',)
		model = Courses

