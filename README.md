# sd-webui-infotext-example

> this is an extension for developers it serves no purpose for the end user 

this is an example of how to read and write infotext when developing an extension for [Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

`Infotext` aka `PNG Info`, the purpose of which is to allow an image to be re-creatable by saving the generation parameters in the images itself.

Webui provides an interface to read and write infotext, but its usage is not well documented.

This is an example in the form of extension with inline documentation on how to read and write infotext.

Three examples are provided [`basic`](scripts/infotext_example_basic.py) [`advance`](scripts/infotext_example_advance.py) and [`selectable script`](scripts/infotext_example_selectable_scripts.py).

Read the [`basic`](scripts/infotext_example_advance.py) first then the [`advanced`](scripts/infotext_example_advance.py) or [`selectable scripts`](scripts/infotext_example_selectable_scripts.py) example or if applicable.

[`basic example`](scripts/infotext_example_advance.py) should work for simple extensions.

[`advance example`](scripts/infotext_example_advance.py) is for extensions with lost of info to write and would prefer to write it in a more structured way.

[`selectable script example`](scripts/infotext_example_selectable_scripts.py) is for selectable dropdown scripts, it demonstrates how to allow automatically switch to the script.
