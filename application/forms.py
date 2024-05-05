from django import forms
from .models import Proposal

class ProposalForm(forms.ModelForm):
    golden_badge = forms.BooleanField(required=False)
    class Meta:
        model = Proposal
        exclude = [
            'operator_reason', 'specialist_reason', 'comment', 'checker_operator', 'checker_specialist',
            'discount_yu', 'discount_percent', 'discount_athlete', 'altyn_belgi', 'conditionally',
            'contract_file', 'average_rating', 'applicant', 'status', 'random_number',
            'univer_id', 'sync_status', 'sync_comment',
        ]