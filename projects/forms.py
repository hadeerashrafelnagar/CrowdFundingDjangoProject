from tracemalloc import start
from django.forms import ModelForm, ValidationError
from django import forms
from .models import *
from django.core.validators import RegexValidator
from django.forms.widgets import CheckboxSelectMultiple
from .models import Project,Categories,ProjectTage
import datetime
from django.template.defaultfilters import slugify
class SearchForm(forms.Form):
    mode = forms.ChoiceField(required=True,choices=(('1',"Tage"),('2',"title")))
    search = forms.CharField(required=True)
class ReportForm(forms.Form):
    content = forms.CharField(required=True)
#=======================================
class ReportFormProject(forms.Form):
    content = forms.CharField(required=True)
    # hadeer
class ReportFormComment(forms.Form):
    content = forms.CharField(required=True)
    # hadeer
class DonationForm(forms.Form):
    amount = forms.IntegerField(required=True)
    # hadeer
class RatingForm(forms.Form):
    rate = forms.IntegerField(required=True)
    # hadeer
    #================================================

class ProjectForm (forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm,self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Categories.objects.all()
        self.fields['category'].widget.attrs.update({'class':'form-control'})
        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = ProjectTage.objects.all()

    class Meta:
        model = Project
        
        fields=('title','details','category','totalTarget','start_date','end_date','tags','image')
        #abels={'title':' ','details':'','category':'Category','target':'','start_date':'','end_date':''}
       
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'details':forms.TextInput(attrs={'class':'form-control'}),
            'totalTarget':forms.NumberInput(attrs={'class':'form-control'}),
            'start_date':forms.DateTimeInput(attrs={'class':'form-control'}),
            'end_date':forms.DateTimeInput(attrs={'class':'form-control'}),
            }
        tags = forms.ModelMultipleChoiceField(
        queryset=ProjectTage.objects.all(),
        widget=forms.CheckboxSelectMultiple
        )
        
 
    def clean(self): 
           cleaned_date=super().clean()
           data =cleaned_date.get('start_date')
           data2= cleaned_date.get('end_date')
           if datetime.datetime.now().date() > data :
                #    print (datetime.datetime.now())
                   print(data)
                   raise ValidationError("start date cannot be a past date")
           elif datetime.datetime.now().date() > data2 :
                 raise ValidationError("end date cannot be a past date")  
           elif  data2 == data :
                raise ValidationError("end date cannot be = start date")  
           
           elif data2 < data :
               raise ValidationError("end date cannot before start date")
           else :
                pass
                 
               
                   
                   
           
               
     
        #Validation #DataFlair

    