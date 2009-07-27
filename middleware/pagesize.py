# used in questions
QUESTIONS_PAGE_SIZE = 10
class QuestionsPageSizeMiddleware(object):
    def process_request(self, request):
        # Set flag to False by default. If it is equal to True, then need to be saved.
        pagesize_changed = False
        # get pagesize from session, if failed then get default value
        user_page_size = request.session.get("pagesize", QUESTIONS_PAGE_SIZE)
        # set pagesize equal to logon user specified value in database
        if request.user.is_authenticated() and request.user.questions_per_page > 0:
            user_page_size = request.user.questions_per_page

        try:
            # get new pagesize from UI selection
            pagesize = int(request.GET.get('pagesize', user_page_size))
            if pagesize <> user_page_size:
                pagesize_changed = True

        except ValueError:
            pagesize  = user_page_size
        
        # save this pagesize to user database
        if pagesize_changed:
            if request.user.is_authenticated():
                user = request.user
                user.questions_per_page = pagesize
                user.save()
        # put pagesize into session
        request.session["pagesize"] = pagesize