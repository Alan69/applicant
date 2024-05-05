from datetime import datetime
from django.views.generic.edit import FormView
from django.views.generic import UpdateView
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import activate, get_language
from .forms import ProposalForm
from .models import Proposal
from main.views import HomeView
from .models import *
from docxtpl import DocxTemplate

def generate_word(request):
    # Fetch data from the Proposal model
    proposal = Proposal.objects.first()  # You may adjust this query based on your needs

    # Extract relevant data from the proposal
    data = {
        "first_name": proposal.first_name,
        "last_name": proposal.last_name,
        "middle_name": proposal.middle_name,
        "identification_birth_date": proposal.identification_birth_date,
        "gender": proposal.gender,
        "citizenship": proposal.citizenship, 
        "nationality": proposal.nationality, 
        "address_area": proposal.address_area, 
        "address_region": proposal.address_region, 
        "address_city": proposal.address_city,
        "educational_certificate_date": proposal.educational_certificate_date, 
        "testing_certificate_date": proposal.testing_certificate_date, 
        "education_stage": proposal.education_stage, 
        "form_of_study": proposal.form_of_study, 
        "educ_plan_group": proposal.educ_plan_group, 
        "basis_for_enrollment": proposal.basis_for_enrollment,
        "father_first_name": proposal.father_first_name,
        "father_last_name": proposal.father_last_name, 
        "mother_first_name": proposal.mother_first_name, 
        "mother_last_name": proposal.mother_last_name, 
        "family_position_status": proposal.family_position_status,
        "address_street": proposal.address_street,
        "lang_of_study": proposal.lang_of_study,
        "testing_certificate_date": proposal.testing_certificate_date,
     
    }
    template = DocxTemplate('template.docx')
    # Load the template docx file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response["Content-Disposition"] = 'filename="output.docx"'
    
    template.render(data)
    template.save(response)
    
    return response

def get_dogovor(request):
    proposal = Proposal.objects.first()  # You may adjust this query based on your needs

    # Extract relevant data from the proposal
    data = {
        "first_name": proposal.first_name,
        "last_name": proposal.last_name,
        "middle_name": proposal.middle_name,
        "identification_birth_date": proposal.identification_birth_date,
        "identification_number": proposal.identification_number,
        "identification_issue_date": proposal.identification_issue_date,
        "citizenship": proposal.citizenship, 
        "address_area": proposal.address_area, 
        "phone_number": proposal.phone_number,
        "address_region": proposal.address_region, 
        "address_city": proposal.address_city,
        "educational_certificate_date": proposal.educational_certificate_date, 
        "testing_certificate_date": proposal.testing_certificate_date, 
        "identification_birth_date": proposal.identification_birth_date,
        "education_stage": proposal.education_stage, 
        "form_of_study": proposal.form_of_study, 
        "educ_plan_group": proposal.educ_plan_group, 
        "basis_for_enrollment": proposal.basis_for_enrollment,
        "father_first_name": proposal.father_first_name,
        "father_last_name": proposal.father_last_name, 
        "mother_first_name": proposal.mother_first_name, 
        "mother_last_name": proposal.mother_last_name, 
        "family_position_status": proposal.family_position_status,
        "iin": proposal.iin,
        "register_address_area": proposal.register_address_area,
     
    }
    template = DocxTemplate('template2.docx')
    # Load the template docx file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response["Content-Disposition"] = 'filename="output2.docx"'
    
    template.render(data)
    template.save(response)
    
    return response


def set_language(request):
    # Получите выбранный код языка из запроса (например, через GET-параметр)
    language_code = request.GET.get('language_code')

    # Установите выбранный язык в текущую локаль
    activate(language_code)

    # Перенаправьте пользователя на нужную страницу
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_faculties(request):
    educ_plan_group_id = request.GET.get('educ_plan_group_id')

    # Получение связанных факультетов на основе выбранной группы специальности
    speciality_group = SpecialityGroup.objects.get(id=educ_plan_group_id)
    faculties = Faculty.objects.filter(id=speciality_group.faculty.id).values('id', 'name_ru', 'name_en', 'name_kk')

    # Создание словаря с данными факультетов (ID и название)
    language = get_language()
    faculties_data = {
        faculty['id']: faculty[f'name_{language}'] for faculty in faculties
    }

    # Возвращение данных в формате JSON
    return JsonResponse({'faculties': faculties_data})


def get_groups(request):
    education_stage_id = request.GET.get('education_stage_id')
    educs = SpecialityGroup.objects.filter(education_stage_id=education_stage_id).values(
        'id', 'name_ru', 'name_en', 'name_kk'
    )

    language = get_language()
    educs_dict = {
        educ['id']: educ[f'name_{language}'] for educ in educs
    }

    return JsonResponse({'educs': educs_dict})


