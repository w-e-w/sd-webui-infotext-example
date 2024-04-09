"""
this is the selectable script example, you should read the basic version first
"""
from modules import scripts
import gradio as gr


class Script(scripts.Script):

    def title(self):
        return 'infotext example - selectable script'

    def ui(self, is_img2img):
        # this is essentially the same as the basic version without the enable checkbox and comments removed
        slider = gr.Slider(label='slider', value=5)
        text = gr.Textbox(label='text', value='some text')
        number = gr.Number(label='number', value=5)

        self.infotext_fields = [
            (slider, 'infotext slider'),
            (text, lambda d: d.get('infotext text', 'you can set default value')),
            (number, lambda d: d.get('infotext number', None)),
        ]

        return slider, text, number

    def run(self, p, *args, **kwargs):
        slider, text, number = args

        # set p.extra_generation_params['Script'] to the title of your script will allow webui to automatically switch the current script when reading infotext
        p.extra_generation_params['Script'] = self.title()

        p.extra_generation_params['infotext slider'] = slider
        p.extra_generation_params['infotext text'] = text
        p.extra_generation_params['infotext number'] = number

        # normally you would have your processing here, but this is just an infotext example.
