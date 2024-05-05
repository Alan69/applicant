from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from . import models
from django import forms
from .models import Proposal,Faculty, CustomUser, Speciality, Subject, Country, Nationality, Area, Citizenship, Region, SpecialityGroup, IdentificationIssuedBy, DocumentType, FamilyPositionStatus, ForeignLang, DormitoryStatus, EducationCertificateProperties, EducationCertificateType, EducationPlaceStatus, EducationInstitution, FamilyStatus, EducationType, EducationReasonType, EducationReason, EducationLang, EducationForm, EducationLevel, EducationStage, EducationStage, PaymentForm, EducationPeriod, IdentificationIssuedBy, Subject1, Subject2, Gender
from docxtpl import DocxTemplate
from django.template.defaultfilters import date
from django.forms import ModelForm, ModelChoiceField
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.admin import ExportMixin
from .resources import ProposalResource
from django.utils import timezone
from django.forms.widgets import DateInput
from django.core.validators import RegexValidator, MaxLengthValidator
from django.contrib.admin.models import LogEntry
from django.core.cache import cache
from django.http import HttpResponse

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    list_filter = ['action_flag']
    search_fields = ['object_repr', 'change_message', 'user__username']
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']

class UniverIdFilter(SimpleListFilter):
    title = 'Идентификатор Univer'
    parameter_name = 'univer_id'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Присутствует'),
            ('false', 'Отсутствует'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(univer_id__isnull=False)
        elif self.value() == 'false':
            return queryset.filter(univer_id__isnull=True)

        return queryset


class CustomAdminFileUploadForm(forms.ModelForm):
    # Установите максимальный размер файла до 50 МБ (в байтах)
    max_file_size = 50 * 1024 * 1024  # 50 МБ в байтах

    def clean_contract_file(self):
        contract_file = self.cleaned_data.get('contract_file')
        if contract_file and contract_file.size > self.max_file_size:
            raise forms.ValidationError('Максимальный размер файла должен быть не больше 50 МБ.')
        return contract_file

    def clean_check_file(self):
        check_file = self.cleaned_data.get('check_file')
        if check_file and check_file.size > self.max_file_size:
            raise forms.ValidationError('Максимальный размер файла должен быть не больше 50 МБ.')
        return check_file

    class Meta:
        model = Proposal
        fields = '__all__'


class ProposalForm(CustomAdminFileUploadForm):
    series_max_length = MaxLengthValidator(limit_value=10, message="Серия должна содержать максимум 10 символов.")
    educational_certificate_series = forms.CharField(max_length=10, label='Серия', validators=[series_max_length])
    iin_regex = RegexValidator(
        regex=r'^\d{12}$',
        message="ИИН должен содержать 12 цифр.'"
    )
    iin = forms.CharField(validators=[iin_regex], max_length=12, label='ИИН')
    latin_chars_validator = RegexValidator(
        regex=r'^[a-zA-Z]*$',
        message="Введите только латинские буквы."
    )
    first_name_en = forms.CharField(max_length=100, label='Фамилия на английском', validators=[latin_chars_validator])
    last_name_en = forms.CharField(max_length=100, label='Имя на английском', validators=[latin_chars_validator])
    middle_name_en = forms.CharField(max_length=100, label='Отчество на английском', validators=[latin_chars_validator], required=False)
    education_period = forms.ModelChoiceField(
        queryset=EducationPeriod.objects.all(), label='Период', required=True)
    education_type = forms.ModelChoiceField(
        queryset=EducationType.objects.all(), label='Тип поступления', required=True)
    education_level = forms.ModelChoiceField(
        queryset=EducationLevel.objects.all(), label='Уровень обучения', required=True)
    education_reason = forms.ModelChoiceField(
        queryset=EducationReason.objects.all(), label='Основание для поступления', required=True)

    class Meta:
        model = Proposal
        fields = '__all__'


@admin.action(description='Сбросить статус синхронизации')
def reset_sync_status(modeladmin, request, queryset):
    queryset.update(sync_status=Proposal.NOT_SYNCED, sync_comment=None)

@admin.action(description='Сгенерировать заявление')
def generate_word(modeladmin, request, queryset):
    # Fetch data from the Proposal model
    proposal = queryset.first()  # You may adjust this query based on your needs

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
    response["Content-Disposition"] = 'filename="zayavlenie.docx"'
    
    template.render(data)
    template.save(response)
    
    return response

@admin.action(description='Сгенерировать договор')
def get_dogovor(modeladmin, request, queryset):
    proposal = queryset.first()  # You may adjust this query based on your needs

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
    response["Content-Disposition"] = 'filename="dogovor.docx"'
    
    template.render(data)
    template.save(response)
    
    return response

@admin.register(Proposal)
class ProposalAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProposalResource
    form = ProposalForm

    list_display = [
        'random_number', 'first_name', 'last_name', 'middle_name', 'faculty', 'univer_id', 'status', 'sync_status',
    ]
    list_filter = ['status', 'conditionally', 'educ_plan', 'sync_status', UniverIdFilter]
    search_fields = ['first_name', 'last_name', 'random_number', 'iin']
    actions = [reset_sync_status, generate_word, get_dogovor]
    list_select_related = [
        'applicant', 'form_of_study', 'lang_of_study', 'payment_form', 'faculty',
        'educ_plan_group', 'educ_plan', 'citizenship', 'nationality', 'gender', 'family_status',
        'educational_institution', 'educational_country', 'educational_area', 'educational_region',
        'educational_place_status', 'educational_certificate_type', 'dormitory', 'english_level',
        'identification_issued_by', 'identification_birth_country', 'address_area', 'address_region',
        'register_address_area', 'register_address_region',
    ]

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='operator').exists():
            return ['sync_comment', 'sync_status', 'univer_id']
        elif request.user.groups.filter(name='specialist').exists():
            return ['operator_reason', 'checker_operator','sync_comment', 'sync_status', 'univer_id']
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        user = request.user
        if user.groups.filter(name='operator').exists():
            obj.checker_operator = request.user
            if obj.specialist_reason:
                return
            if obj.operator_reason == 'accepted':
                obj.status = 'checking'
            obj.save()
        elif user.groups.filter(name='specialist').exists():
            obj.checker_specialist = request.user
            if obj.specialist_reason == 'accepted':
                obj.status = 'accepted'
            elif obj.specialist_reason == 'rejeted':
                obj.status = 'rejeted'
            obj.save()
        elif user.is_superuser:
            obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='specialist').exists():
            qs = qs.filter(faculty__in=request.user.faculty.all())
        elif request.user.groups.filter(name='operator').exists():
            qs = qs.filter(faculty__in=request.user.faculty.all())
        return qs

    def get_list_filter(self, request):
        # Get the list of filters defined in the parent class
        list_filter = super().get_list_filter(request)
        # Check if the current user belongs to the "manager" group
        list_filter = ['status', 'conditionally', 'educ_plan', 'conditionally', 'discount_yu', 'faculty',  'golden_badge',]
        if request.user.groups.filter(name='manager').exists():
            # Add additional filters to be shown only to managers
            list_filter = ['status', 'conditionally', 'educ_plan', 'conditionally', 'discount_yu', 'faculty',  'golden_badge',]

        return list_filter
    
    fieldsets = (
                ('Личные данные', {'fields': ('first_name', 'last_name',  'middle_name', 'first_name_en', 'last_name_en', 'middle_name_en', 'phone_number', 'citizenship', 'nationality', 'gender', 'family_status'  )}),
                ('Паспортные данные', {'fields': ('document_type', 'iin', 'identification_number', 'identification_issued_by', 'identification_issue_date', 'identification_expiration_date', 'identification_birth_date', 'identification_birth_place', 'identification_birth_country')}),
                ('Образовательная программа', {'fields': ('education_period','education_type','education_stage','education_level','education_reason','form_of_study','lang_of_study', 'payment_form',  'faculty', 'educ_plan_group', 'educ_plan')}),
                ('Данные сертификата ЕНТ, КТ или IELTS', {'fields': ('basis_for_enrollment', 'ict_number', 'testing_certificate_date', 'testing_certificate_series', 'testing_certificate_number', 'mathematical_literacy', 'reading_literacy', 'history_of_kazakhstan', 'profile_subject_1_name', 'profile_subject_1', 'profile_subject_2_name', 'profile_subject_2', 'average_rating', 'competition_score', 'grant_certificate_number', 'grant_certificate_date', )}),
                ('Данные учебного заведения', {'fields': ('educational_institution', 'institution_name', 'educational_country', 'educational_area', 'educational_region', 'educational_place_status', 'educational_certificate_type', 'educational_certificate_properties', 'educational_certificate_date', 'educational_certificate_series', 'golden_badge', 'golden_badge_file', )}),
                ('Адрес проживания', {'fields': ('address_area', 'address_region', 'address_city', 'address_street', 'address_house', 'address_apartment')}),
                ('Адрес прописки', {'fields': ('register_address_area', 'register_address_region', 'register_address_city', 'register_address_street', 'register_address_house', 'register_address_apartment')}),
                ('Дополнительные данные', {'fields': ('family_position_status', 'family_position_file', 'father_last_name','parent_type', 'father_first_name','father_middle_name', 'father_profession', 'father_work', 'father_phone_number', 'mother_last_name', 'mother_first_name','mother_middle_name', 'mother_profession', 'mother_work', 'mother_phone_number','dormitory','english_level',)}),
                ('Договор', {'fields': ('discount_yu', 'discount_percent', 'discount_sport', 'conditionally', 'contract_file', 'check_file', 'operator_reason',)}),
                ('Статус синхронизации', {'fields': ('sync_status', 'univer_id',  'sync_comment')}),
            )
            

    def get_fieldsets(self, request, obj=None):
        user = request.user
        
        if user.groups.filter(name='operator').exists():
            fieldsets = (
                ('Личные данные', {'fields': ('first_name', 'last_name',  'middle_name', 'first_name_en', 'last_name_en', 'middle_name_en', 'phone_number', 'citizenship', 'nationality', 'gender', 'family_status'  )}),
                ('Паспортные данные', {'fields': ('document_type', 'iin', 'identification_number', 'identification_issued_by', 'identification_issue_date', 'identification_expiration_date', 'identification_birth_date', 'identification_birth_place', 'identification_birth_country')}),
                ('Образовательная программа', {'fields': ('education_period','education_type','education_stage','education_level','education_reason','form_of_study','lang_of_study', 'payment_form',  'faculty', 'educ_plan_group', 'educ_plan')}),
                ('Данные сертификата ЕНТ, КТ или IELTS', {'fields': ('basis_for_enrollment', 'ict_number', 'testing_certificate_date', 'testing_certificate_series', 'testing_certificate_number', 'mathematical_literacy', 'reading_literacy', 'history_of_kazakhstan', 'profile_subject_1_name', 'profile_subject_1', 'profile_subject_2_name', 'profile_subject_2', 'average_rating', 'competition_score', 'grant_certificate_number', 'grant_certificate_date', )}),
                ('Данные учебного заведения', {'fields': ('educational_institution', 'institution_name', 'educational_country', 'educational_area', 'educational_region', 'educational_place_status', 'educational_certificate_type', 'educational_certificate_properties', 'educational_certificate_date', 'educational_certificate_series', 'golden_badge', 'golden_badge_file', )}),
                ('Адрес проживания', {'fields': ('address_area', 'address_region', 'address_city', 'address_street', 'address_house', 'address_apartment')}),
                ('Адрес прописки', {'fields': ('register_address_area', 'register_address_region', 'register_address_city', 'register_address_street', 'register_address_house', 'register_address_apartment')}),
                ('Дополнительные данные', {'fields': ('family_position_status', 'family_position_file', 'father_last_name','parent_type', 'father_first_name','father_middle_name', 'father_profession', 'father_work', 'father_phone_number', 'mother_last_name', 'mother_first_name','mother_middle_name', 'mother_profession', 'mother_work', 'mother_phone_number','dormitory','english_level',)}),
                ('Договор', {'fields': ('discount_yu', 'discount_percent', 'discount_sport', 'conditionally', 'contract_file', 'check_file', 'operator_reason',)}),
                ('Статус синхронизации', {'fields': ('sync_status', 'univer_id',  'sync_comment')}),
            )
        elif user.groups.filter(name='specialist').exists():
            fieldsets = (
                ('Личные данные', {'fields': ('first_name', 'last_name',  'middle_name', 'first_name_en', 'last_name_en', 'middle_name_en', 'phone_number', 'citizenship', 'nationality', 'gender', 'family_status'  )}),
                ('Паспортные данные', {'fields': ('document_type', 'iin', 'identification_number', 'identification_issued_by', 'identification_issue_date', 'identification_expiration_date', 'identification_birth_date', 'identification_birth_place', 'identification_birth_country')}),
                ('Образовательная программа', {'fields': ('education_period','education_type','education_stage','education_level','education_reason','form_of_study', 'lang_of_study', 'payment_form',  'faculty', 'educ_plan_group', 'educ_plan')}),
                ('Данные сертификата ЕНТ, КТ или IELTS', {'fields': ('basis_for_enrollment', 'ict_number', 'testing_certificate_date', 'testing_certificate_series', 'testing_certificate_number', 'mathematical_literacy', 'reading_literacy', 'history_of_kazakhstan', 'profile_subject_1_name', 'profile_subject_1', 'profile_subject_2_name', 'profile_subject_2','average_rating', 'competition_score', 'grant_certificate_number', 'grant_certificate_date', )}),
                ('Данные учебного заведения', {'fields': ('educational_institution', 'institution_name', 'educational_country', 'educational_area', 'educational_region', 'educational_place_status', 'educational_certificate_type', 'educational_certificate_properties', 'educational_certificate_date', 'educational_certificate_series', 'golden_badge', 'golden_badge_file', )}),
                ('Адрес проживания', {'fields': ('address_area', 'address_region', 'address_city', 'address_street', 'address_house', 'address_apartment')}),
                ('Адрес прописки', {'fields': ('register_address_area', 'register_address_region', 'register_address_city', 'register_address_street', 'register_address_house', 'register_address_apartment')}),
                ('Дополнительные данные', {'fields': ('family_position_status', 'family_position_file', 'father_last_name','parent_type', 'father_first_name','father_middle_name', 'father_profession', 'father_work', 'father_phone_number', 'mother_last_name', 'mother_first_name','mother_middle_name', 'mother_profession', 'mother_work', 'mother_phone_number','dormitory','english_level',)}),
                ('Договор', {'fields': ('discount_yu', 'discount_percent', 'discount_sport', 'conditionally', 'contract_file', 'check_file', 'operator_reason', 'checker_operator', 'specialist_reason',)}),
                ('Статус синхронизации', {'fields': ('sync_status', 'univer_id', 'sync_comment')}),
            )
        elif user.groups.filter(name='manager').exists():
            fieldsets = (
                ('Личные данные', {'fields': ('first_name', 'last_name',  'middle_name', 'first_name_en', 'last_name_en', 'middle_name_en', 'phone_number', 'citizenship', 'nationality', 'gender', 'family_status'  )}),
                ('Паспортные данные', {'fields': ('document_type', 'iin', 'identification_number', 'identification_issued_by', 'identification_issue_date', 'identification_expiration_date', 'identification_birth_date', 'identification_birth_place', 'identification_birth_country')}),
                ('Образовательная программа', {'fields': ('education_period','education_type','education_stage','education_level','education_reason','form_of_study', 'lang_of_study', 'payment_form',  'faculty', 'educ_plan_group', 'educ_plan')}),
                ('Данные сертификата ЕНТ, КТ или IELTS', {'fields': ('basis_for_enrollment', 'ict_number', 'testing_certificate_date', 'testing_certificate_series', 'testing_certificate_number', 'mathematical_literacy', 'reading_literacy', 'history_of_kazakhstan', 'profile_subject_1_name', 'profile_subject_1', 'profile_subject_2_name', 'profile_subject_2', 'average_rating','competition_score', 'grant_certificate_number', 'grant_certificate_date', )}),
                ('Данные учебного заведения', {'fields': ('educational_institution', 'institution_name', 'educational_country', 'educational_area', 'educational_region', 'educational_place_status', 'educational_certificate_type', 'educational_certificate_properties', 'educational_certificate_date', 'educational_certificate_series', 'golden_badge', 'golden_badge_file', )}),
                ('Адрес проживания', {'fields': ('address_area', 'address_region', 'address_city', 'address_street', 'address_house', 'address_apartment')}),
                ('Адрес прописки', {'fields': ('register_address_area', 'register_address_region', 'register_address_city', 'register_address_street', 'register_address_house', 'register_address_apartment')}),
                ('Дополнительные данные', {'fields': ('family_position_status', 'family_position_file', 'father_last_name','parent_type', 'father_first_name','father_middle_name', 'father_profession', 'father_work', 'father_phone_number', 'mother_last_name', 'mother_first_name','mother_middle_name', 'mother_profession', 'mother_work', 'mother_phone_number','dormitory','english_level',)}),
                ('Договор', {'fields': ('discount_yu', 'discount_percent', 'discount_sport', 'conditionally', 'contract_file', 'check_file', 'operator_reason', 'checker_operator', 'specialist_reason', 'checker_specialist',)}),
                ('Статус синхронизации', {'fields': ('sync_status', 'univer_id', 'sync_comment')}),
            )
        else:
            fieldsets = super().get_fieldsets(request, obj)
        return fieldsets


