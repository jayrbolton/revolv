from django import forms

from models import Category, Project


class ProjectForm(forms.ModelForm):
    """
    Form used for the Create and Update Project View. Controls what fields
    the user can access and their basic appearance to the user.
    """

    # for allowing numbers to use commas for thousands separators
    funding_goal = forms.DecimalField(min_value=0, decimal_places=2, localize=True)
    impact_power = forms.FloatField(localize=True)
    # sets the lat and long fields to hidden (clicking on the map updates them)
    location_latitude = forms.DecimalField(widget=forms.HiddenInput())
    location_longitude = forms.DecimalField(widget=forms.HiddenInput())
    # sets the categories list to be hidden and not required (using chosen.js updates it)
    categories_list = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Project
        # fields that need to be filled out
        fields = (
            'title',
            'mission_statement',
            'funding_goal',
            'impact_power',
            'end_date',
            'video_url',
            'cover_photo',
            'org_name',
            'org_about',
            'org_start_date',
            'location',
            'location_latitude',
            'location_longitude',
            'categories_list'
        )

    def clean_categories_list(self):
        """ This method processes the input from the hidden categories list field, which
        is a string of the comma separated values. It parses it and insures all the categories
        are valid, then converts it into an actual list.
        """
        data = self.cleaned_data['categories_list']
        # splits the list and filters out any empty strings
        categories_list = data.strip().split(',')
        categories_list = filter(None, categories_list)
        # checks if all the categories in it are valid
        for category in categories_list:
            if category not in Category.valid_categories:
                raise forms.ValidationError("You have entered an invalid category.")
        return categories_list


class ProjectStatusForm(forms.ModelForm):
    """
    An empty form, used so that one can update the project status through
    the ReviewProjectView
    """
    class Meta:
        model = Project
        # fields that need to be filled out, empty on purpose
        fields = ()


class PostFundingUpdateForm(forms.ModelForm):
    """
    A form for providing post funding updates about a project
    """
    class Meta:
        model = Project
        fields = (
            'post_funding_updates',
            'solar_url',
        )
