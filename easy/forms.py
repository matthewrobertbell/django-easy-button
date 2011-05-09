from django import forms
from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.helpers import Layout, Fieldset, Row, HTML

class EasyForm(forms.ModelForm):
    class Meta:
        exclude = ('id', )
    def __init__(self, data, id=None, instance=None, form_action=None,
            *args, **kwargs):
        self.helper = FormHelper() 
        if id or instance: 
            if not instance: instance = model_class.g404(user=req.user, pk=id)
            else: instance = instance
            id = instance.id
        if form_action:
            if id: form_action = form_action.replace('{id}', str(id))
            else: form_action = form_action.replace('{id}', '')
            self.helper.form_action = form_action
        submit = Submit('save', 'Create' if not instance else 'Edit')
        super(EasyForm, self).__init__(data, instance=instance, *args, **kwargs)
        self.helper.add_input(submit)

    def save(self, *args, **kwargs):
        if self.instance: self.cleaned_data['id'] = self.instance.id
        return super(EasyForm,self).save(*args,**kwargs)
        

class UserForm(EasyForm):
    def __init__(self, data, user=None, *args, **kwargs):
        super(UserForm, self).__init__(data, *args, **kwargs)
        self.user = user
    class Meta:
        exclude = ('id', 'user',)
    def save(self, *args, **kwargs):
        old_commit = kwargs.get('commit', True)
        new_kwargs = dict(**kwargs)
        new_kwargs['commit'] = False
        to_return = super(UserForm, self).save(*args,**new_kwargs)
        self.instance.user = self.user
        if old_commit: self.instance.save()
        return self.instance
