#
# Data tables/relationship of Assets:
#    - Asset is a table of the assets
#    - Revision is a table of revisions
#    - AssetRevision relates an Asset to a list of Revisions (ie, AssetRevision.revisions = [list of Revision's])
#
# Data table/relation of Revisions:
#    - Datablock is the types of data in Blender ("Groups", "Actions", "Materials", etc)
#    - Data is a specific Datablock item ("Group.001", "Group.002", "WalkAction", etc)
#    - Datablock.datablocks = [list of Data's]
#    - Blend is a table of blend files
#    - Blend.datablocks = [list of Datablocks]
#
# Data tables/relationship of Shots:
#    - Sequence is a tables of sequences
#    - Shot is a table of shots
#    - Sequence.shots = [list of Shot's]
#
# TODO:
#    - relationship between departments (ex. Model->Surface->Rig):
#         * UI can autoselect downstream/upstream version of asset/shot
#         * Can preview a thumbnail of "latest version of the asset/shot"

from collections import namedtuple
import random
import time
import os

root_path = os.path.dirname(__file__)

# Dummy data

departments = ['model', 'surface', 'rig']
asset_categories = ['prop', 'set', 'character', 'material']
asset_names = ['cone', 'cube', 'cylinder', 'icosphere', 'sphere', 'suzanne', 'torus']
comment_text = ['lots of changes. too much to describe', 'made better', 'approved', 'small fix']
comment_text.append(('this log entry is very long. it contains many things\n'
                     '- lots of changes\n'
                     '- updated uvs\n'
                     '- changed edge loops\n'
                     '- made shader metal\n'))
users = ['vicken.mavlian', 'cristian.kovacs', 'dan.murray']

# tables/data fields for blend file data
blend_datablocks = ['actions', 'groups', 'materials', 'scenes']
Blend = namedtuple('Blend', 'filename datablocks')
Datablock = namedtuple('Datablock', 'name datas')
Data = namedtuple('Data', 'name')

Revision = namedtuple('Revision', 'version date user comment publish thumbnail blend')

# tables/data fields for assets and shots
Asset = namedtuple('Asset', 'name section')
AssetRevision = namedtuple('AssetRevision', 'asset department revisions')
assets = []
asset_revisions = []

shots = []
shot_revisions = []


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
        asset = Asset(name=name, section=random.choice(asset_categories))
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
                thumbnail = asset.name+'.png'
                revision = Revision(version=version, date=date, user=user, comment=comment, publish=publish,
                                    thumbnail=thumbnail, blend=blend)
                revisions.append(revision)

            asset_revision = AssetRevision(asset=asset, department=department, revisions=revisions)
            asset_revisions.append(asset_revision)

    global shots
    global shot_revisions

    shots = []
    shot_revisions = []

    seqs = set()
    for i in sorted(random.sample(range(0,1000, 10), 100)):
        name = str(i).zfill(3)
        sequence = random.choice(range(0, 1000, 100))
        sequence = str(sequence).zfill(3)
        shot = Asset(name=name, section=sequence)
        shots.append(shot)
        seqs.add(sequence)

    for shot in shots:
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
                thumbnail = shot.name+'.png'
                revision = Revision(version=version, date=date, user=user, comment=comment, publish=publish,
                                    thumbnail=thumbnail, blend=blend)
                revisions.append(revision)

            shot_revision = AssetRevision(asset=shot, department=department, revisions=revisions)
            shot_revisions.append(shot_revision)

if __name__ == "__main__":
    pass
