"""
this is an example script to demonstrate how to read and write infotext in stable-diffusion-webui
Reading infotext is typically defined in the ui method
Writing infotext is typically defined in or before the process_batch method
"""
from modules import scripts
import gradio as gr


class Script(scripts.Script):

    def title(self):
        return 'infotext example - basic'

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        # just a simple ui with elements to demonstrate infotext
        with gr.Accordion(label=self.title(), open=False):
            checkbox = gr.Checkbox(label='enable', value=False)
            slider = gr.Slider(label='slider', value=5)
            text = gr.Textbox(label='text', value='some text')
            number = gr.Number(label='number', value=5)

        """
        Read infotex
        
        self.infotext_fields is the list of elements that will be updated with the infotext
        basic use
        (component, infotext_key)
        "infotext_key" is the key webui will look for in the infotext, if not found then the element will not be updated
        this is equivalent to lambda d: d.get('infotext_key)

        custom function
        if can also use a function to get the value if you need more complex logic.
        (component, lambda) or (component, function)
        the function should take the infotext dictionary from webui and return the value for the element.
        if return None then the element will not be updated.

        ---

        Note prior to webui 1.8 theres a bug that if the component default value is int but the infotext value is float
        the issue has been fixed in webui 1.8, but if you are working with older versions you should set the value
        as float even if it might be set to int by the user
            > if a slider ranges between 0-1 and the default is 1 then you should set the value as 1.0 not 1
            > but if only integers are expected then it is fine to set as int
        see fix PR paste infotext cast int as float
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/14523

        """
        infotext_keys = ['infotext slider', 'infotext Text', 'infotext number']

        self.infotext_fields = [
            # example 1: enable the checkbox if any of the keys in infotext_keys is present in the infotext
            (checkbox, lambda d: any(key in d for key in infotext_keys)),
            # example 2: set the slider value to the value of 'infotext slider' key in the infotext
            (slider, 'infotext slider'),  # this is equivalent to lambda d: d.get('infotext slider')
            # example 3: with a default value if not found
            (text, lambda d: d.get('infotext text', 'you can set default value')),
            # example 4: with a default value if not found
            (number, lambda d: d.get('infotext number', None)),
        ]

        return checkbox, slider, text, number

    def process_batch(self, p, *args, **kwargs):
        checkbox, slider, text, number = args
        if checkbox:
            p.extra_generation_params['infotext slider'] = slider
            p.extra_generation_params['infotext text'] = text
            p.extra_generation_params['infotext number'] = number
        """
        Writing infotext
        
        if you wish the infotext to be written to "params.txt"
        so that it works with the button "Read generation parameters from prompt or last generation if prompt is empty into user interface."
        then it need to be written in or this callback Script.process_batch

        however that is only needed to be written in output images can be delayed upto the point where image is written

        to add a infotext a a key value pare p.extra_generation_params dict
        the valuse should only be string int or float

        ---
                
        the key chosen for the infotext should be unique across the base webui and all other extensions
        so it is advised to use a prefix to avoid conflicts.
    
        as mentioned a infotax key does not natively support structural data this could be inconvenient,
        also depends on the use case you might have lots of key values for you extention,
        along with the prefix this could make the info text a bit bloated.
        I provide will prived a solution to most of these issues in the advance version

        in this case "checkbox" is not written to infotext because we can infer it from the other values

        ---

        note: as of webui 1.9 
        the value also suports list and functions
        when a list is pass list[index] will be written to the infotext, the index is the index of the image in the job
        a function can be used if more advance logic is needed

        for details see PR 'create_infotext allow index and callable'
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/15460
        """
