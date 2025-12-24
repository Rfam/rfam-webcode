"""
Django forms for the Rfam website.
"""
import re
from django import forms
from django.core.validators import EmailValidator


class AlignmentSubmissionForm(forms.Form):
    """
    Form for accepting alignment submissions.

    Users can submit Stockholm-format alignments for consideration as:
    - A new Rfam family (requires PubMed ID)
    - A replacement alignment for an existing family (requires accession)
    """

    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your name',
            'class': 'form-control'
        }),
        error_messages={'required': 'You must give your name.'}
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your email address',
            'class': 'form-control'
        }),
        error_messages={'required': 'You must give your email address.'}
    )

    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Comments on the alignment.',
            'class': 'form-control',
            'rows': 4
        })
    )

    alignment = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.sto,.stockholm,.txt'
        }),
        error_messages={'required': 'You must upload a Stockholm-format alignment.'}
    )

    new_family = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    accession = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Rfam accession (e.g., RF00001)',
            'class': 'form-control'
        }),
        error_messages={'required': 'You must supply an accession for an existing family.'}
    )

    pmid = forms.CharField(
        max_length=20,
        required=False,
        label='PubMed ID',
        widget=forms.TextInput(attrs={
            'placeholder': 'PubMed ID',
            'class': 'form-control'
        }),
        error_messages={'required': 'You must supply a PMID if this is a new family.'}
    )

    def clean_accession(self):
        """Validate Rfam accession format."""
        accession = self.cleaned_data.get('accession', '')
        new_family = self.data.get('new_family')

        # If new_family is checked, accession is not required
        if new_family:
            return accession

        if not accession:
            raise forms.ValidationError(
                'Must supply a family accession unless this is a new family'
            )

        # Validate accession format: RF##### or RM#####
        if not re.match(r'^R[FM]\d{5}$', accession, re.IGNORECASE):
            raise forms.ValidationError('Not a valid Rfam family accession')

        return accession.upper()

    def clean_pmid(self):
        """Validate PubMed ID."""
        pmid = self.cleaned_data.get('pmid', '')
        new_family = self.data.get('new_family')

        # If new_family is checked, pmid is required
        if new_family and not pmid:
            raise forms.ValidationError(
                'Must supply a PubMed ID if this is a new family'
            )

        # If pmid is provided, validate it's a number
        if pmid and not pmid.isdigit():
            raise forms.ValidationError('Not a valid PubMed ID.')

        return pmid

    def clean_alignment(self):
        """Validate Stockholm-format alignment file."""
        alignment = self.cleaned_data.get('alignment')

        if not alignment:
            raise forms.ValidationError('No valid Stockholm-format file')

        # Check file size (400 bytes to 10MB)
        if alignment.size < 400:
            raise forms.ValidationError(
                'Alignment file is too small (minimum 400 bytes)'
            )
        if alignment.size > 10 * 1024 * 1024:  # 10MB
            raise forms.ValidationError(
                'Alignment file is too large (maximum 10MB)'
            )

        # Read and validate Stockholm format
        try:
            content = alignment.read().decode('utf-8')
            alignment.seek(0)  # Reset file pointer for later use

            lines = content.strip().split('\n')

            if not lines:
                raise forms.ValidationError('Could not read the Stockholm-format file')

            # Check Stockholm format: first line must be "# STOCKHOLM 1.0"
            if not lines[0].strip() == '# STOCKHOLM 1.0':
                raise forms.ValidationError(
                    'Not a valid Stockholm-format file (must start with "# STOCKHOLM 1.0")'
                )

            # Check Stockholm format: last line must be "//"
            if not lines[-1].strip() == '//':
                raise forms.ValidationError(
                    'Not a valid Stockholm-format file (must end with "//")'
                )

        except UnicodeDecodeError:
            raise forms.ValidationError(
                'Could not read the file. Please ensure it is a valid text file.'
            )

        return alignment

    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        new_family = self.data.get('new_family')

        # Dynamically set required based on new_family checkbox
        if new_family:
            # New family: pmid required, accession not required
            if not cleaned_data.get('pmid'):
                self.add_error('pmid', 'You must supply a PMID if this is a new family.')
        else:
            # Existing family: accession required, pmid not required
            if not cleaned_data.get('accession'):
                self.add_error('accession', 'You must supply an accession for an existing family.')

        return cleaned_data
