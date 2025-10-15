from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Client, CompanyNews, Review, Sale
from .validators import validate_age_18

class CompanyNewsForm(forms.ModelForm):
    class Meta:
        model = CompanyNews
        fields = ['title', 'content', 'image']
        widgets = {
            'title':   forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image':   forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating':  forms.Select(attrs={'class':'form-select'}),
            'comment': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }
        labels = {
            'rating':  'Оценка',
            'comment': 'Комментарий',
        }


class SignUpForm(UserCreationForm):
    email       = forms.EmailField(required=True, label='Email')
    birth_date  = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[validate_age_18]
    )
    phone       = forms.CharField(label='Телефон', max_length=30)

    class Meta:
        model  = User
        fields = ('username','email','birth_date','phone','password1','password2')

    def save(self, commit=True):
        user = super().save(commit)
        Client.objects.create(
            user=user,
            phone=self.cleaned_data['phone'],
            birth_date=self.cleaned_data['birth_date']
        )
        return user


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model  = Client
        fields = ("phone", "birth_date")
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'birth_date': 'Дата рождения',
            'phone':      'Телефон',
        }
        help_texts = {
            'birth_date': 'Укажите дату рождения (18+).',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")                # забираем пользователя
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = user.email

    def clean_birth_date(self):
        dob = self.cleaned_data['birth_date']
        validate_age_18(dob)
        return dob

    def save(self, commit=True):
        client = super().save(commit=commit)
        user   = client.user
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return client

class SaleForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, label="Количество")
    client   = forms.ModelChoiceField(
        queryset=Client.objects.none(),
        label="Клиент",
        required=False,
        help_text="Выберите покупателя"
    )

    class Meta:
        model  = Sale
        fields = ("quantity", "client")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and hasattr(user, "employee_profile"):
            qs = Client.objects.exclude(user=user)
            self.fields["client"].queryset = qs
            self.fields["client"].required = True
        else:
            self.fields.pop("client", None)
