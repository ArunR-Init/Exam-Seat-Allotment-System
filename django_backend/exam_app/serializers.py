"""
Serializers for the Exam Allotment System.
These handle data validation similar to Zod schemas in the Node.js version.
"""
from rest_framework import serializers
from .models import User, Room, Allotment


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'role']
        read_only_fields = ['id']


class StudentRegisterSerializer(serializers.Serializer):
    """Serializer for student registration (matching studentRegisterSchema)."""
    username = serializers.CharField(required=True, error_messages={'required': 'Roll Number is required'})
    name = serializers.CharField(required=True, error_messages={'required': 'Name is required'})
    password = serializers.CharField(required=True, write_only=True, error_messages={'required': 'Password is required'})
    confirmPassword = serializers.CharField(required=True, write_only=True, error_messages={'required': 'Confirm Password is required'})
    
    def validate(self, data):
        """Validate that passwords match."""
        if data.get('password') != data.get('confirmPassword'):
            raise serializers.ValidationError({
                'confirmPassword': "Passwords don't match"
            })
        return data
    
    def create(self, validated_data):
        """Create a new student user."""
        validated_data.pop('confirmPassword')
        validated_data['role'] = 'student'
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Serializer for login (matching loginSchema)."""
    username = serializers.CharField(required=True, error_messages={'required': 'Username/Roll Number is required'})
    password = serializers.CharField(required=True, write_only=True, error_messages={'required': 'Password is required'})
    role = serializers.ChoiceField(choices=['admin', 'teacher', 'student'], required=True)


class TeacherCreateSerializer(serializers.Serializer):
    """Serializer for creating a teacher."""
    username = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def create(self, validated_data):
        """Create a new teacher user."""
        validated_data['role'] = 'teacher'
        return User.objects.create_user(**validated_data)


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model."""
    
    class Meta:
        model = Room
        fields = ['id', 'name', 'teacher_id']
        read_only_fields = ['id']


class AllotmentSerializer(serializers.ModelSerializer):
    """Serializer for Allotment model."""
    
    class Meta:
        model = Allotment
        fields = ['id', 'student_id', 'room_id', 'seat_number']
        read_only_fields = ['id']


class StudentAllotmentResponseSerializer(serializers.Serializer):
    """Response serializer for student allotment details."""
    room = RoomSerializer()
    allotment = AllotmentSerializer()


class TeacherRoomStudentSerializer(serializers.Serializer):
    """Serializer for student in teacher's room."""
    student = UserSerializer()
    seatNumber = serializers.IntegerField(source='seat_number')


class TeacherRoomResponseSerializer(serializers.Serializer):
    """Response serializer for teacher's room details."""
    room = RoomSerializer()
    students = TeacherRoomStudentSerializer(many=True)


class AllotmentResultSerializer(serializers.Serializer):
    """Response serializer for allotment operation."""
    message = serializers.CharField()
    roomsCreated = serializers.IntegerField()
    studentsAllotted = serializers.IntegerField()
