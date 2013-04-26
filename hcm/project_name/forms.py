from ajax_select import make_ajax_field
from imagestore.forms import ImageForm
from imagestore.models import Image


class HcmImageForm(ImageForm):
    tags = make_ajax_field(Image, 'tags', 'tag')

    class Meta(object):
        model = Image
        exclude = ('user', 'order')
