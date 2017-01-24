from collections import namedtuple
import random
import time
import os

root_path = os.path.dirname(__file__)


departments = ['model', 'surface', 'rig']
categories= ['prop', 'set', 'character']
asset_names = ['cone', 'cube', 'cylinder', 'icosphere', 'sphere', 'suzanne', 'torus']
comment_text = ['lots of changes. too much to describe', 'made better', 'approved', 'small fix']
users = ['vicken.mavlian', 'cristian.kovacs', 'dan.murray']
assets = []
asset_revisions = []

blend_datablocks = ['actions', 'groups', 'materials']

Blend = namedtuple('Blend', 'filename datablocks')
Datablock = namedtuple('Datablock', 'name datas')
Data = namedtuple('Data', 'name')

Asset = namedtuple('Asset', 'name category')
Revision = namedtuple('Revision', 'version date user comment publish thumbnail blend')
AssetRevision = namedtuple('AssetRevision', 'asset department revisions')


def new_blend():
    filenames = ['wip.blend', 'new.blend', 'backup.blend']
    filename = random.choice(filenames)

    datablocks = []
    for blend_datablock in blend_datablocks: # Group, Actions, Materials
        datas = []
        for i in range(random.randint(1,5)):
            name = blend_datablock + '.' + str(i).zfill(3)
            data = Data(name=name)
            datas.append(data)

        datablock = Datablock(name=blend_datablock, datas=datas)
        datablocks.append(datablock)

    blend = Blend(filename=filename, datablocks=datablocks)
    return blend

def regenerate():
    global assets
    global asset_revisions
    assets = []
    asset_revisions = []

    for name in asset_names:
        asset = Asset(name=name, category=random.choice(categories))
        assets.append(asset)

    for asset in assets:
        for department in departments:
            revisions = []

            # put this time stuff here to make sure each revision is always at a later date
            start = 1480000000
            end = int(time.time())
            for version in ("%03d" % i for i in range(random.randint(1,10))):
                blend = new_blend()

                rev_time = random.randint(start, end)
                start = rev_time
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rev_time))
                user = random.choice(users)
                comment = random.choice(comment_text)
                publish = str(random.choice(['True', 'False']))
                thumbnail = asset.name + '.png'
                revision = Revision(version=version, date=date, user=user, comment=comment, publish=publish, thumbnail=thumbnail, blend=blend)
                revisions.append(revision)

            asset_revision = AssetRevision(asset=asset, department=department, revisions=revisions)
            asset_revisions.append(asset_revision)

if __name__ == "__main__":
    pass
