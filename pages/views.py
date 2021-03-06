from django.db import connection

from django.views.generic import TemplateView


def fetch_dictionarized_rows(cursor, query):
    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return rows


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        with connection.cursor() as cursor:
            query = """
                SELECT "Timeslot".*, "Tutoring".*, "Medium".*, "Description".*, "Bill".*, "Tutoring".name, "Description".description as description
                FROM "TutoringParticipant"
                   LEFT JOIN "Timeslot_TutoringParticipant" ON tutoringparticipant.id_tutoring_participant = timeslot_tutoringparticipant.id_tutoring_participant
                   LEFT JOIN "Timeslot" ON timeslot_tutoringparticipant.id_timeslot = timeslot.id_timeslot
                   LEFT JOIN "Tutoring" ON timeslot.id_tutoring = tutoring.id_tutoring
                   LEFT JOIN "Description" ON tutoring.id_description = description.id_description
                   LEFT JOIN "Medium" ON timeslot.id_medium = medium.id_medium
                   LEFT JOIN "Bill" ON timeslot_tutoringparticipant.id_bill = bill.id_bill
                WHERE "TutoringParticipant".id_user = 2;
            """

            context = super().get_context_data(**kwargs)
            context['tutorings'] = fetch_dictionarized_rows(cursor=cursor, query=query)
            return context


class TutoringsPageView(TemplateView):
    template_name = "tutorings.html"

    def get_context_data(self, **kwargs):
        sort_param = self.request.GET.get('sort', None)

        sort_part = {
            'price-asc': 'ORDER BY "Tutoring".price_for_timeslot ASC',
            'price-desc': 'ORDER BY "Tutoring".price_for_timeslot DESC'
        }.get(sort_param, 'ORDER BY "Timeslot".takes_place_at')

        location_param = self.request.GET.get('location', None)

        location_part = {
            'remote': 'AND "Medium".is_remote = 1',
            'onsite': 'AND "Medium".is_remote = 0',
        }.get(location_param, '')

        subject_param = self.request.GET.get('subject', None)
        subject_part = f'AND "Tutoring".id_subject = {int(subject_param)}' \
            if subject_param and subject_param.isdigit() \
            else ''

        with connection.cursor() as cursor:
            query = f"""
                SELECT *, "Tutoring".price_for_timeslot
                FROM "Timeslot"
                         LEFT JOIN timeslot_tutoringparticipant ttp ON timeslot.id_timeslot = ttp.id_timeslot
                         LEFT JOIN "Medium" ON timeslot.id_medium = medium.id_medium
                         LEFT JOIN "Tutoring" ON timeslot.id_tutoring = tutoring.id_tutoring
                         LEFT JOIN "Description" ON tutoring.id_description = description.id_description
                WHERE (id_timeslot_tutoring_participant IS NULL OR allow_multiple_participants IS 1)
                  {location_part}
                  AND "Timeslot".takes_place_at BETWEEN DATETIME('2021-11-01 15:22:18') AND DATETIME('2021-11-13 15:22:18')
                  {subject_part}
                {sort_part};
            """

            context = super().get_context_data(**kwargs)

            context['tutorings'] = fetch_dictionarized_rows(cursor=cursor, query=query)

            query = """
                SELECT *
                FROM "Subject";
            """

            context['subjects'] = fetch_dictionarized_rows(cursor=cursor, query=query)

            return context


class TutoringPreviewPageView(TemplateView):
    template_name = "tutoring-preview.html"

    def get_context_data(self, **kwargs):
        with connection.cursor() as cursor:
            query = """
                SELECT * FROM "Tutoring"
                   LEFT JOIN tutoringscope ts ON tutoring.id_tutoring_scope = ts.id_tutoring_scope
                   LEFT JOIN subject s ON tutoring.id_subject = s.id_subject
                   LEFT JOIN book b ON tutoring.id_book = b.id_book
                   LEFT JOIN description d ON tutoring.id_description = d.id_description
                WHERE id_tutoring = 1;
            """

            context = super().get_context_data(**kwargs)
            context['tutoring'] = fetch_dictionarized_rows(cursor=cursor, query=query)[0]

            query = """
                SELECT * FROM "Rating"
                   LEFT JOIN ratingdispute rd ON rating.id_rating = rd.id_rating
                WHERE id_tutoring = 1;
            """

            context['ratings'] = fetch_dictionarized_rows(cursor=cursor, query=query)
            return context