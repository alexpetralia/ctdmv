class CSVFileMixin(object):
    """
    Mixin which allows the override of the filename being
    passed back to the user when the spreadsheet is downloaded.
    """

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if response.accepted_renderer.format == "csv":
            response["Content-Disposition"] = f"attachment; filename=data.csv"
        return response

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context['header'] = (
            'id', 'creation_date_utc', 'branch', 'service',
            'wait_time_mins', 'num_waiting',
        )
        return context
