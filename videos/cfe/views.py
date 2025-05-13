class FileUpload:

    def post(self, request):
        file_id = request.POST.get('file')
        size = request.POST.get('fileSize')
        type = request.POST.get('fileType')
        data = {}

        if file_id:
            obj = Video.objects.get(id=int(file_id))
