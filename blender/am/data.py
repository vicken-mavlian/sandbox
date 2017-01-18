from collections import namedtuple
import random
import time

departments = ['model', 'surface', 'rig']
categories= ['prop', 'set', 'character']
asset_names = ['cone', 'cube', 'cylinder', 'icosphere', 'sphere', 'suzanne', 'torus']
comment_text = ['lots of changes. too much to describe', 'made better', 'approved', 'small fix']
users = ['vicken.mavlian', 'cristian.kovacs', 'dan.murray']
assets = []
asset_revisions = []

Asset = namedtuple('Asset', 'name thumbnail category')
Revision = namedtuple('Revision', 'version date user comment publish')
AssetRevision = namedtuple('AssetRevision', 'asset department revisions')

def regenerate():
    global assets
    global asset_revisions
    assets = []
    asset_revisions = []

    for name in asset_names:
        asset = Asset(name=name, thumbnail=name+'.png', category=random.choice(categories))
        assets.append(asset)

    for asset in assets:
        for department in departments:
            revisions = []

            # put this time stuff here to make sure each revision is always at a later date
            start = 1480000000
            end = int(time.time())
            for version in ("%03d" % i for i in range(random.randint(1,10))):
                rev_time = random.randint(start, end)
                start = rand_time
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rev_time))
                user = random.choice(users)
                comment = random.choice(comment_text)
                publish = str(random.choice(['True', 'False']))
                revision = Revision(version=version, date=date, user=user, comment=comment, publish=publish)
                revisions.append(revision)

            asset_revision = AssetRevision(asset=asset, department=department, revisions=revisions)
            asset_revisions.append(asset_revision)

if __name__ == "__main__":
    pass
