from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Job
from .serializers import JobSerializer


# Create your views here.
class JobList(APIView):
    def get(self, request):
        # jobs = Job.objects.all()
        jobs = Job.objects.filter(is_active=True)  # only return active jobs
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetail(APIView):
    def __get_active_job(self, pk):
        return get_object_or_404(Job, pk=pk, is_active=True)  # only return active jobs

    def get(self, request, pk):
        # job = get_object_or_404(Job, pk=pk, is_active=True)  # only return active jobs
        job = self.__get_active_job(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        # job = get_object_or_404(Job, pk=pk, is_active=True)  # only update active jobs
        job = self.__get_active_job(pk)
        serializer = JobSerializer(job, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        job = self.__get_active_job(pk)
        # job = get_object_or_404(Job, pk=pk, is_active=True)  # only delete active jobs
        job.is_active = False  # soft delete
        job.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
