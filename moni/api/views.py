# api/views.py
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from user.models import User, Profile
from api.serializers import UserSerializer, ProfileSerializer
from nucleo.models import comunidad, vertiente, kit
from api.serializers import ComunidadSerializer, VertienteSerializer, KitSerializer
from rest_framework import authentication, permissions

# Vista para usuarios

# Solicitar token de autenticación
class UserLogin(APIView):
    """
    UserLogin is an APIView for handling POST requests to authenticate a user.

    Raises:
        Http404: _description_
        Http404: _description_
        Http404: _description_
        Http404: _description_
        Http404: _description_

    Returns:
        _type_: _description_
        token (str): The authentication token.
    """

class UserList(APIView):
    """
    UserList is an APIView for handling GET and POST requests for the User model.

    Methods:
        get: Returns a list of all users.
        post: Creates a new user.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Handles GET requests to retrieve a list of all users.

        Args:
            request (HttpRequest): The HTTP request object.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object containing the serialized user data.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Handles POST requests to create a new user.

        Args:
            request (HttpRequest): The HTTP request object containing the user data.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object containing the serialized user data or errors.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    """
    UserDetail is an APIView for handling GET, PUT, and DELETE requests for a single User instance.

    Methods:
        get: Retrieves a single user by ID.
        put: Updates a user by ID.
        delete: Deletes a user by ID.
    """
    def get_object(self, pk):
        """
        Retrieves a User instance by primary key (ID).

        Args:
            pk (int): The primary key of the user.

        Returns:
            User: The User instance.
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Handles GET requests to retrieve a single user by ID.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the user.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object containing the serialized user data.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Handles PUT requests to update a user by ID.

        Args:
            request (HttpRequest): The HTTP request object containing the updated user data.
            pk (int): The primary key of the user.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object containing the serialized user data or errors.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Handles DELETE requests to delete a user by ID.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the user.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object with status code 204 (No Content).
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileList(APIView):
    """
    ProfileList is an APIView for handling GET and POST requests for the Profile model.

    Methods:
        get: Returns a list of all profiles.
        post: Creates a new profile.
    """
    def get(self, request, format=None):
        """
        Handles GET requests to retrieve a list of all profiles.

        Args:
            request (HttpRequest): The HTTP request object.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object containing the serialized profile data.
        """
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Handles POST requests to create a new profile.

        Args:
            request (HttpRequest): The HTTP request object containing the profile data.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object containing the serialized profile data or errors.
        """
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetail(APIView):
    """
    ProfileDetail is an APIView for handling GET, PUT, and DELETE requests for a single Profile instance.

    Methods:
        get: Retrieves a single profile by ID.
        put: Updates a profile by ID.
        delete: Deletes a profile by ID.
    """
    def get_object(self, pk):
        """
        Retrieves a Profile instance by primary key (ID).

        Args:
            pk (int): The primary key of the profile.

        Returns:
            Profile: The Profile instance.
        """
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Handles GET requests to retrieve a single profile by ID.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the profile.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object containing the serialized profile data.
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Handles PUT requests to update a profile by ID.

        Args:
            request (HttpRequest): The HTTP request object containing the updated profile data.
            pk (int): The primary key of the profile.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object containing the serialized profile data or errors.
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Handles DELETE requests to delete a profile by ID.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the profile.
            format (str, optional): The format to return the response in.

        Returns:
            Response: A Response object with status code 204 (No Content).
        """
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Vista para comunidad
class ComunidadList(APIView):
    def get(self, request, format=None):
        comunidades = comunidad.objects.all()
        serializer = ComunidadSerializer(comunidades, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ComunidadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComunidadDetail(APIView):
    def get_object(self, pk):
        try:
            return comunidad.objects.get(pk=pk)
        except comunidad.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comunidad_obj = self.get_object(pk)
        serializer = ComunidadSerializer(comunidad_obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comunidad_obj = self.get_object(pk)
        serializer = ComunidadSerializer(comunidad_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comunidad_obj = self.get_object(pk)
        comunidad_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Vista para vertiente
class VertienteList(APIView):
    def get(self, request, format=None):
        vertientes = vertiente.objects.all()
        serializer = VertienteSerializer(vertientes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VertienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VertienteDetail(APIView):
    def get_object(self, pk):
        try:
            return vertiente.objects.get(pk=pk)
        except vertiente.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vertiente_obj = self.get_object(pk)
        serializer = VertienteSerializer(vertiente_obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vertiente_obj = self.get_object(pk)
        serializer = VertienteSerializer(vertiente_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vertiente_obj = self.get_object(pk)
        vertiente_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Vista para kit
class KitList(APIView):
    def get(self, request, format=None):
        kits = kit.objects.all()
        serializer = KitSerializer(kits, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = KitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KitDetail(APIView):
    def get_object(self, pk):
        try:
            return kit.objects.get(pk=pk)
        except kit.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        kit_obj = self.get_object(pk)
        serializer = KitSerializer(kit_obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        kit_obj = self.get_object(pk)
        serializer = KitSerializer(kit_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        kit_obj = self.get_object(pk)
        kit_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)