"""Preserve the inherited scalar contract when changing bit helper ownership.

George Lydakis with OpenAI Codex assistance. Apache-2.0.
This supplements the hosting ownership/profile audit; it does not replace it.
"""

import json


def same_json(left, right):
    return json.dumps(left, sort_keys=True, separators=(',', ':')) == json.dumps(right, sort_keys=True, separators=(',', ':'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_nine_stage_bit_schedule(schedule):
    """Check the original four-pair level progression and all eight F2 columns."""
    levels = [-1]*4
    columns = [1 << i for i in range(8)]
    stages = []
    bridges = 0
    exchanged = False
    for event in schedule:
        require(not exchanged, 'No event may follow the terminal exchange')
        kind = event['kind']
        if kind == 'local_cover_sweep':
            stage, pair, reverse = event['stage'], event['pair'], event['reverse']
            require(type(stage) is int and 0 <= stage < 9, 'Invalid local stage')
            require(type(pair) is int and 0 <= pair < 4, 'Invalid data pair')
            require(type(reverse) is bool, 'Invalid orientation')
            require(pair == max(0, (stage-1)//2), 'Wrong active pair')
            require(reverse == (stage in (1,3,5,7)), 'Wrong local orientation')
            require(levels[pair] == stage-1, 'Local invocation at the wrong level')
            source, destination = (2*pair+1,2*pair) if reverse else (2*pair,2*pair+1)
            columns[destination] ^= columns[source]
            levels[pair] = stage
            stages.append(stage)
        elif kind == 'idle':
            pair, start, end, rank = (event[k] for k in ['pair','source_level','target_level','rank'])
            require(type(pair) is int and 0 <= pair < 4, 'Invalid idle pair')
            require(all(type(x) is int for x in [start,end,rank]), 'Invalid idle levels/rank')
            require(levels[pair] == start and start <= end <= 8, 'Invalid idle progression')
            require(rank == 7*(end-start), 'Wrong original idle rank')
            levels[pair] = end
        elif kind == 'bridge':
            destination, source = event['dst'], event['src']
            require(all(type(x) is int and 0 <= x < 4 for x in [destination,source]), 'Invalid bridge pair')
            require(destination != source and levels[destination] == levels[source], 'Bridge at incompatible levels')
            require(type(event['coefficient']) is int and event['coefficient'] in (-1,1), 'Invalid bridge coefficient')
            columns[2*destination] ^= columns[2*source]
            columns[2*source+1] ^= columns[2*destination+1]
            bridges += 1
        else:
            require(kind == 'exchange' and levels == [8]*4, 'Missing or premature terminal exchange')
            for pair in range(4):
                columns[2*pair],columns[2*pair+1] = columns[2*pair+1],columns[2*pair]
            exchanged = True
    require(exchanged and stages == list(range(9)) and bridges == 9, 'Incomplete scalar schedule')
    require(columns == [1 << i for i in range(8)], 'Scalar schedule does not restore all columns')
    return columns


def require_hosted_bit_contract(template, parent):
    """Permit only PR442's bit hosting changes; require the audited parent as input.

    Original idle ranks describe the pending coordinate sets. Reduced child ranks
    live in hosting.remainders, validated separately by the ownership audit.
    """
    validate_nine_stage_bit_schedule(parent['schedule'])
    schedule = []
    idle_index = 0
    for event in template['schedule']:
        entry = dict(event)
        if entry['kind'] == 'idle':
            require(type(entry.get('idx')) is int and entry['idx'] == idle_index,
                    'Idle indices must be consecutive and unique')
            del entry['idx']
            idle_index += 1
        schedule.append(entry)
    require(same_json(schedule, parent['schedule']), 'Hosted schedule changed the parent scalar/level contract')
    validate_nine_stage_bit_schedule(schedule)
    require(len(template['calls']) == len(parent['calls']) == 72, 'Wrong invocation count')
    for call, original in zip(template['calls'],parent['calls']):
        require(same_json({k:v for k,v in call.items() if k != 'owners'},
                          {k:v for k,v in original.items() if k != 'owners'}),
                'Hosting changed an invocation header or its order')
    allowed = {'version','live','helper_route','hosting','calls','schedule'}
    require(same_json({k:v for k,v in template.items() if k not in allowed},
                      {k:v for k,v in parent.items() if k not in allowed}),
            'Hosting changed an inherited template field')
    return {'status':'PASS_HOSTED_BIT_PARENT_CONTRACT','scalar_columns':8,'invocations':72,
            'scope':'Parent scalar/level/schedule and invocation binding; ownership audit remains required.'}


if __name__ == '__main__':
    import argparse
    import gzip
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('parent', type=Path)
    parser.add_argument('hosted', type=Path)
    args = parser.parse_args()
    def load(path):
        data = path.read_bytes()
        return json.loads(gzip.decompress(data) if path.suffix == '.gz' else data)
    print(json.dumps(require_hosted_bit_contract(load(args.hosted),load(args.parent)),indent=2))
