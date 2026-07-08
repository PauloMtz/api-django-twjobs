from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# from rest_framework.pagination import PageNumberPagination

from core.pagination import TWJobsPagination
from .models import Job
from .serializers import JobSerializer
from .filters import JobFilterSet


# Create your views here.
class JobList(APIView):
    def get(self, request):
        # paginator = PageNumberPagination()
        paginator = TWJobsPagination()
        query_set = Job.objects.filter(is_active=True)
        # --- abaixo segue filtro sem o filterset ---
        # query_set = Job.objects.filter(
        #    is_active=True,
        #    title__icontains=request.GET.get("title", ""),
        #    location__icontains=request.GET.get("location", ""),
        # )
        # if request.GET.get("job_type") is not None:
        #    query_set = query_set.filter(job_type=request.GET.get("job_type"))
        # --- filtros com o filterset ---
        filter = JobFilterSet(request.GET, queryset=query_set)
        jobs = paginator.paginate_queryset(filter.qs, request)
        serializer = JobSerializer(jobs, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetail(APIView):
    def __get_active_job(self, pk):
        return get_object_or_404(Job, pk=pk, is_active=True)

    def get(self, request, pk):
        job = self.__get_active_job(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.__get_active_job(pk)
        serializer = JobSerializer(job, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        job = self.__get_active_job(pk)
        job.is_active = False
        job.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