@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name_ru']
    search_fields = ['name_ru']


@admin.register(Speciality)
class SpecialityAdmin(ImportExportModelAdmin):
    list_display = ['id', 'cipher', 'speciality_group', 'name_ru',]
    search_fields = ['name_ru']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='specialist').exists() or request.user.groups.filter(name='operator').exists():
            faculty_ids = request.user.faculty.values_list('id', flat=True)
            qs = qs.filter(speciality_group__faculty__in=faculty_ids)
        return qs


@admin.register(SpecialityGroup)
class SpecialityGroupAdmin(ImportExportModelAdmin):
    list_display = ['id', 'cipher', 'education_stage', 'faculty', 'name_ru',]
    search_fields = ['name_ru']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='specialist').exists() or request.user.groups.filter(name='operator').exists():
            faculty_ids = request.user.faculty.values_list('id', flat=True)
            qs = qs.filter(faculty__in=faculty_ids)
        return qs


@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = ['name_ru']
    search_fields = ['name_ru']


@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
    list_display = ['name_ru']
    search_fields = ['name_ru']


class NationalityAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']


admin.site.register(Nationality, NationalityAdmin)


class AreaAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name_ru', ]
    search_fields = ['name_ru']


admin.site.register(Area, AreaAdmin)


class RegionAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']


