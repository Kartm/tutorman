from django.db import connection
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        with connection.cursor() as cursor:
            query = """
                SELECT "Timeslot".*, "Tutoring".*, "Medium".*, "Description".*, "Bill".*
                FROM "TutoringParticipant"
                   LEFT JOIN "Timeslot_TutoringParticipant" ON tutoringparticipant.id_tutoring_participant = timeslot_tutoringparticipant.id_tutoring_participant
                   LEFT JOIN "Timeslot" ON timeslot_tutoringparticipant.id_timeslot = timeslot.id_timeslot
                   LEFT JOIN "Tutoring" ON timeslot.id_tutoring = tutoring.id_tutoring
                   LEFT JOIN "Description" ON tutoring.id_description = description.id_description
                   LEFT JOIN "Medium" ON timeslot.id_medium = medium.id_medium
                   LEFT JOIN "Bill" ON timeslot_tutoringparticipant.id_bill = bill.id_bill
                WHERE "TutoringParticipant".id_user = 2;
            """
            cursor.execute(query)

            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            print(rows)

            context = super().get_context_data(**kwargs)
            context['tutorings'] = rows
            return context


class TutoringsPageView(TemplateView):
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

class TutoringPreviewPageView(TemplateView):
    template_name = "tutoring-preview.html"

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