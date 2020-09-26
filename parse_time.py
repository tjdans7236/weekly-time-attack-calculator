import yaml
import json
from pathlib import Path
from datetime import timedelta
import logging
import argparse

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def str_to_time(time_str):
    time_split = time_str.split(':')
    
    if len(time_split) > 3:
        LOG.error(
            "Incorrect time format detected!"
            f"{time_str} is not of format minute:second:millisecond"
        )
        raise ValueError
        
    if len(time_split) == 1:
        LOG.error(f"It's impossible to finish a track within a second. Got {time_str}")
        raise ValueError
        
    if len(time_split) == 2:
        time_split.insert(0, '0')
        
    if len(time_split[2]) > 3:
        LOG.error(f"Incorrect format: millisecond can have at most 3 digits")
        raise ValueError
        
    m = int(time_split[0])
    s = int(time_split[1])
    ms = int(time_split[2]) * 10**(3 - len(time_split[2]))
    
    if not ((0 <= m < 60) and (0 <= s < 60) and (0 <= ms < 1000)):
        LOG.error(f"{time_str} is not a valid time!")
        raise ValueError
        
    return timedelta(minutes=m, seconds=s, milliseconds=ms)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file', help="The input time attack records yml file")
    args = parser.parse_args()

    in_file = args.in_file
    out_file = in_file.replace('.yml', '.json')

    with Path('data/name_to_webhook.yml').open('r') as file:
        n2w = yaml.load(file, Loader=yaml.BaseLoader)

    with Path('data').joinpath(in_file).open('r') as file:
        tt = yaml.load(file, Loader=yaml.BaseLoader)

    meta = tt.pop('metadata')

    event_id = meta['event_id']
    track = meta['track']
    event_period = meta['period']

    output = {'version': 3,
     'backups': [{'name': f'Event {event_id}',
       'webhookUrl': 'https://discordapp.com/api/webhooks/735370644858077244/IxHapktYAdoEPCG34sqy6uF2d5ZIrJ0mMW4ILDFVec2dGkyd0dHeUunf4BH8kyrx_VV0',
       'message': {'embeds': [{'title': f'Event #{event_id}',
          'color': 16754513,
          'fields': [{'name': 'Track:', 'value': track},
           {'name': 'Event Period', 'value': event_period},
           {'name': 'Prize',
            'value': 'Fastest Player: **Weekly Dominator**\nMost Improved: **Weekly Genius**'}]},
         {'title': 'Fastest Player',
          'description': "",
          'color': 16754513},
         {'title': 'Most Improved',
          'description': "",
          'color': 16754513}]}}]}

    tt_td = {name: [str_to_time(t) for t in tt[name]] for name in tt}

    t2p = {}
    i2p = {}
    for player in tt_td:
        time_list = tt_td[player]
        best_time = max(time_list)
        if best_time in t2p:
            t2p[best_time].append(player)
        else:
            t2p[best_time] = [player]

        max_time = max(time_list)
        min_time = min(time_list)
        improvement = max_time - min_time
        if improvement in i2p:
            i2p[improvement].append(player)
        else:
            i2p[improvement] = [player]

    with Path('output/example_output.json').open('r') as file:
        output_format = json.load(file)

    fastest_str = "\n".join([f"**{i}.** {n2w[', '.join([p for p in t2p[t]])]} - {str(t + timedelta(microseconds=1))[:-4]}" for i, t in enumerate(sorted(t2p.keys()))])

    LOG.info(f'Fastest Rank:\n{fastest_str}')

    most_improved_str = "\n".join([f"**{i}.** {n2w[', '.join([p for p in i2p[t]])]} - {str(t + timedelta(microseconds=1))[:-4]}" for i, t in enumerate(sorted(i2p.keys(), reverse=True))])

    LOG.info(f'Most Improved Rank:\n{most_improved_str}')

    output['backups'][0]['message']['embeds'][1]['description'] = fastest_str

    output['backups'][0]['message']['embeds'][2]['description'] = most_improved_str

    LOG.info(f'writing results to output/{out_file}')

    with Path('output').joinpath(out_file).open('w') as file:
        json.dump(output, file, indent=4)