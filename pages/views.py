from django.db import connection
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "tutorings.html"

    def get_context_data(self, **kwargs):
        with connection.cursor() as cursor:
            query = """
                SELECT *
                FROM "Timeslot"
                         LEFT JOIN timeslot_tutoringparticipant ttp ON timeslot.id_timeslot = ttp.id_timeslot
                         LEFT JOIN "Medium" ON timeslot.id_medium = medium.id_medium
                         LEFT JOIN "Tutoring" ON timeslot.id_tutoring = tutoring.id_tutoring
                WHERE (id_timeslot_tutoring_participant IS NULL OR allow_multiple_participants IS 1)
                  AND "Medium".is_remote = 1
                  AND "Timeslot".takes_place_at BETWEEN DATETIME('2021-11-01 15:22:18') AND DATETIME('2021-11-13 15:22:18')
                  AND "Tutoring".id_subject = 1
                ORDER BY "Timeslot".takes_place_at;
            """
            cursor.execute(query)

            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            print(rows)

            context = super().get_context_data(**kwargs)
            context['tutorings'] = rows
            return context