def get_educs(request):
    educ_plan_group_id = request.GET.get('educ_plan_group_id')
    educs = Speciality.objects.filter(speciality_group_id=educ_plan_group_id).values(
        'id', 'name_ru', 'name_en', 'name_kk'
    )

    language = get_language()
    educs_dict = {
        educ['id']: educ[f'name_{language}'] for educ in educs
    }

    return JsonResponse({'educs': educs_dict})


def get_subject1(request):
    educ_plan_id = request.GET.get('educ_plan_id')

    # Определение языковой локали
    language = get_language()

    subjects = Subject1.objects.filter(speciality_id=educ_plan_id).values('id', f'subject1__name_{language}')
    subjects2 = Subject2.objects.filter(speciality_id=educ_plan_id).values('id', f'subject2__name_{language}')

    subjects_dict = {
        subject['id']: subject[f'subject1__name_{language}'] for subject in subjects
    }

    subjects_dict2 = {
        subject2['id']: subject2[f'subject2__name_{language}'] for subject2 in subjects2
    }

    data = {'subjects': subjects_dict, 'subjects2': subjects_dict2}

    return JsonResponse(data)


def get_regions(request):
    educational_area_id = request.GET.get('educational_area_id')
    regions = Region.objects.filter(area_id=educational_area_id).values('id', 'name_ru', 'name_en', 'name_kk')

    language = get_language()
    regions_dict = {
        region['id']: region[f'name_{language}'] for region in regions
    }

    return JsonResponse({'regions': regions_dict})

class ApplicationFormView(HomeView, FormView):
    template_name = "application/application.html"
    form_class = ProposalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposal_form = self.form_class
        context['proposal_form'] = proposal_form
        applicant = self.request.user
        context['applicant'] = applicant
        context['proposals'] = Proposal.objects.filter(applicant=applicant)
        context['success_message'] = self.request.GET.get('success_message', False)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_success_url(self):
        return reverse('application')

    def form_valid(self, form):
        if form.is_valid():
            apply = form.save(commit=False)
            applicant = self.request.user
            current_year = datetime.now().year

            existing_application = Proposal.objects.filter(applicant=applicant, created_at__year=current_year).exists()

            if existing_application:
                # Обработка ошибки, если уже существует заявка студента в текущем году
                form.add_error(None, 'У вас уже существует заявка на текущий год.')
                return self.form_invalid(form)

            messages.success(self.request, 'Form submission successful')
            apply.applicant = self.request.user

            # Получение значения из чекбокса
            golden_badge = form.cleaned_data.get('golden_badge')
            apply.golden_badge = golden_badge

            apply.save()

        return HttpResponseRedirect(self.get_success_url() + '?success_message=true')

    def form_invalid(self, form):
        # Добавьте заполненные данные обратно в контекст формы
        self.object = None

        context = self.get_context_data(form=form)
        context['form'] = form  # Замените form_class на form

        return self.render_to_response(context)


class ApplicationUpdateView(UpdateView):
    """
    Вьюшка для редактирования заявки
    """
    model = Proposal
    template_name = "application/applicationedit.html"
    form_class = ProposalForm

    def get_object(self, *args, **kwargs):
        application = get_object_or_404(Proposal, pk=self.kwargs['pk'], applicant=self.request.user)
        return application

    def get_context_data(self, **kwargs):
        applicant = self.request.user
        proposal_id = self.kwargs['pk']

        context = super().get_context_data(**kwargs)
        context['proposal_form'] = self.form_class
        context['applicant'] = applicant
        context['proposals'] = Proposal.objects.filter(id=proposal_id, applicant=applicant)

        if self.object and self.object.status != 'new':
            context['read_only'] = True

        return context

    def get_success_url(self):
        return reverse('application')

    def form_valid(self, form):
        if form.is_valid():
            apply = form.save(commit=False)

            # Обновляем необходимые поля
            apply.status = 'new'
            messages.success(self.request, 'Form submission successful')

            # Получение значения из чекбокса
            golden_badge = form.cleaned_data.get('golden_badge')
            apply.golden_badge = golden_badge

            apply.save()

        return HttpResponseRedirect(self.get_success_url() + '?success_message=true')

    def form_invalid(self, form):
        # Добавьте заполненные данные обратно в контекст формы
        self.object = None

        context = self.get_context_data(form=form)
        context['form'] = form  # Замените form_class на form

        return self.render_to_response(context)
