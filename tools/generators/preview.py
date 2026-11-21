import glob, os, sys, json
from PIL import Image, ImageChops
base='src/main/resources/assets/femboyequipment/textures'
def tint(im, rgb):
    t=Image.new('RGBA', im.size, rgb+(255,))
    out=ImageChops.multiply(im, t); out.putalpha(im.getchannel('A')); return out
def default(name):
    m=json.load(open(f'src/main/resources/assets/femboyequipment/items/{name}.json'))['model']
    if 'tints' not in m: return None
    c=m['tints'][0]['default'] & 0xFFFFFF
    return ((c>>16)&255,(c>>8)&255,c&255)
def comp(name, rgb):
    im=Image.open(f'{base}/item/{name}.png').convert('RGBA')
    if rgb is None: rgb=default(name) or (255,255,255)
    ov=f'{base}/item/{name}_overlay.png'
    if os.path.exists(ov):
        im=tint(im,rgb); im.alpha_composite(Image.open(ov).convert('RGBA'))
    return im
names=sorted(os.path.basename(p)[:-4] for p in glob.glob(base+'/item/*.png') if not p.endswith('_overlay.png'))
rows=[None,(120,170,255)]
sheet=Image.new('RGBA',(len(names)*104+104*2, 2*104),(55,55,65,255))
for r,rgb in enumerate(rows):
    for n,name in enumerate(names):
        sheet.alpha_composite(comp(name,rgb).resize((96,96),Image.NEAREST),(n*104+4,r*104+4))
for n,b in enumerate(['pastel_pink_bricks','ribbon_block']):
    tile=Image.open(f'{base}/block/{b}.png').convert('RGBA')
    t2=Image.new('RGBA',(32,32));[t2.paste(tile,(x,y)) for x in (0,16) for y in (0,16)]
    sheet.alpha_composite(t2.resize((96,96),Image.NEAREST),((len(names)+n)*104+4,4))
sheet.save(sys.argv[1]+'/sheet.png')
arm=[p for p in sorted(glob.glob(base+'/entity/equipment/*/*.png')) if not p.endswith('_overlay.png')]
s2=Image.new('RGBA',(4*264,((len(arm)+3)//4)*136),(120,120,130,255))
for n,p in enumerate(arm):
    im=tint(Image.open(p).convert('RGBA'),default(os.path.basename(p)[:-4])); im.alpha_composite(Image.open(p[:-4]+'_overlay.png').convert('RGBA'))
    s2.alpha_composite(im.resize((256,128),Image.NEAREST),((n%4)*264+4,(n//4)*136+4))
s2.save(sys.argv[1]+'/armor.png')
print(names)

acc=sorted(p for p in glob.glob(base+'/entity/accessory/*.png') if not p.endswith('_overlay.png'))
dm={'cat_ears':'cat_ears','cat_tail':'cat_ears','bunny_ears':'bunny_ears','bunny_tail':'bunny_ears','pleated_skirt':'pleated_skirt','maid_skirt':'maid_apron'}
s3=Image.new('RGBA',(len(acc)*264,136),(120,120,130,255))
for n,p in enumerate(acc):
    nm=os.path.basename(p)[:-4]
    im=tint(Image.open(p).convert('RGBA'),default(dm[nm])); im.alpha_composite(Image.open(p[:-4]+'_overlay.png').convert('RGBA'))
    sc=256//im.size[0]
    s3.alpha_composite(im.resize((im.size[0]*sc,im.size[1]*sc),Image.NEAREST),(n*264+4,4))
s3.save(sys.argv[1]+'/acc.png')
