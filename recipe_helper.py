"""Helper function for compact recipe creation."""
def R(name, name_hi, region, state, cat, veg, diff, prep, cook, serves, story, ings, steps, tips=None, cal=0, pro=0, carb=0, fat=0, tags=None):
    return {"name":name,"name_hi":name_hi,"region":region,"state":state,"cat":cat,"veg":veg,
            "diff":diff,"prep":prep,"cook":cook,"serves":serves,"story":story,
            "ingredients":ings,"steps":steps,"tips":tips or [],
            "nutrition":{"cal":cal,"protein":pro,"carbs":carb,"fat":fat},"tags":tags or []}
