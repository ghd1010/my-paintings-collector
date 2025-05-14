from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404 # get painting or raise the error
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from main_app.models import Painting, ColorPalette, Mood

from .serializers import PaintingSerializer, ColorPaletteSerializer

class SignUpView(APIView):
    # we can add in a try-catch if the user is already signed up
    permission_classes = [AllowAny]
    
    # when we recieve a POST request with username, email, and password. Create a new user
    def post(self, request):
        # using .get will not error if there is no username
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        # check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)
        
        try:
            validate_password(password)
        except ValidationError as err:
            return Response({'error': err.messages}, status=400)

        # Actually create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # create an access and refresh token for the user and send this in a response
        tokens = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(tokens),
                'access': str(tokens.access_token)
            },
            status=201
        )


class PaintingListAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get all Paintings form the DB
        # Serialize our paintings into JSON
        # Return the serialized paintings in the HTTP response
        paintings = Painting.filter(user=request.user) # now we only get the paintings for the user who login, to protect data that is not belong to the authenticated user
        serializer = PaintingSerializer(paintings, many=True) # `many=True` will make sure we get an array of paintings
        return Response(serializer.data)
    
    def post(self, request):
        # De-serialize our data
        # If it's valid, save it to the Database
        # Return a respose of 201 created
        serializer = PaintingSerializer(data=request.data)
        if serializer.is_valid(): # is it valid?
            serializer.save() # save to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# ------ This is the POST test request in Postman ------
# Link: http://127.0.0.1:8000/api/paintings/

# Body:
#   {
#         "mood": [],
#         "name": "kitten-test",
#         "colors_type": "Oil",
#         "year_created": 2025,
#         "style": "Free Style",
#         "user": 2
#     }

class CreatePaletteAPI(APIView):
    def get(self, request):
        palette = ColorPalette.objects.all() # Query the DB for all palettes
        serializer = PaintingSerializer(palette, many=True) # `many=True` will make sure we get an array of palettes
        return Response(serializer.data)

    def post(self, request, painting_id):
        #painting will be the painting object passed into our painting_id 
        # or it will raise a 404, if it doesnt exist
        painting = get_object_or_404(Painting, pk=painting_id) #id= also same, this line ensures the painting exist in DB 
        # get hold of the JSON data that has come in on the POST request
        data = request.data.copy() #immutable, cannot be changed, and we want to change it hmmm but add .copy() works
        # make a copy as request.data is immutable
        data['painting'] = painting.id 
        serializer = ColorPaletteSerializer(data=data)
        if serializer.is_valid(): # if its valid ?!
            serializer.save() # save to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------ This is the POST test request in Postman ------
# Link: http://127.0.0.1:8000/api/paintings/3/add-palette

# Body:
# {
#   "name": "warm",
#   "colors": "red, orange, yellow, hot-pink",
#   "note": "summer summer!"
# }

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_mood_to_painting(request, painting_id, mood_id):
    try:
        # Get the painting by painting_id
        painting = Painting.objects.get(pk=painting_id)
        # Get the mood by mood_id
        mood = Mood.objects.get(pk=mood_id)
        # Add the mood to the painting
        painting.mood.add(mood)
        return Response({'message': 'Mood was added successfully!'}, status=200)
    except Painting.DoesNotExist:
        return Response({'error': 'The painting does not exist'}, status=404)
    except Mood.DoesNotExist:
        return Response({'error': 'The mood does not exist'}, status=404)
    except: # catch all
        return Response({'error': 'Something went wrong'}, status=500)

# ------ This is the POST test request in Postman ------

# Mood was added successfully!: http://127.0.0.1:8000/api/paintings/8/add-mood/3 
# The painting does not exist: http://127.0.0.1:8000/api/paintings/100/add-mood/3
# The mood does not exist: http://127.0.0.1:8000/api/paintings/2/add-mood/100

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_mood_from_painting(request, painting_id, mood_id):
    try:
        # Get the painting by painting_id
        painting = Painting.objects.get(pk=painting_id)
        # Get the mood by mood_id
        mood = Mood.objects.get(pk=mood_id)
        # remove the mood from the painting
        painting.mood.remove(mood)
        return Response({'message': 'Mood was removed successfully!'}, status=200)
    except Painting.DoesNotExist:
        return Response({'error': 'The painting does not exist'}, status=404)
    except Mood.DoesNotExist:
        return Response({'error': 'The mood does not exist'}, status=404)
    except: # catch all
        return Response({'error': 'Something went wrong'}, status=500)
    
# ------ This is the POST test request in Postman ------

# Mood was removed successfully!: http://127.0.0.1:8000/api/paintings/2/remove-mood/2
# The painting does not exist: http://127.0.0.1:8000/api/paintings/200/remove-mood/2
# The mood does not exist: http://127.0.0.1:8000/api/paintings/2/remove-mood/100