admin.site.register(Region, RegionAdmin)


class CitizenshipAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']


admin.site.register(Citizenship, CitizenshipAdmin)


class IdentificationIssuedByAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']


admin.site.register(IdentificationIssuedBy,IdentificationIssuedByAdmin)


class DocumentTypeAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']


admin.site.register(DocumentType, DocumentTypeAdmin)


class FamilyPositionStatusAdmin(ImportExportModelAdmin):
    list_display = ['id', 'external_id', 'name_ru', ]
    search_fields = ['name_ru']


admin.site.register(FamilyPositionStatus, FamilyPositionStatusAdmin)


class ForeignLangAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']


admin.site.register(ForeignLang, ForeignLangAdmin)


class DormitoryStatusAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']


admin.site.register(DormitoryStatus, DormitoryStatusAdmin)


class EducationCertificatePropertiesAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']


admin.site.register(EducationCertificateProperties, EducationCertificatePropertiesAdmin)


class EducationCertificateTypeAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationCertificateType, EducationCertificateTypeAdmin)



class EducationPlaceStatusAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationPlaceStatus, EducationPlaceStatusAdmin)




class EducationInstitutionAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationInstitution, EducationInstitutionAdmin)



class FamilyStatusAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(FamilyStatus, FamilyStatusAdmin)



class EducationTypeAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationType, EducationTypeAdmin)



class EducationReasonTypeAdmin(ImportExportModelAdmin):
    list_display = ['id', 'external_id',  'name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationReasonType, EducationReasonTypeAdmin)



class EducationReasonAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationReason, EducationReasonAdmin)


class EducationLangAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationLang, EducationLangAdmin)


class EducationFormAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationForm, EducationFormAdmin)


class EducationLevelAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationLevel, EducationLevelAdmin)

class EducationStageAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationStage, EducationStageAdmin)


class GenderAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(Gender, GenderAdmin)



class PaymentFormAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(PaymentForm, PaymentFormAdmin)


class CustomUserAdmin(ImportExportModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'email']
    search_fields = ['last_name', 'first_name',]

admin.site.register(CustomUser, CustomUserAdmin)



class EducationPeriodAdmin(ImportExportModelAdmin):
    list_display = ['name_ru', ]
    search_fields = ['name_ru']

admin.site.register(EducationPeriod, EducationPeriodAdmin)


class Subject1Admin(ImportExportModelAdmin):
    list_display = [ 'id', 'speciality', 'subject1',  ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='specialist').exists() or request.user.groups.filter(name='operator').exists():
            faculty_ids = request.user.faculty.values_list('id', flat=True)
            qs = qs.filter(speciality__speciality_group__faculty__in=faculty_ids)
        return qs


admin.site.register(Subject1, Subject1Admin)


class Subject2Admin(ImportExportModelAdmin):
    list_display = ['speciality','subject2', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='specialist').exists() or request.user.groups.filter(name='operator').exists():
            faculty_ids = request.user.faculty.values_list('id', flat=True)
            qs = qs.filter(speciality__speciality_group__faculty__in=faculty_ids)
        return qs


admin.site.register(Subject2, Subject2Admin)
