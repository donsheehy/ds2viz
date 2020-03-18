# Planning for ds_viz

## PDF and PNG Output

Currently svg output is pretty good.
Getting pdf and/or png output would be better for producing good pdfs.

## Styles need to be converted to TOML format.

This will make them easier to read and write.

## Colors Need a consistent format

Sticking with webstandard hex is probably best.
Not sure about opacity?

## Deal properly with margin and padding

These are defined in the style.
It should be possible to pad and margin the sides differently as in html.

We need to decide how margins and padding work for alignment.
Traditionally, padding is a minimum guarantee that is not additive.
