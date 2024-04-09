"""
this is the advanced version you should read the basic version first
the advanced version aims to reduce the number of keys written to infotext and allow structural data

the basic idea is to write a single key to infotext that contains a json string,
that allows for multiple key value pairs to be stored in a single master key,
only the master key need to be unique, inertial valuse can be stored in string list or dict,
reduce the number of keys and characters written to infotext

in this example, the master key is 'infotext dict'
"""
from modules import scripts, script_callbacks
import gradio as gr
import json

quote_swap = str.maketrans('\'"', '"\'')
"""
quote_swap is a translation table that swaps single and double quotes in a string
this helps to avoid escaping " in json strings reducing bloat
"""


class Script(scripts.Script):

    def title(self):
        return 'infotext example - advance'

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion(label=self.title(), open=False):
            checkbox = gr.Checkbox(label='enable', value=False)
            slider = gr.Slider(label='slider', value=5)
            text = gr.Textbox(label='text', value='some text')
            number = gr.Number(label='number', value=5)

        def get_infotext(d, key, default=None):
            """
            function to get the value from the infotext
            depending on the structure of your infotext
            add extra logic if needed
            """
            if 'infotext dict' in d:
                return d['infotext dict'].get(key, default)
            return default

        self.infotext_fields = [
            # example 1: enable the checkbox if 'infotext dict' key is present in the infotext
            (checkbox, lambda d: 'infotext dict' in d),
            # the rest is all calls to get_infotext with different keys and defaults
            (slider, lambda d: get_infotext(d, 's')),
            (text, lambda d: get_infotext(d, 't', 'you can set default value')),
            (number, lambda d: get_infotext('n', None)),
        ]

        return checkbox, slider, text, number

    def process_batch(self, p, *args, **kwargs):
        checkbox, slider, text, number = args
        if checkbox:
            infotext = {
                's': slider,
                't': text,
                'n': number
            }
            infotext_qs_json = json.dumps(infotext).translate(quote_swap)
            p.extra_generation_params['infotext dict'] = infotext_qs_json
        """
        same as the basic version but instead of writing multiple keys to infotext
        we encode them as a json string and store them under a single key
        the 'quote_swap' is used to swap single and double quotes to avoid escaping,
        this helps to reduce the number of characters written to infotext and makes it more readable
        
        since the our infotext is under our master key and is separated form the rest of the infotext
        we can use structural however we want like using a single character key for the value
        reducing the total length of the infotext,
        you can of course use a full name as key to improve readability but you don't have to add a prefix
        """


def pares_infotext(infotext, params):
    """
    this function is called when webui pastes infotext,
    hears is where we decode our quote swapped json string back to a dictionary
    """
    try:
        params['infotext dict'] = json.loads(params['infotext dict'].translate(quote_swap))
    except Exception:
        pass


# register the pares_infotext function to be called when infotext is pasted
script_callbacks.on_infotext_pasted(pares_infotext)
