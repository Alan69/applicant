from import_export import resources
from .models import Proposal, Faculty, Speciality, Subject, Country, Nationality, Area, Citizenship, Region, SpecialityGroup, Subject, IdentificationIssuedBy, DocumentType, FamilyPositionStatus, ForeignLang, DormitoryStatus, EducationCertificateProperties, EducationCertificateType, EducationPlaceStatus, EducationInstitution, FamilyStatus, EducationType, EducationReasonType, EducationReason, EducationLang, EducationForm, EducationLevel, EducationStage, PaymentForm, EducationPeriod, Subject1, Subject2, Gender
from import_export import fields

class ProposalResource(resources.ModelResource):
    new_first_name = fields.Field(attribute='first_name', column_name='Имя')
    new_last_name = fields.Field(attribute='last_name', column_name='Фамилия')
    new_middle_name = fields.Field(attribute='middle_name', column_name='Отчество')
    new_first_name_en = fields.Field(attribute='first_name_en', column_name='Фамилия на английском')
    new_last_name_en = fields.Field(attribute='last_name_en', column_name='Имя на английском')
    new_middle_name_en = fields.Field(attribute='middle_name_en', column_name='Отчество на английском')
    new_phone_number = fields.Field(attribute='phone_number', column_name='Номер телефона')
    new_citizenship = fields.Field(attribute='citizenship', column_name='Гражданство')
    new_nationality = fields.Field(attribute='nationality', column_name='Национальность')
    new_gender = fields.Field(attribute='gender', column_name='Пол')
    new_family_status = fields.Field(attribute='family_status', column_name='Семейное положение')

    new_document_type = fields.Field(attribute='document_type', column_name='Тип документа')
    new_iin = fields.Field(attribute='iin', column_name='ИИН')
    new_identification_number = fields.Field(attribute='identification_number', column_name='№ документа')
    new_identification_issued_by = fields.Field(attribute='identification_issued_by', column_name='Кем выдан')
    new_identification_issue_date = fields.Field(attribute='identification_issue_date', column_name='Дата выдачи')
    new_identification_expiration_date = fields.Field(attribute='identification_expiration_date', column_name='Дата истечение срока')
    new_identification_birth_date = fields.Field(attribute='identification_birth_date', column_name='Дата рождения')
    new_identification_birth_country = fields.Field(attribute='identification_birth_country', column_name='Страна рождения (по удостоверению)')
    new_identification_birth_place = fields.Field(attribute='identification_birth_place', column_name='Место рождения (по удостоверению)')

    new_education_period = fields.Field(attribute='education_period', column_name='Период')
    new_education_type = fields.Field(attribute='education_type', column_name='Тип поступления')
    new_education_stage = fields.Field(attribute='education_stage', column_name='Ступень обучения')
    new_education_level = fields.Field(attribute='education_level', column_name='Уровень обучения')
    new_education_reason = fields.Field(attribute='education_reason', column_name='Основание для поступления')
    new_form_of_study = fields.Field(attribute='form_of_study', column_name='Форма обучения')
    new_lang_of_study = fields.Field(attribute='lang_of_study', column_name='Язык обучения')
    new_payment_form = fields.Field(attribute='payment_form', column_name='Форма оплаты')
    new_faculty = fields.Field(attribute='faculty', column_name='Факультет')
    new_educ_plan = fields.Field(attribute='educ_plan', column_name='Образовательная программа')


    new_basis_for_enrollment = fields.Field(attribute='basis_for_enrollment', column_name='Основание для зачисления')
    new_ict_number = fields.Field(attribute='ict_number', column_name='ТЖК')
    new_testing_certificate_date = fields.Field(attribute='testing_certificate_date', column_name='Дата выдачи сертификата')
    new_testing_certificate_series = fields.Field(attribute='testing_certificate_series', column_name='Серия')
    new_testing_certificate_number = fields.Field(attribute='testing_certificate_number', column_name='Номер')
    new_mathematical_literacy = fields.Field(attribute='mathematical_literacy', column_name='Математическая грамотность')
    new_reading_literacy = fields.Field(attribute='reading_literacy', column_name='Грамотность чтения')
    new_history_of_kazakhstan = fields.Field(attribute='history_of_kazakhstan', column_name='История Казахстана')
    new_profile_subject_1_name = fields.Field(attribute='profile_subject_1_name', column_name='Профильный предмет 1 название')
    new_profile_subject_1 = fields.Field(attribute='profile_subject_1', column_name='Профильный предмет 1 балл')
    new_profile_subject_2_name = fields.Field(attribute='profile_subject_2_name', column_name='Профильный предмет 2 название')
    new_profile_subject_2 = fields.Field(attribute='profile_subject_2', column_name='Профильный предмет 2 балл')
    new_average_rating = fields.Field(attribute='average_rating', column_name='Средняя оценка')
    new_competition_score = fields.Field(attribute='competition_score', column_name='Балл конкурса')
    new_grant_certificate_number = fields.Field(attribute='grant_certificate_number', column_name='№ сертификата гранта (при наличии)')
    new_grant_certificate_date = fields.Field(attribute='grant_certificate_date', column_name='Дата выдачи сертификата')


    new_educational_institution = fields.Field(attribute='educational_institution', column_name='Вид учебного заведения')
    new_institution_name = fields.Field(attribute='institution_name', column_name='Название учебного заведения')
    new_educational_country = fields.Field(attribute='educational_country', column_name='Страна')
    new_educational_area = fields.Field(attribute='educational_area', column_name='Область')
    new_educational_region = fields.Field(attribute='educational_region', column_name='Район')
    new_educational_certificate_type = fields.Field(attribute='educational_certificate_type', column_name='Тип документа')
    new_educational_place_status = fields.Field(attribute='educational_place_status', column_name='Статус населенного пункта, в котором находится учебное заведение')
    new_educational_certificate_date = fields.Field(attribute='educational_certificate_date', column_name='Дата выдачи документа об образовании (аттестат, диплом)')
    new_educational_certificate_series = fields.Field(attribute='educational_certificate_series', column_name='Серия, № документа об образовании (аттестат, диплом)')
    new_educational_certificate_properties = fields.Field(attribute='educational_certificate_properties', column_name='Свойства документа')
    new_golden_badge = fields.Field(attribute='golden_badge', column_name='Алтын белгі')

    new_address_area = fields.Field(attribute='address_area', column_name='Область')
    new_address_region = fields.Field(attribute='address_region', column_name='Район')
    new_address_city = fields.Field(attribute='address_city', column_name='Город, село')
    new_address_street = fields.Field(attribute='address_street', column_name='Улица')
    new_address_house = fields.Field(attribute='address_house', column_name='Дом')
    new_address_apartment = fields.Field(attribute='address_apartment', column_name='Квартира')


    new_register_address_area = fields.Field(attribute='register_address_area', column_name='Область')
    new_register_address_region = fields.Field(attribute='register_address_region', column_name='Район')
    new_register_address_city = fields.Field(attribute='register_address_city', column_name='Город, село')
    new_register_address_street = fields.Field(attribute='register_address_street', column_name='Улица')
    new_register_address_house = fields.Field(attribute='register_address_house', column_name='Дом')
    new_register_address_apartment = fields.Field(attribute='register_address_apartment', column_name='Квартира')


    new_family_position_status = fields.Field(attribute='family_position_status', column_name='Семейный статус')
    new_father_last_name = fields.Field(attribute='father_last_name', column_name='Фамилия отца')
    new_father_first_name = fields.Field(attribute='father_first_name', column_name='Имя отца')
    new_father_middle_name = fields.Field(attribute='father_middle_name', column_name='Отчество отца')
    new_father_profession = fields.Field(attribute='father_profession', column_name='Профессия отца')
    new_father_work = fields.Field(attribute='father_work', column_name='Место работы отца')
    new_father_phone_number = fields.Field(attribute='father_phone_number', column_name='Номер телефона отца')

    new_mother_last_name = fields.Field(attribute='mother_last_name', column_name='Фамилия матери')
    new_mother_first_name = fields.Field(attribute='mother_first_name', column_name='Имя матери')
    new_mother_middle_name = fields.Field(attribute='mother_middle_name', column_name='Отчество матери')
    new_mother_profession = fields.Field(attribute='mother_profession', column_name='Профессия матери')
    new_mother_work = fields.Field(attribute='mother_work', column_name='Место работы матери')
    new_mother_phone_number = fields.Field(attribute='mother_phone_number', column_name='Номер телефона матери')

    new_dormitory = fields.Field(attribute='dormitory', column_name='Общежитие')
    new_english_level = fields.Field(attribute='english_level', column_name='Изучаемый иностранный язык')


    new_discount_yu = fields.Field(attribute='discount_yu', column_name='Наименование скидки')
    new_discount_percent = fields.Field(attribute='discount_percent', column_name='Скидка %')
    new_discount_sport = fields.Field(attribute='discount_sport', column_name='Скидки спортсменам')
    new_conditionally = fields.Field(attribute='conditionally', column_name='Условно')
    new_checker_operator = fields.Field(attribute='checker_operator', column_name='Оператор')
    new_operator_reason = fields.Field(attribute='checker_operator', column_name='Статус Оператора')
    new_checker_specialist = fields.Field(attribute='checker_specialist', column_name='Специалист')
    new_specialist_reason = fields.Field(attribute='checker_specialist', column_name='Статус Специалиста')

    class Meta:
        model = Proposal
        fields = ('new_first_name','new_dormitory', 'new_nationality' )
        use_bulk = True


    def dehydrate_new_conditionally(self, proposal):
        # Здесь вы можете изменить значение поля dormitory
        # в соответствии с вашими требованиями
        if proposal.conditionally == 'yes':
            return 'да'
        elif proposal.conditionally == 'no':
            return 'нет'
        else:
            return ''


    def dehydrate_new_golden_badge(self, proposal):
        if proposal.golden_badge:
            return 'Да'
        else:
            return 'Нет'

    def dehydrate_new_discount_yu(self, proposal):
        # Здесь вы можете изменить значение поля dormitory
        # в соответствии с вашими требованиями
        if proposal.discount_yu == 'my':
            return 'Мой выбор YU'
        elif proposal.discount_yu == 'sport':
            return 'Спорт'
        elif proposal.discount_yu == 'gold':
            return 'Алтын белгі'
        else:
            return ''


    def dehydrate_new_discount_sport(self, proposal):
        if proposal.discount_sport == 'master':
            return 'Мастер спорта'
        elif proposal.discount_sport == 'kms':
            return 'КМС'
        else:
            return ''


    def dehydrate_new_identification_birth_date(self, proposal):
        if proposal.identification_birth_date:
            return proposal.identification_birth_date.strftime('%d.%m.%Y')
        return ''


    def dehydrate_new_grant_certificate_date(self, proposal):
        if proposal.grant_certificate_date:
            return proposal.grant_certificate_date.strftime('%d.%m.%Y')
        return ''

    def dehydrate_new_testing_certificate_date(self, proposal):
        if proposal.testing_certificate_date:
            return proposal.testing_certificate_date.strftime('%d.%m.%Y')
        return ''

    def dehydrate_new_educational_certificate_date(self, proposal):
        if proposal.educational_certificate_date:
            return proposal.educational_certificate_date.strftime('%d.%m.%Y')
        return ''

    def dehydrate_new_identification_issue_date(self, proposal):
        if proposal.identification_issue_date:
            return proposal.identification_issue_date.strftime('%d.%m.%Y')
        return ''


    def dehydrate_new_identification_expiration_date(self, proposal):
        if proposal.identification_expiration_date:
            return proposal.identification_expiration_date.strftime('%d.%m.%Y')
        return ''



