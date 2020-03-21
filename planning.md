# Planning for ds_viz

## Public Launch

- [ ] Get dependencies into `setup.py`
- [ ] put it on pypi
- [ ] do a build test for ds book in fresh pipenv
- [ ] update note in users guide to the data structures book


## Styles need to be converted to TOML format.

This will make them easier to read and write.

## Alignment should happen w.r.t. least common ancestor

## Colors Need a consistent format

Sticking with webstandard hex is probably best.
Not sure about opacity?

## Better Boxes

Sides should be proper attributes.

## Deal properly with margin and padding

These are defined in the style.
It should be possible to pad and margin the sides differently as in html.

We need to decide how margins and padding work for alignment.
Traditionally, padding is a minimum guarantee that is not additive.
Adjacent elements are spaced so the distance is the max of their padding values.

## Primitives updates

Polylines are more primitive than Lines.
It should replace `DP_Line` as the main primitive for lines.

Bezier Curves.  It's time.

## Arrowheads and curve decorations

## Anchors as a function

Especially needed for groups and circles.
For groups, an index should give you access to the anchors of the children.
For circles (and points), a vector should give you an anchor on the boundary.

---

# Done

## PDF and PNG Output

Currently svg output is pretty good.
Getting pdf and/or png output would be better for producing good pdfs.
