import sys
import time
import random
from workflow import web
from workflow import Workflow

def main(wf):
    user_input = ''.join(wf.args)

    if wf.update_available:
        wf.add_item("An update is available!",
                    autocomplete='workflow:update', valid=False)

    units = wf.cached_data('brreg', max_age=60*60*24) # It's not updating that often, so once a day is fine
    while units is None:
        units = web.get('https://data.brreg.no/enhetsregisteret/api/enheter').json()['_embedded']['enheter']
        time.sleep(1)

    wf.cache_data('brreg', units) # Add to cache
    if 'random' in user_input: # find one random
        l = len(units)
        index = random.randint(0, l-1)
        unit = units[index]
        title = unit['navn']
        num = unit['organisasjonsnummer'] if 'organisasjonsnummer' in unit else -1
        wf.add_item(title, arg=num, valid=(unit > 0))
    else:
        for unit in units:
            title = unit['navn']
            num = unit['organisasjonsnummer'] if 'organisasjonsnummer' in unit else -1
            if user_input.lower() in title.lower():
                wf.add_item(title, arg=num, valid=(unit > 0))    
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'mrlys/alfred-brreg',
        'version': 'v0.1.0',
    })
    sys.exit(wf.run(main))