class FacultyResource(resources.ModelResource):
    class Meta:
        model = Faculty

class SpecialityResource(resources.ModelResource):
    class Meta:
        model = Speciality

class SpecialityGroupResource(resources.ModelResource):
    class Meta:
        model = SpecialityGroup


class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject


class CountryResource(resources.ModelResource):
    class Meta:
        model = Country


class NationalityResource(resources.ModelResource):
    class Meta:
        model = Nationality


class AreaResource(resources.ModelResource):
    class Meta:
        model = Area


class RegionResource(resources.ModelResource):
    class Meta:
        model = Region


class CitizenshipResource(resources.ModelResource):
    class Meta:
        model = Citizenship


class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject


class EducationPeriodResource(resources.ModelResource):
    class Meta:
        model = EducationPeriod


class PaymentFormResource(resources.ModelResource):
    class Meta:
        model = PaymentForm


class EducationStageResource(resources.ModelResource):
    class Meta:
        model = EducationStage

class EducationLevelResource(resources.ModelResource):
    class Meta:
        model = EducationLevel


class EducationFormResource(resources.ModelResource):
    class Meta:
        model = EducationForm


class EducationLangResource(resources.ModelResource):
    class Meta:
        model = EducationLang


class EducationReasonResource(resources.ModelResource):
    class Meta:
        model = EducationReason

class EducationReasonTypeResource(resources.ModelResource):
    class Meta:
        model = EducationReasonType


class EducationTypeResource(resources.ModelResource):
    class Meta:
        model = EducationType


class FamilyStatusResource(resources.ModelResource):
    class Meta:
        model = FamilyStatus


class EducationInstitutionResource(resources.ModelResource):
    class Meta:
        model = EducationInstitution


class EducationPlaceStatusResource(resources.ModelResource):
    class Meta:
        model = EducationPlaceStatus


class EducationCertificateTypeResource(resources.ModelResource):
    class Meta:
        model = EducationCertificateType


class EducationCertificatePropertiesResource(resources.ModelResource):
    class Meta:
        model = EducationCertificateProperties


class DormitoryStatusResource(resources.ModelResource):
    class Meta:
        model = DormitoryStatus


class ForeignLangResource(resources.ModelResource):
    class Meta:
        model = ForeignLang


class FamilyPositionStatusResource(resources.ModelResource):
    class Meta:
        model = FamilyPositionStatus


class DocumentTypeResource(resources.ModelResource):
    class Meta:
        model = DocumentType


class GenderTypeResource(resources.ModelResource):
    class Meta:
        model = Gender


class IdentificationIssuedByResource(resources.ModelResource):
    class Meta:
        model = IdentificationIssuedBy


class Subject1Resource(resources.ModelResource):
    class Meta:
        model = Subject1


class Subject2Resource(resources.ModelResource):
    class Meta:
        model = Subject2
